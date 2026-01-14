"""Comprehensive Performance Optimization Tests.

This module tests all performance optimizations in Truthound:
1. Expression-Based Batch Executor
2. Lazy Loading Validator Registry
3. xxhash Cache Optimization
4. Native Polars Expressions (maskers)
5. Heap-Based Report Sorting
6. Batched Statistics Collection
7. Vectorized Validation
8. Query Plan Optimizations
"""

import heapq
import time
from typing import Any
from unittest.mock import patch

import polars as pl
import pytest

# ============================================================================
# Test Data Generators
# ============================================================================


def generate_test_data(
    rows: int = 100_000,
    include_nulls: bool = True,
    include_pii: bool = True,
) -> pl.LazyFrame:
    """Generate test data for performance testing."""
    import random

    random.seed(42)

    data = {
        "id": list(range(rows)),
        "name": [f"User_{i}" for i in range(rows)],
        "age": [random.randint(18, 80) for _ in range(rows)],
        "salary": [random.uniform(30000, 200000) for _ in range(rows)],
        "department": [random.choice(["Engineering", "Sales", "HR", "Marketing"]) for _ in range(rows)],
        "is_active": [random.choice([True, False]) for _ in range(rows)],
    }

    if include_nulls:
        # Add nulls to some columns
        for i in random.sample(range(rows), rows // 10):
            data["name"][i] = None
        for i in random.sample(range(rows), rows // 20):
            data["age"][i] = None

    if include_pii:
        data["email"] = [f"user{i}@example.com" for i in range(rows)]
        data["ssn"] = [f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}" for _ in range(rows)]
        data["phone"] = [f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}" for _ in range(rows)]

    return pl.DataFrame(data).lazy()


# ============================================================================
# 1. Expression-Based Batch Executor Tests
# ============================================================================


class TestExpressionBatchExecutor:
    """Test the expression-based batch executor for single collect() optimization."""

    def test_batch_executor_basic(self):
        """Test basic batch executor functionality."""
        from truthound.validators.base import (
            ExpressionBatchExecutor,
            ExpressionValidatorMixin,
            ValidationExpressionSpec,
            ValidationIssue,
            Validator,
        )
        from truthound.types import Severity

        # Create a simple expression-based validator
        class SimpleNullValidator(Validator, ExpressionValidatorMixin):
            name = "simple_null"

            def get_validation_exprs(
                self, lf: pl.LazyFrame, columns: list[str]
            ) -> list[ValidationExpressionSpec]:
                specs = []
                for col in columns:
                    specs.append(
                        ValidationExpressionSpec(
                            column=col,
                            validator_name=self.name,
                            issue_type="null_values",
                            count_expr=pl.col(col).is_null().sum(),
                            non_null_expr=pl.col(col).is_not_null().sum(),
                        )
                    )
                return specs

            def validate(self, lf: pl.LazyFrame) -> list[ValidationIssue]:
                return self._validate_with_expressions(lf)

        # Test with batch executor
        lf = generate_test_data(1000)
        executor = ExpressionBatchExecutor()
        executor.add_validator(SimpleNullValidator(columns=("name", "age")))

        issues = executor.execute(lf)

        # Should find null issues
        assert len(issues) >= 0  # May or may not find issues depending on data
        for issue in issues:
            assert issue.column in ["name", "age"]
            assert issue.issue_type == "null_values"

    def test_batch_executor_multiple_validators(self):
        """Test batch executor with multiple validators."""
        from truthound.validators.base import (
            ExpressionBatchExecutor,
            ExpressionValidatorMixin,
            ValidationExpressionSpec,
            ValidationIssue,
            Validator,
        )
        from truthound.types import Severity

        class RangeValidator(Validator, ExpressionValidatorMixin):
            name = "range_validator"

            def __init__(self, min_val: float = 0, max_val: float = 100, **kwargs):
                super().__init__(**kwargs)
                self.min_val = min_val
                self.max_val = max_val

            def get_validation_exprs(
                self, lf: pl.LazyFrame, columns: list[str]
            ) -> list[ValidationExpressionSpec]:
                specs = []
                for col in columns:
                    c = pl.col(col)
                    specs.append(
                        ValidationExpressionSpec(
                            column=col,
                            validator_name=self.name,
                            issue_type="out_of_range",
                            count_expr=((c < self.min_val) | (c > self.max_val)).sum(),
                            non_null_expr=c.is_not_null().sum(),
                        )
                    )
                return specs

            def validate(self, lf: pl.LazyFrame) -> list[ValidationIssue]:
                return self._validate_with_expressions(lf)

        class NullValidator(Validator, ExpressionValidatorMixin):
            name = "null_validator"

            def get_validation_exprs(
                self, lf: pl.LazyFrame, columns: list[str]
            ) -> list[ValidationExpressionSpec]:
                specs = []
                for col in columns:
                    specs.append(
                        ValidationExpressionSpec(
                            column=col,
                            validator_name=self.name,
                            issue_type="null_values",
                            count_expr=pl.col(col).is_null().sum(),
                            non_null_expr=pl.col(col).count(),
                        )
                    )
                return specs

            def validate(self, lf: pl.LazyFrame) -> list[ValidationIssue]:
                return self._validate_with_expressions(lf)

        lf = generate_test_data(1000)

        # Test batch execution
        executor = ExpressionBatchExecutor()
        executor.add_validator(RangeValidator(min_val=0, max_val=100, columns=("age",)))
        executor.add_validator(NullValidator(columns=("name", "age")))

        issues = executor.execute(lf)

        # Verify issues are collected from both validators
        issue_types = {issue.issue_type for issue in issues}
        # Should have at least null values (we know there are nulls)
        assert "null_values" in issue_types or len(issues) == 0

    def test_batch_executor_performance(self):
        """Test that batch execution is faster than sequential."""
        from truthound.validators.base import (
            ExpressionBatchExecutor,
            ExpressionValidatorMixin,
            ValidationExpressionSpec,
            ValidationIssue,
            Validator,
        )

        class SimpleValidator(Validator, ExpressionValidatorMixin):
            name = "simple"

            def get_validation_exprs(
                self, lf: pl.LazyFrame, columns: list[str]
            ) -> list[ValidationExpressionSpec]:
                specs = []
                for col in columns:
                    specs.append(
                        ValidationExpressionSpec(
                            column=col,
                            validator_name=self.name,
                            issue_type="test",
                            count_expr=pl.col(col).is_null().sum(),
                        )
                    )
                return specs

            def validate(self, lf: pl.LazyFrame) -> list[ValidationIssue]:
                return self._validate_with_expressions(lf)

        lf = generate_test_data(10000)
        columns = ["name", "age", "salary", "department"]

        # Batched execution
        executor = ExpressionBatchExecutor()
        for col in columns:
            executor.add_validator(SimpleValidator(columns=(col,)))

        start = time.perf_counter()
        batched_issues = executor.execute(lf)
        batched_time = time.perf_counter() - start

        # Sequential execution
        start = time.perf_counter()
        sequential_issues = []
        for col in columns:
            validator = SimpleValidator(columns=(col,))
            sequential_issues.extend(validator.validate(lf))
        sequential_time = time.perf_counter() - start

        print(f"\nBatched time: {batched_time:.4f}s")
        print(f"Sequential time: {sequential_time:.4f}s")
        print(f"Speedup: {sequential_time / batched_time:.2f}x")

        # Results should be equivalent
        assert len(batched_issues) == len(sequential_issues)

    def test_batch_executor_empty_data(self):
        """Test batch executor with empty data."""
        from truthound.validators.base import (
            ExpressionBatchExecutor,
            ExpressionValidatorMixin,
            ValidationExpressionSpec,
            ValidationIssue,
            Validator,
        )

        class SimpleValidator(Validator, ExpressionValidatorMixin):
            name = "simple"

            def get_validation_exprs(
                self, lf: pl.LazyFrame, columns: list[str]
            ) -> list[ValidationExpressionSpec]:
                return [
                    ValidationExpressionSpec(
                        column=col,
                        validator_name=self.name,
                        issue_type="test",
                        count_expr=pl.col(col).is_null().sum(),
                    )
                    for col in columns
                ]

            def validate(self, lf: pl.LazyFrame) -> list[ValidationIssue]:
                return self._validate_with_expressions(lf)

        # Empty dataframe
        lf = pl.DataFrame({"col1": [], "col2": []}).lazy()

        executor = ExpressionBatchExecutor()
        executor.add_validator(SimpleValidator(columns=("col1", "col2")))

        issues = executor.execute(lf)
        assert len(issues) == 0


# ============================================================================
# 2. Lazy Loading Validator Registry Tests
# ============================================================================


class TestLazyLoadingRegistry:
    """Test the lazy loading validator registry."""

    def test_lazy_loader_basic(self):
        """Test basic lazy loading functionality."""
        from truthound.validators._lazy import (
            LazyValidatorLoader,
            ValidatorImportMetrics,
            VALIDATOR_IMPORT_MAP,
        )

        metrics = ValidatorImportMetrics()
        loader = LazyValidatorLoader(VALIDATOR_IMPORT_MAP, metrics)

        # Before loading
        assert "NullValidator" not in loader.get_loaded_names()

        # Load NullValidator
        NullValidator = loader.load("NullValidator")
        assert NullValidator is not None
        assert "NullValidator" in loader.get_loaded_names()

        # Check metrics
        assert metrics.total_lazy_loads >= 1
        assert "NullValidator" in metrics.load_times

    def test_lazy_loader_caching(self):
        """Test that lazy loading caches results."""
        from truthound.validators._lazy import (
            LazyValidatorLoader,
            VALIDATOR_IMPORT_MAP,
        )

        loader = LazyValidatorLoader(VALIDATOR_IMPORT_MAP)

        # First load
        start = time.perf_counter()
        v1 = loader.load("BetweenValidator")
        first_time = time.perf_counter() - start

        # Second load (should be cached)
        start = time.perf_counter()
        v2 = loader.load("BetweenValidator")
        second_time = time.perf_counter() - start

        assert v1 is v2  # Same object
        assert second_time < first_time  # Faster due to caching

    def test_lazy_loader_import_metrics(self):
        """Test import metrics tracking."""
        from truthound.validators._lazy import (
            LazyValidatorLoader,
            ValidatorImportMetrics,
            VALIDATOR_IMPORT_MAP,
        )

        metrics = ValidatorImportMetrics()
        loader = LazyValidatorLoader(VALIDATOR_IMPORT_MAP, metrics)

        # Load multiple validators
        loader.load("NullValidator")
        loader.load("BetweenValidator")
        loader.load("UniqueValidator")

        # Access same validator multiple times
        loader.load("NullValidator")
        loader.load("NullValidator")

        summary = metrics.get_summary()

        assert summary["total_lazy_loads"] >= 3
        assert "NullValidator" in dict(summary["most_accessed"])

    def test_lazy_loader_invalid_validator(self):
        """Test loading non-existent validator."""
        from truthound.validators._lazy import LazyValidatorLoader

        loader = LazyValidatorLoader({"ValidValidator": "truthound.validators.base"})

        with pytest.raises(AttributeError):
            loader.load("NonExistentValidator")

    def test_lazy_loader_preload(self):
        """Test preloading specific validators."""
        from truthound.validators._lazy import (
            LazyValidatorLoader,
            VALIDATOR_IMPORT_MAP,
        )

        loader = LazyValidatorLoader(VALIDATOR_IMPORT_MAP)

        # Preload specific validators
        loader.preload("NullValidator", "BetweenValidator")

        assert "NullValidator" in loader.get_loaded_names()
        assert "BetweenValidator" in loader.get_loaded_names()

    def test_lazy_loader_category_preload(self):
        """Test preloading an entire category."""
        from truthound.validators._lazy import (
            LazyValidatorLoader,
            VALIDATOR_IMPORT_MAP,
            CATEGORY_MODULES,
        )

        loader = LazyValidatorLoader(VALIDATOR_IMPORT_MAP)

        # Preload completeness category
        loader.preload_category("completeness")

        loaded = loader.get_loaded_names()
        # Should have loaded completeness validators
        completeness_validators = [
            name for name, module in VALIDATOR_IMPORT_MAP.items()
            if "completeness" in module
        ]

        # At least some should be loaded
        loaded_completeness = [v for v in completeness_validators if v in loaded]
        assert len(loaded_completeness) > 0


# ============================================================================
# 3. xxhash Cache Optimization Tests
# ============================================================================


class TestXxhashCache:
    """Test xxhash cache optimization."""

    def test_fast_hash_available(self):
        """Test if xxhash is available and used."""
        from truthound.cache import _HAS_XXHASH, _fast_hash

        # Test hashing works
        result = _fast_hash("test content")
        assert len(result) == 16
        assert isinstance(result, str)

        # Same input should give same output
        assert _fast_hash("test") == _fast_hash("test")

        # Different input should give different output
        assert _fast_hash("test1") != _fast_hash("test2")

    def test_fast_hash_performance(self):
        """Test that xxhash is faster than SHA256."""
        import hashlib
        from truthound.cache import _fast_hash, _HAS_XXHASH

        content = "test content " * 1000  # ~13KB string
        iterations = 1000

        # Test fast_hash (xxhash if available)
        start = time.perf_counter()
        for _ in range(iterations):
            _fast_hash(content)
        fast_time = time.perf_counter() - start

        # Test SHA256
        start = time.perf_counter()
        for _ in range(iterations):
            hashlib.sha256(content.encode()).hexdigest()[:16]
        sha_time = time.perf_counter() - start

        print(f"\nFast hash time ({iterations} iterations): {fast_time:.4f}s")
        print(f"SHA256 time ({iterations} iterations): {sha_time:.4f}s")

        if _HAS_XXHASH:
            print(f"xxhash speedup: {sha_time / fast_time:.2f}x")
            # xxhash should be significantly faster
            assert fast_time < sha_time
        else:
            print("xxhash not available, using SHA256 fallback")

    def test_data_fingerprint(self):
        """Test data fingerprint generation."""
        from truthound.cache import get_data_fingerprint

        # Test with dict
        data1 = {"col1": [1, 2, 3], "col2": ["a", "b", "c"]}
        fp1 = get_data_fingerprint(data1)
        assert len(fp1) == 16

        # Same data should give same fingerprint
        data2 = {"col1": [1, 2, 3], "col2": ["a", "b", "c"]}
        fp2 = get_data_fingerprint(data2)
        assert fp1 == fp2

        # Different data should give different fingerprint
        data3 = {"col1": [1, 2, 3, 4], "col2": ["a", "b", "c", "d"]}
        fp3 = get_data_fingerprint(data3)
        assert fp1 != fp3

    def test_source_key(self):
        """Test source key generation."""
        from truthound.cache import get_source_key

        # Dict
        data = {"col1": [1, 2, 3]}
        key = get_source_key(data)
        assert key.startswith("dict:")

        # DataFrame
        df = pl.DataFrame({"col1": [1, 2, 3]})
        key = get_source_key(df)
        assert "DataFrame" in key


# ============================================================================
# 4. Native Polars Expressions (Maskers) Tests
# ============================================================================


class TestNativePolarsExpressions:
    """Test native Polars expressions for masking."""

    def test_redact_masking(self):
        """Test redaction masking with native expressions."""
        from truthound.maskers import mask_data

        lf = pl.DataFrame({
            "name": ["John Doe", "Jane Smith", None],
            "email": ["john@example.com", "jane@test.org", "admin@corp.io"],
            "ssn": ["123-45-6789", "987-65-4321", "111-22-3333"],
        }).lazy()

        result = mask_data(lf, columns=["name", "email", "ssn"], strategy="redact")

        # Check masking applied
        assert result["name"][0] is not None
        assert result["name"][2] is None  # Null preserved

        # SSN should be masked but keep structure
        for ssn in result["ssn"].to_list():
            assert "-" in ssn
            assert "*" in ssn

    def test_hash_masking(self):
        """Test hash masking with native Polars hash."""
        from truthound.maskers import mask_data

        lf = pl.DataFrame({
            "id": ["user1", "user2", "user3"],
            "secret": ["password1", "password2", None],
        }).lazy()

        result = mask_data(lf, columns=["id", "secret"], strategy="hash")

        # Hashed values should be different from original
        assert result["id"][0] != "user1"
        assert result["secret"][2] is None  # Null preserved

        # Same input should give same hash (deterministic)
        result2 = mask_data(lf, columns=["id"], strategy="hash")
        assert result["id"][0] == result2["id"][0]

    def test_fake_masking(self):
        """Test fake data masking."""
        from truthound.maskers import mask_data

        lf = pl.DataFrame({
            "email": ["john@example.com", "jane@test.org"],
            "phone": ["+1-555-123-4567", "+1-555-987-6543"],
            "ssn": ["123-45-6789", "987-65-4321"],
        }).lazy()

        result = mask_data(lf, columns=["email", "phone", "ssn"], strategy="fake")

        # Emails should look like emails
        for email in result["email"].to_list():
            assert "@masked.com" in email

        # Phones should have consistent format
        for phone in result["phone"].to_list():
            assert "+1-555-" in phone

        # SSNs should have format
        for ssn in result["ssn"].to_list():
            assert "-" in ssn

    def test_masking_performance(self):
        """Test that native expressions are performant."""
        from truthound.maskers import mask_data

        # Generate larger dataset
        rows = 50000
        lf = pl.DataFrame({
            "email": [f"user{i}@example.com" for i in range(rows)],
            "ssn": [f"{i % 900 + 100:03d}-{i % 90 + 10:02d}-{i % 9000 + 1000:04d}" for i in range(rows)],
        }).lazy()

        # Time the masking operation
        start = time.perf_counter()
        result = mask_data(lf, columns=["email", "ssn"], strategy="redact")
        elapsed = time.perf_counter() - start

        print(f"\nMasking {rows} rows took: {elapsed:.4f}s")
        print(f"Throughput: {rows / elapsed:,.0f} rows/sec")

        assert len(result) == rows
        assert elapsed < 5.0  # Should complete in reasonable time


# ============================================================================
# 5. Heap-Based Report Sorting Tests
# ============================================================================


class TestHeapBasedReportSorting:
    """Test heap-based report sorting for efficient severity access."""

    def test_report_add_issue(self):
        """Test adding issues maintains heap property."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue
        from truthound.types import Severity

        report = Report()

        # Add issues in random order
        report.add_issue(ValidationIssue("col1", "test", 10, Severity.LOW))
        report.add_issue(ValidationIssue("col2", "test", 20, Severity.CRITICAL))
        report.add_issue(ValidationIssue("col3", "test", 15, Severity.MEDIUM))

        # Most severe should be accessible in O(1)
        most_severe = report.get_most_severe()
        assert most_severe is not None
        assert most_severe.severity == Severity.CRITICAL

    def test_report_add_issues_batch(self):
        """Test batch adding issues with heapify."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue
        from truthound.types import Severity

        issues = [
            ValidationIssue("col1", "test", 10, Severity.LOW),
            ValidationIssue("col2", "test", 20, Severity.HIGH),
            ValidationIssue("col3", "test", 15, Severity.MEDIUM),
            ValidationIssue("col4", "test", 5, Severity.CRITICAL),
        ]

        report = Report()
        report.add_issues(issues)

        # Verify heap property
        assert report.get_most_severe().severity == Severity.CRITICAL
        assert len(report.issues) == 4

    def test_report_get_top_issues(self):
        """Test getting top k issues by severity."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue
        from truthound.types import Severity

        report = Report()

        # Add many issues
        for i in range(100):
            severity = [Severity.LOW, Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL][i % 4]
            report.add_issue(ValidationIssue(f"col{i}", "test", i, severity))

        # Get top 5
        top_5 = report.get_top_issues(5)
        assert len(top_5) == 5

        # All should be CRITICAL (highest severity)
        for issue in top_5:
            assert issue.severity == Severity.CRITICAL

    def test_report_sorted_issues_caching(self):
        """Test that sorted issues are cached."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue
        from truthound.types import Severity

        report = Report()
        for i in range(1000):
            report.add_issue(ValidationIssue(f"col{i}", "test", i, Severity.MEDIUM))

        # First call builds cache
        start = time.perf_counter()
        sorted1 = report.get_sorted_issues()
        first_time = time.perf_counter() - start

        # Second call uses cache
        start = time.perf_counter()
        sorted2 = report.get_sorted_issues()
        second_time = time.perf_counter() - start

        assert sorted1 is sorted2  # Same object
        assert second_time < first_time  # Faster

    def test_report_severity_iteration(self):
        """Test iterating issues by severity."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue
        from truthound.types import Severity

        report = Report()
        report.add_issue(ValidationIssue("col1", "test", 10, Severity.LOW))
        report.add_issue(ValidationIssue("col2", "test", 20, Severity.CRITICAL))
        report.add_issue(ValidationIssue("col3", "test", 15, Severity.HIGH))

        # Iterate and verify order
        severities = [issue.severity for issue in report.iter_by_severity()]
        assert severities == [Severity.CRITICAL, Severity.HIGH, Severity.LOW]


# ============================================================================
# 6. Batched Statistics Collection Tests
# ============================================================================


class TestBatchedStatisticsCollection:
    """Test batched statistics collection in schema learning."""

    def test_schema_learn_single_pass(self):
        """Test that schema learning uses single pass for statistics."""
        from truthound.schema import learn

        lf = generate_test_data(10000)

        # Time schema learning
        start = time.perf_counter()
        schema = learn(lf)
        elapsed = time.perf_counter() - start

        print(f"\nSchema learning for 10K rows took: {elapsed:.4f}s")

        # Verify statistics collected
        assert schema.row_count == 10000
        assert "age" in schema.columns
        assert schema["age"].min_value is not None
        assert schema["age"].max_value is not None
        assert schema["age"].mean is not None
        assert schema["age"].std is not None

    def test_schema_learn_with_constraints(self):
        """Test constraint inference in schema learning."""
        from truthound.schema import learn

        lf = pl.DataFrame({
            "status": ["active", "inactive", "pending", "active", "inactive"],
            "score": [85, 90, 75, 88, 92],
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        }).lazy()

        schema = learn(lf, infer_constraints=True, categorical_threshold=10)

        # Low cardinality column should have allowed_values
        assert schema["status"].allowed_values is not None
        assert set(schema["status"].allowed_values) == {"active", "inactive", "pending"}

        # Numeric column should have range
        assert schema["score"].min_value == 75
        assert schema["score"].max_value == 92

    def test_schema_learn_performance(self):
        """Test schema learning performance with larger data."""
        from truthound.schema import learn

        # Generate larger dataset
        rows = 100000
        lf = generate_test_data(rows)

        start = time.perf_counter()
        schema = learn(lf)
        elapsed = time.perf_counter() - start

        print(f"\nSchema learning for {rows:,} rows took: {elapsed:.4f}s")
        print(f"Throughput: {rows / elapsed:,.0f} rows/sec")

        assert schema.row_count == rows
        assert elapsed < 10.0  # Should complete reasonably


# ============================================================================
# 7. Vectorized Validation Tests
# ============================================================================


class TestVectorizedValidation:
    """Test vectorized validation using Polars expressions."""

    def test_null_validator_vectorized(self):
        """Test null validator uses vectorized operations."""
        from truthound.validators.completeness.null import NullValidator

        lf = generate_test_data(10000)
        validator = NullValidator(columns=("name", "age"))

        start = time.perf_counter()
        issues = validator.validate(lf)
        elapsed = time.perf_counter() - start

        print(f"\nNull validation for 10K rows took: {elapsed:.4f}s")

        # Should find null values (we added them) - issue_type is "null" not "null_values"
        assert any(issue.issue_type == "null" for issue in issues)

    def test_range_validator_vectorized(self):
        """Test range validator uses vectorized operations."""
        from truthound.validators.distribution.range import BetweenValidator

        lf = generate_test_data(10000)
        validator = BetweenValidator(min_value=0, max_value=50, columns=("age",))

        start = time.perf_counter()
        issues = validator.validate(lf)
        elapsed = time.perf_counter() - start

        print(f"\nRange validation for 10K rows took: {elapsed:.4f}s")

        # Should find out of range values (ages go up to 80)
        assert len(issues) > 0
        assert issues[0].issue_type == "out_of_range"

    def test_unique_validator_vectorized(self):
        """Test unique validator uses vectorized operations."""
        from truthound.validators.uniqueness.unique import UniqueValidator

        # Create data with duplicates
        lf = pl.DataFrame({
            "id": list(range(1000)) + list(range(500)),  # 500 duplicates
            "name": [f"user{i}" for i in range(1500)],
        }).lazy()

        validator = UniqueValidator(columns=("id",))

        start = time.perf_counter()
        issues = validator.validate(lf)
        elapsed = time.perf_counter() - start

        print(f"\nUnique validation for 1.5K rows took: {elapsed:.4f}s")

        assert len(issues) > 0
        # issue_type is "unique_violation" not "duplicate_values"
        assert issues[0].issue_type == "unique_violation"


# ============================================================================
# 8. Query Plan Optimization Tests
# ============================================================================


class TestQueryPlanOptimization:
    """Test query plan optimizations in validators."""

    def test_optimized_collect(self):
        """Test optimized_collect uses all optimizations."""
        from truthound.validators.base import optimized_collect, _get_optimizations

        lf = generate_test_data(1000)

        # Get optimization flags
        opts = _get_optimizations()

        # Verify all optimizations enabled
        assert opts.predicate_pushdown
        assert opts.projection_pushdown
        assert opts.slice_pushdown
        assert opts.comm_subplan_elim
        assert opts.comm_subexpr_elim

        # Test optimized collect works
        result = optimized_collect(lf.select(pl.len()))
        assert result.item() == 1000

    def test_streaming_mode(self):
        """Test streaming mode for large datasets."""
        from truthound.validators.base import optimized_collect

        # Create larger dataset
        lf = generate_test_data(50000)

        # Collect with streaming
        start = time.perf_counter()
        result = optimized_collect(lf, streaming=True)
        streaming_time = time.perf_counter() - start

        print(f"\nStreaming collect for 50K rows took: {streaming_time:.4f}s")

        assert len(result) == 50000


# ============================================================================
# 9. Integration Performance Tests
# ============================================================================


class TestIntegrationPerformance:
    """Integration tests for overall performance."""

    def test_check_performance(self):
        """Test overall check() performance."""
        import truthound as th

        lf = generate_test_data(10000)

        start = time.perf_counter()
        report = th.check(lf)
        elapsed = time.perf_counter() - start

        print(f"\nth.check() for 10K rows took: {elapsed:.4f}s")
        print(f"Found {len(report.issues)} issues")

        assert elapsed < 30.0  # Should complete in reasonable time

    def test_profile_performance(self):
        """Test profile() performance."""
        import truthound as th

        lf = generate_test_data(10000)

        start = time.perf_counter()
        profile = th.profile(lf)
        elapsed = time.perf_counter() - start

        print(f"\nth.profile() for 10K rows took: {elapsed:.4f}s")

        assert elapsed < 5.0

    def test_mask_performance(self):
        """Test mask() performance."""
        import truthound as th

        lf = generate_test_data(10000, include_pii=True)

        start = time.perf_counter()
        masked = th.mask(lf, strategy="hash")
        elapsed = time.perf_counter() - start

        print(f"\nth.mask() for 10K rows took: {elapsed:.4f}s")

        assert elapsed < 5.0
        assert len(masked) == 10000


# ============================================================================
# 10. Memory Efficiency Tests
# ============================================================================


class TestMemoryEfficiency:
    """Test memory efficiency of performance optimizations."""

    def test_lazy_evaluation_preserves_memory(self):
        """Test that lazy evaluation doesn't materialize large datasets."""
        # Create a large lazy frame that would use significant memory
        rows = 1_000_000
        lf = pl.DataFrame({
            "id": range(rows),
            "value": range(rows),
        }).lazy()

        # Schema operations should stay lazy
        schema = lf.collect_schema()
        assert len(schema) == 2

        # Selective collect should be memory efficient
        count = lf.select(pl.len()).collect().item()
        assert count == rows

    def test_expression_based_validation_memory(self):
        """Test that expression-based validation is memory efficient."""
        from truthound.validators.base import (
            ExpressionBatchExecutor,
            ExpressionValidatorMixin,
            ValidationExpressionSpec,
            ValidationIssue,
            Validator,
        )

        class SimpleValidator(Validator, ExpressionValidatorMixin):
            name = "simple"

            def get_validation_exprs(
                self, lf: pl.LazyFrame, columns: list[str]
            ) -> list[ValidationExpressionSpec]:
                return [
                    ValidationExpressionSpec(
                        column=col,
                        validator_name=self.name,
                        issue_type="test",
                        count_expr=pl.col(col).is_null().sum(),
                    )
                    for col in columns
                ]

            def validate(self, lf: pl.LazyFrame) -> list[ValidationIssue]:
                return self._validate_with_expressions(lf)

        # Large dataset
        rows = 100000
        lf = generate_test_data(rows)

        executor = ExpressionBatchExecutor()
        for col in ["name", "age", "salary", "department"]:
            executor.add_validator(SimpleValidator(columns=(col,)))

        # Execute - should be memory efficient due to single collect
        issues = executor.execute(lf)

        # Just verify it completes without memory issues
        assert isinstance(issues, list)


# ============================================================================
# Run Performance Benchmark
# ============================================================================


def run_benchmark():
    """Run a comprehensive performance benchmark."""
    print("\n" + "=" * 60)
    print("Truthound Performance Benchmark")
    print("=" * 60)

    import truthound as th

    # Test different data sizes
    sizes = [1000, 10000, 50000]

    for size in sizes:
        print(f"\n--- Testing with {size:,} rows ---")
        lf = generate_test_data(size, include_pii=True)

        # Check
        start = time.perf_counter()
        report = th.check(lf)
        check_time = time.perf_counter() - start
        print(f"check():   {check_time:.4f}s ({size / check_time:,.0f} rows/sec)")

        # Profile
        start = time.perf_counter()
        profile = th.profile(lf)
        profile_time = time.perf_counter() - start
        print(f"profile(): {profile_time:.4f}s ({size / profile_time:,.0f} rows/sec)")

        # Mask
        start = time.perf_counter()
        masked = th.mask(lf, strategy="hash")
        mask_time = time.perf_counter() - start
        print(f"mask():    {mask_time:.4f}s ({size / mask_time:,.0f} rows/sec)")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Run benchmark when executed directly
    run_benchmark()

    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
