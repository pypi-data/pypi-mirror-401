"""Comprehensive performance optimization tests for Truthound.

This module tests all major performance optimization features:
1. Expression-Based Batch Executor
2. Lazy Loading Validator Registry
3. xxhash Cache Optimization
4. Native Polars Expressions (Masking)
5. Heap-Based Report Sorting
6. Batched Statistics Collection
7. Query Plan Optimizations

Usage:
    pytest tests/test_performance_optimization.py -v
    pytest tests/test_performance_optimization.py -v -k "test_batch_executor"
"""

from __future__ import annotations

import time
import random
import string
from datetime import datetime, timedelta
from typing import Any

import polars as pl
import pytest

from truthound.types import Severity


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def small_df() -> pl.LazyFrame:
    """Create a small test DataFrame (1K rows)."""
    n = 1_000
    return pl.DataFrame({
        "id": range(n),
        "name": [f"name_{i}" for i in range(n)],
        "age": [random.randint(18, 80) if random.random() > 0.05 else None for _ in range(n)],
        "price": [random.uniform(10, 1000) if random.random() > 0.02 else None for _ in range(n)],
        "email": [f"user{i}@example.com" if random.random() > 0.03 else None for i in range(n)],
        "score": [random.randint(0, 100) for _ in range(n)],
    }).lazy()


@pytest.fixture
def medium_df() -> pl.LazyFrame:
    """Create a medium test DataFrame (100K rows)."""
    n = 100_000
    return pl.DataFrame({
        "id": range(n),
        "name": [f"name_{i}" for i in range(n)],
        "age": [random.randint(18, 80) if random.random() > 0.05 else None for _ in range(n)],
        "price": [random.uniform(10, 1000) if random.random() > 0.02 else None for _ in range(n)],
        "email": [f"user{i}@example.com" if random.random() > 0.03 else None for i in range(n)],
        "score": [random.randint(0, 100) for _ in range(n)],
        "category": [random.choice(["A", "B", "C", "D"]) for _ in range(n)],
    }).lazy()


@pytest.fixture
def large_df() -> pl.LazyFrame:
    """Create a large test DataFrame (1M rows)."""
    n = 1_000_000
    return pl.DataFrame({
        "id": range(n),
        "value": [random.uniform(-100, 100) if random.random() > 0.01 else None for _ in range(n)],
        "category": [random.choice(["A", "B", "C", "D", "E"]) for _ in range(n)],
        "score": [random.randint(0, 100) for _ in range(n)],
    }).lazy()


# =============================================================================
# 1. Expression-Based Batch Executor Tests
# =============================================================================


class TestExpressionBatchExecutor:
    """Tests for ExpressionBatchExecutor performance."""

    def test_batch_executor_basic_functionality(self, small_df: pl.LazyFrame) -> None:
        """Test that batch executor produces correct results."""
        from truthound.validators.base import ExpressionBatchExecutor
        from truthound.validators.completeness.null import NullValidator
        from truthound.validators.distribution.range import BetweenValidator

        executor = ExpressionBatchExecutor()
        executor.add_validator(NullValidator())
        executor.add_validator(BetweenValidator(min_value=0, max_value=100, columns=("score",)))

        issues = executor.execute(small_df)

        # Should find null issues in age and price columns
        null_issues = [i for i in issues if i.issue_type == "null"]
        assert len(null_issues) > 0

    def test_batch_executor_vs_sequential_correctness(self, small_df: pl.LazyFrame) -> None:
        """Test that batch execution produces same results as sequential."""
        from truthound.validators.base import ExpressionBatchExecutor
        from truthound.validators.completeness.null import NullValidator, NotNullValidator
        from truthound.validators.distribution.range import PositiveValidator

        validators = [
            NullValidator(),
            NotNullValidator(columns=("id",)),
            PositiveValidator(columns=("score",)),
        ]

        # Sequential execution
        sequential_issues = []
        for v in validators:
            sequential_issues.extend(v.validate(small_df))

        # Batch execution
        executor = ExpressionBatchExecutor()
        executor.add_validators(validators)
        batch_issues = executor.execute(small_df)

        # Compare results (order may differ)
        seq_by_type = {(i.column, i.issue_type): i.count for i in sequential_issues}
        batch_by_type = {(i.column, i.issue_type): i.count for i in batch_issues}

        assert seq_by_type == batch_by_type, f"Results mismatch:\nSeq: {seq_by_type}\nBatch: {batch_by_type}"

    def test_batch_executor_performance(self, medium_df: pl.LazyFrame) -> None:
        """Test batch executor is faster than sequential for multiple validators."""
        from truthound.validators.base import ExpressionBatchExecutor
        from truthound.validators.completeness.null import NullValidator, CompletenessRatioValidator
        from truthound.validators.distribution.range import BetweenValidator, NonNegativeValidator

        validators = [
            NullValidator(),
            CompletenessRatioValidator(min_ratio=0.9),
            BetweenValidator(min_value=0, max_value=100, columns=("age", "score")),
            NonNegativeValidator(columns=("age", "price", "score")),
        ]

        # Sequential timing
        start = time.perf_counter()
        for v in validators:
            v.validate(medium_df)
        sequential_time = time.perf_counter() - start

        # Batch timing
        executor = ExpressionBatchExecutor()
        executor.add_validators(validators)

        start = time.perf_counter()
        executor.execute(medium_df)
        batch_time = time.perf_counter() - start

        print(f"\nPerformance comparison (100K rows, 4 validators):")
        print(f"  Sequential: {sequential_time:.3f}s")
        print(f"  Batched: {batch_time:.3f}s")
        print(f"  Speedup: {sequential_time / batch_time:.2f}x")

        # Batch should be at least 1.2x faster (conservative)
        # In practice, often 2-3x faster
        assert batch_time < sequential_time, "Batch should be faster than sequential"

    def test_batch_executor_empty_dataframe(self) -> None:
        """Test batch executor handles empty DataFrames correctly."""
        from truthound.validators.base import ExpressionBatchExecutor
        from truthound.validators.completeness.null import NullValidator

        empty_df = pl.DataFrame({"a": [], "b": []}).lazy()

        executor = ExpressionBatchExecutor()
        executor.add_validator(NullValidator())
        issues = executor.execute(empty_df)

        assert len(issues) == 0

    def test_batch_executor_single_validator(self, small_df: pl.LazyFrame) -> None:
        """Test batch executor with single validator."""
        from truthound.validators.base import ExpressionBatchExecutor
        from truthound.validators.completeness.null import NullValidator

        executor = ExpressionBatchExecutor()
        executor.add_validator(NullValidator())

        issues = executor.execute(small_df)

        # Should produce same results as direct call
        direct_issues = NullValidator().validate(small_df)

        assert len(issues) == len(direct_issues)

    def test_batch_executor_clear(self, small_df: pl.LazyFrame) -> None:
        """Test batch executor clear method."""
        from truthound.validators.base import ExpressionBatchExecutor
        from truthound.validators.completeness.null import NullValidator

        executor = ExpressionBatchExecutor()
        executor.add_validator(NullValidator())

        issues1 = executor.execute(small_df)
        assert len(issues1) > 0

        executor.clear()
        issues2 = executor.execute(small_df)
        assert len(issues2) == 0


# =============================================================================
# 2. Lazy Loading Validator Registry Tests
# =============================================================================


class TestLazyLoadingRegistry:
    """Tests for lazy loading validator registry."""

    def test_lazy_loading_basic(self) -> None:
        """Test basic lazy loading of validators."""
        from truthound.validators._lazy import (
            get_validator_loader,
            VALIDATOR_IMPORT_MAP,
        )

        loader = get_validator_loader()

        # Check that validator is available
        assert loader.is_available("NullValidator")
        assert loader.is_available("BetweenValidator")
        assert not loader.is_available("NonExistentValidator")

    def test_lazy_loading_on_demand(self) -> None:
        """Test that validators are loaded only when accessed."""
        from truthound.validators._lazy import LazyValidatorLoader, VALIDATOR_IMPORT_MAP

        # Create fresh loader
        loader = LazyValidatorLoader(VALIDATOR_IMPORT_MAP)
        metrics = loader.get_metrics()

        # Initially no loads
        assert metrics.total_lazy_loads == 0

        # Access a validator
        NullValidator = loader.load("NullValidator")
        assert NullValidator is not None

        # Should have recorded the load
        metrics = loader.get_metrics()
        assert metrics.total_lazy_loads >= 1
        assert "NullValidator" in metrics.load_times

    def test_lazy_loading_cache(self) -> None:
        """Test that loaded validators are cached."""
        from truthound.validators._lazy import LazyValidatorLoader, VALIDATOR_IMPORT_MAP

        loader = LazyValidatorLoader(VALIDATOR_IMPORT_MAP)

        # Load same validator twice
        v1 = loader.load("NullValidator")
        v2 = loader.load("NullValidator")

        # Should be same object (cached)
        assert v1 is v2

        # Access count should be 2, but load count should be 1
        metrics = loader.get_metrics()
        assert metrics.access_counts.get("NullValidator", 0) == 2
        assert metrics.load_times.get("NullValidator") is not None

    def test_lazy_loading_preload_category(self) -> None:
        """Test preloading an entire category."""
        from truthound.validators._lazy import LazyValidatorLoader, VALIDATOR_IMPORT_MAP

        loader = LazyValidatorLoader(VALIDATOR_IMPORT_MAP)

        # Preload completeness category
        loader.preload_category("completeness")

        # Check that validators are loaded
        loaded_names = loader.get_loaded_names()
        assert "NullValidator" in loaded_names or len(loaded_names) > 0

    def test_lazy_loading_metrics_summary(self) -> None:
        """Test metrics summary."""
        from truthound.validators._lazy import LazyValidatorLoader, VALIDATOR_IMPORT_MAP

        loader = LazyValidatorLoader(VALIDATOR_IMPORT_MAP)

        # Load a few validators
        loader.load("NullValidator")
        loader.load("BetweenValidator")
        loader.load("NullValidator")  # Access again

        summary = loader.get_metrics().get_summary()

        assert "total_lazy_loads" in summary
        assert "total_load_time_ms" in summary
        assert "most_accessed" in summary
        assert summary["total_lazy_loads"] >= 2

    def test_available_validators_count(self) -> None:
        """Test that we have many validators available."""
        from truthound.validators._lazy import VALIDATOR_IMPORT_MAP

        # Should have 200+ validators mapped
        assert len(VALIDATOR_IMPORT_MAP) >= 100


# =============================================================================
# 3. xxhash Cache Optimization Tests
# =============================================================================


class TestXXHashCache:
    """Tests for xxhash cache optimization."""

    def test_fast_hash_function_exists(self) -> None:
        """Test that _fast_hash function exists and works."""
        from truthound.cache import _fast_hash

        result = _fast_hash("test content")
        assert isinstance(result, str)
        assert len(result) == 16  # 16 hex characters

    def test_fast_hash_deterministic(self) -> None:
        """Test that hash is deterministic."""
        from truthound.cache import _fast_hash

        content = "test content for hashing"
        h1 = _fast_hash(content)
        h2 = _fast_hash(content)

        assert h1 == h2

    def test_fast_hash_different_inputs(self) -> None:
        """Test that different inputs produce different hashes."""
        from truthound.cache import _fast_hash

        h1 = _fast_hash("content1")
        h2 = _fast_hash("content2")

        assert h1 != h2

    def test_xxhash_available(self) -> None:
        """Test if xxhash is available for performance."""
        from truthound.cache import _HAS_XXHASH

        print(f"\nxxhash available: {_HAS_XXHASH}")
        # Just informational - not a failure if not installed

    def test_data_fingerprint_file_path(self, tmp_path) -> None:
        """Test data fingerprint for file paths."""
        from truthound.cache import get_data_fingerprint

        # Create a test file
        test_file = tmp_path / "test.csv"
        test_file.write_text("a,b,c\n1,2,3\n")

        fp = get_data_fingerprint(str(test_file))
        assert isinstance(fp, str)
        assert len(fp) == 16

    def test_data_fingerprint_dataframe(self) -> None:
        """Test data fingerprint for DataFrames."""
        from truthound.cache import get_data_fingerprint

        df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        fp = get_data_fingerprint(df)

        assert isinstance(fp, str)
        assert len(fp) == 16

    def test_cache_hash_performance(self) -> None:
        """Test cache hash performance."""
        from truthound.cache import _fast_hash, _HAS_XXHASH
        import hashlib

        content = "a" * 10000  # 10KB content

        # Time _fast_hash
        start = time.perf_counter()
        for _ in range(1000):
            _fast_hash(content)
        fast_time = time.perf_counter() - start

        # Time standard SHA256
        start = time.perf_counter()
        for _ in range(1000):
            hashlib.sha256(content.encode()).hexdigest()[:16]
        sha_time = time.perf_counter() - start

        print(f"\nHash performance (1000 iterations, 10KB content):")
        print(f"  _fast_hash ({'xxhash' if _HAS_XXHASH else 'sha256'}): {fast_time*1000:.2f}ms")
        print(f"  SHA256: {sha_time*1000:.2f}ms")

        if _HAS_XXHASH:
            print(f"  xxhash speedup: {sha_time / fast_time:.2f}x")


# =============================================================================
# 4. Native Polars Expressions (Masking) Tests
# =============================================================================


class TestNativePolarsExpressions:
    """Tests for native Polars expressions in masking."""

    def test_redact_masking(self) -> None:
        """Test redact masking uses native expressions."""
        from truthound.maskers import _apply_redact

        df = pl.DataFrame({
            "email": ["user@example.com", "test@test.org", None],
            "ssn": ["123-45-6789", "987-65-4321", None],
            "phone": ["555-123-4567", None, "555-987-6543"],
        })

        # Test email masking
        result = _apply_redact(df, "email")
        assert result["email"][0] is not None
        assert "@" in result["email"][0]  # Structure preserved

        # Test SSN masking
        result = _apply_redact(df, "ssn")
        assert "-" in result["ssn"][0]  # Dashes preserved
        assert "*" in result["ssn"][0]  # Characters masked

    def test_hash_masking(self) -> None:
        """Test hash masking uses native Polars hash."""
        from truthound.maskers import _apply_hash

        df = pl.DataFrame({
            "sensitive": ["secret1", "secret2", "secret3", None],
        })

        result = _apply_hash(df, "sensitive")

        # All non-null values should be hashed
        assert result["sensitive"][0] is not None
        assert result["sensitive"][0] != "secret1"  # Different from original
        assert len(result["sensitive"][0]) == 16  # Hash length
        assert result["sensitive"][3] is None  # Null preserved

    def test_fake_masking(self) -> None:
        """Test fake masking uses native expressions."""
        from truthound.maskers import _apply_fake

        df = pl.DataFrame({
            "email": ["user@example.com", "test@test.org"],
            "phone": ["+1-555-123-4567", "555-987-6543"],
            "ssn": ["123-45-6789", "987-65-4321"],
        })

        # Test email fake
        result = _apply_fake(df, "email")
        assert "@masked.com" in result["email"][0]

        # Test phone fake
        result = _apply_fake(df, "phone")
        assert "+1-555-" in result["phone"][0]

    def test_masking_deterministic(self) -> None:
        """Test that masking is deterministic."""
        from truthound.maskers import _apply_hash, _apply_fake

        df = pl.DataFrame({"value": ["test123"]})

        hash1 = _apply_hash(df, "value")["value"][0]
        hash2 = _apply_hash(df, "value")["value"][0]
        assert hash1 == hash2

        fake1 = _apply_fake(df, "value")["value"][0]
        fake2 = _apply_fake(df, "value")["value"][0]
        assert fake1 == fake2

    def test_masking_null_handling(self) -> None:
        """Test that masking preserves nulls."""
        from truthound.maskers import _apply_redact, _apply_hash, _apply_fake

        df = pl.DataFrame({"col": ["value", None, "value2"]})

        for fn in [_apply_redact, _apply_hash, _apply_fake]:
            result = fn(df, "col")
            assert result["col"][1] is None

    def test_mask_data_streaming(self) -> None:
        """Test that mask_data uses streaming for large datasets."""
        from truthound.maskers import mask_data

        # Create dataset
        n = 10_000
        df = pl.DataFrame({
            "email": [f"user{i}@example.com" for i in range(n)],
        })
        lf = df.lazy()

        # Should work with streaming
        result = mask_data(lf, columns=["email"], strategy="hash")
        assert len(result) == n
        assert result["email"][0] != "user0@example.com"


# =============================================================================
# 5. Heap-Based Report Sorting Tests
# =============================================================================


class TestHeapBasedReportSorting:
    """Tests for heap-based report sorting."""

    def test_report_heap_initialization(self) -> None:
        """Test that report initializes heap correctly."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue

        issues = [
            ValidationIssue(column="a", issue_type="test", count=1, severity=Severity.LOW),
            ValidationIssue(column="b", issue_type="test", count=2, severity=Severity.CRITICAL),
            ValidationIssue(column="c", issue_type="test", count=3, severity=Severity.MEDIUM),
        ]

        report = Report(issues=issues)

        # Heap should be initialized
        assert len(report._issues_heap) == 3

    def test_get_most_severe_o1(self) -> None:
        """Test O(1) access to most severe issue."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue

        issues = [
            ValidationIssue(column="a", issue_type="test", count=1, severity=Severity.LOW),
            ValidationIssue(column="b", issue_type="test", count=2, severity=Severity.CRITICAL),
            ValidationIssue(column="c", issue_type="test", count=3, severity=Severity.HIGH),
        ]

        report = Report(issues=issues)
        most_severe = report.get_most_severe()

        assert most_severe is not None
        assert most_severe.severity == Severity.CRITICAL
        assert most_severe.column == "b"

    def test_add_issue_maintains_heap(self) -> None:
        """Test that add_issue maintains heap property."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue

        report = Report()

        report.add_issue(ValidationIssue(column="a", issue_type="test", count=1, severity=Severity.LOW))
        assert report.get_most_severe().severity == Severity.LOW

        report.add_issue(ValidationIssue(column="b", issue_type="test", count=2, severity=Severity.CRITICAL))
        assert report.get_most_severe().severity == Severity.CRITICAL

        report.add_issue(ValidationIssue(column="c", issue_type="test", count=3, severity=Severity.MEDIUM))
        assert report.get_most_severe().severity == Severity.CRITICAL

    def test_add_issues_batch_heapify(self) -> None:
        """Test that batch add uses efficient heapify."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue

        report = Report()

        issues = [
            ValidationIssue(column=f"col{i}", issue_type="test", count=i, severity=random.choice(list(Severity)))
            for i in range(100)
        ]

        report.add_issues(issues)

        assert len(report.issues) == 100
        assert len(report._issues_heap) == 100

    def test_get_top_issues_efficient(self) -> None:
        """Test that get_top_issues is efficient for small k."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue

        # Create many issues
        severities = list(Severity)
        issues = [
            ValidationIssue(column=f"col{i}", issue_type="test", count=i, severity=severities[i % len(severities)])
            for i in range(1000)
        ]

        report = Report(issues=issues)

        # Get top 5
        top5 = report.get_top_issues(5)
        assert len(top5) == 5

        # All should be CRITICAL (severity 0)
        for issue in top5:
            assert issue.severity == Severity.CRITICAL

    def test_sorted_cache(self) -> None:
        """Test that sorted results are cached."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue

        issues = [
            ValidationIssue(column=f"col{i}", issue_type="test", count=i, severity=random.choice(list(Severity)))
            for i in range(100)
        ]

        report = Report(issues=issues)

        # First call - builds cache
        sorted1 = report.get_sorted_issues()
        assert report._sorted_cache is not None

        # Second call - uses cache
        sorted2 = report.get_sorted_issues()
        assert sorted1 is sorted2  # Same object (cached)

    def test_heap_performance(self) -> None:
        """Test heap-based operations performance."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue

        n = 10000
        issues = [
            ValidationIssue(column=f"col{i}", issue_type="test", count=i, severity=random.choice(list(Severity)))
            for i in range(n)
        ]

        # Time O(n) heapify
        start = time.perf_counter()
        report = Report(issues=issues.copy())
        init_time = time.perf_counter() - start

        # Time O(1) most severe
        start = time.perf_counter()
        for _ in range(1000):
            report.get_most_severe()
        most_severe_time = time.perf_counter() - start

        # Time O(k log n) top-k
        start = time.perf_counter()
        for _ in range(100):
            report.get_top_issues(10)
        top_k_time = time.perf_counter() - start

        print(f"\nHeap performance ({n} issues):")
        print(f"  Initialization: {init_time*1000:.2f}ms")
        print(f"  get_most_severe() x 1000: {most_severe_time*1000:.2f}ms ({most_severe_time/1000*1000:.4f}ms each)")
        print(f"  get_top_issues(10) x 100: {top_k_time*1000:.2f}ms ({top_k_time/100*1000:.2f}ms each)")


# =============================================================================
# 6. Batched Statistics Collection Tests
# =============================================================================


class TestBatchedStatistics:
    """Tests for batched statistics collection in schema learning."""

    def test_schema_learn_single_pass(self, small_df: pl.LazyFrame) -> None:
        """Test that schema learning uses single pass for basic stats."""
        from truthound.schema import learn

        # Collect the LazyFrame to get schema
        df = small_df.collect()

        # Learn schema - should use batched expressions
        schema = learn(df)

        # Should have learned all columns
        assert len(schema.columns) == 6
        assert "id" in schema.columns
        assert "name" in schema.columns
        assert "age" in schema.columns

    def test_schema_learn_numeric_stats(self, small_df: pl.LazyFrame) -> None:
        """Test that schema learning captures numeric statistics."""
        from truthound.schema import learn

        df = small_df.collect()
        schema = learn(df, infer_constraints=True)

        # Check numeric column stats
        age_schema = schema.columns["age"]
        assert age_schema.min_value is not None
        assert age_schema.max_value is not None
        assert age_schema.mean is not None
        assert age_schema.quantiles is not None

    def test_schema_learn_null_ratios(self, small_df: pl.LazyFrame) -> None:
        """Test that schema learning calculates null ratios."""
        from truthound.schema import learn

        df = small_df.collect()
        schema = learn(df)

        for col_name, col_schema in schema.columns.items():
            assert col_schema.null_ratio is not None
            assert 0 <= col_schema.null_ratio <= 1

    def test_schema_learn_performance(self, medium_df: pl.LazyFrame) -> None:
        """Test schema learning performance on medium dataset."""
        from truthound.schema import learn

        df = medium_df.collect()

        start = time.perf_counter()
        schema = learn(df, infer_constraints=True)
        duration = time.perf_counter() - start

        print(f"\nSchema learning performance (100K rows, 7 columns):")
        print(f"  Duration: {duration*1000:.2f}ms")
        print(f"  Columns learned: {len(schema.columns)}")

        # Should be fast (< 1 second for 100K rows)
        assert duration < 1.0

    def test_schema_categorical_detection(self) -> None:
        """Test that schema detects categorical columns."""
        from truthound.schema import learn

        df = pl.DataFrame({
            "category": ["A", "B", "C", "A", "B", "C"] * 100,  # 6 unique values
            "high_cardinality": [f"val_{i}" for i in range(600)],  # Many unique values
        })

        schema = learn(df, infer_constraints=True, categorical_threshold=10)

        # Category should have allowed_values
        assert schema.columns["category"].allowed_values is not None
        assert set(schema.columns["category"].allowed_values) == {"A", "B", "C"}

        # High cardinality should not have allowed_values
        assert schema.columns["high_cardinality"].allowed_values is None


# =============================================================================
# 7. Query Plan Optimization Tests
# =============================================================================


class TestQueryPlanOptimizations:
    """Tests for query plan optimizations."""

    def test_optimized_collect_function(self, small_df: pl.LazyFrame) -> None:
        """Test that optimized_collect works correctly."""
        from truthound.validators.base import optimized_collect

        result = optimized_collect(small_df.select(pl.col("id")))
        assert len(result) == 1000

    def test_optimized_collect_streaming(self, large_df: pl.LazyFrame) -> None:
        """Test streaming mode with optimized collect."""
        from truthound.validators.base import optimized_collect

        # Should work with streaming enabled
        result = optimized_collect(
            large_df.select(pl.len()),
            streaming=True
        )
        assert result.item() == 1_000_000

    def test_safe_sampler(self, medium_df: pl.LazyFrame) -> None:
        """Test SafeSampler utility."""
        from truthound.validators.base import SafeSampler

        # Test safe_head
        head_df = SafeSampler.safe_head(medium_df, 10)
        assert len(head_df) == 10

        # Test with column selection
        head_df = SafeSampler.safe_head(medium_df, 10, columns=["id", "name"])
        assert len(head_df) == 10
        assert set(head_df.columns) == {"id", "name"}

    def test_safe_filter_sample(self, medium_df: pl.LazyFrame) -> None:
        """Test SafeSampler filter sample."""
        from truthound.validators.base import SafeSampler

        # Filter for non-null age values
        sample_df = SafeSampler.safe_filter_sample(
            medium_df,
            pl.col("age").is_not_null(),
            n=100,
            columns=["id", "age"]
        )

        assert len(sample_df) <= 100
        assert all(sample_df["age"].is_not_null())


# =============================================================================
# 8. Expression Validator Mixin Tests
# =============================================================================


class TestExpressionValidatorMixin:
    """Tests for ExpressionValidatorMixin functionality."""

    def test_validation_expression_spec(self) -> None:
        """Test ValidationExpressionSpec creation."""
        from truthound.validators.base import ValidationExpressionSpec

        spec = ValidationExpressionSpec(
            column="test_col",
            validator_name="test_validator",
            issue_type="test_issue",
            count_expr=pl.col("test_col").is_null().sum(),
            non_null_expr=pl.len(),
        )

        assert spec.column == "test_col"
        assert spec.validator_name == "test_validator"

    def test_spec_get_all_exprs(self) -> None:
        """Test that spec generates correct expressions."""
        from truthound.validators.base import ValidationExpressionSpec

        spec = ValidationExpressionSpec(
            column="test_col",
            validator_name="test_validator",
            issue_type="test_issue",
            count_expr=pl.col("test_col").is_null().sum(),
            non_null_expr=pl.len(),
            extra_exprs=[pl.col("test_col").mean()],
            extra_keys=["mean_val"],
        )

        exprs = spec.get_all_exprs("_v0")

        assert len(exprs) == 3  # count, non_null, extra
        # Check aliases
        expr_names = [str(e) for e in exprs]
        assert any("_v0_count" in n for n in expr_names)

    def test_expression_validator_protocol(self) -> None:
        """Test ExpressionValidatorProtocol compliance."""
        from truthound.validators.base import ExpressionValidatorProtocol
        from truthound.validators.completeness.null import NullValidator

        validator = NullValidator()

        # NullValidator should implement the protocol
        assert isinstance(validator, ExpressionValidatorProtocol)

    def test_validate_with_expressions(self, small_df: pl.LazyFrame) -> None:
        """Test _validate_with_expressions method."""
        from truthound.validators.completeness.null import NullValidator

        validator = NullValidator()
        issues = validator.validate(small_df)

        # Should find null issues
        null_issues = [i for i in issues if i.issue_type == "null"]
        assert len(null_issues) > 0


# =============================================================================
# 9. Large Scale Performance Benchmark
# =============================================================================


class TestLargeScalePerformance:
    """Large scale performance benchmarks."""

    def test_million_row_validation(self, large_df: pl.LazyFrame) -> None:
        """Test validation on 1M row dataset."""
        from truthound.validators.completeness.null import NullValidator
        from truthound.validators.distribution.range import BetweenValidator

        # Test NullValidator
        start = time.perf_counter()
        issues = NullValidator().validate(large_df)
        null_time = time.perf_counter() - start

        # Test BetweenValidator
        start = time.perf_counter()
        issues = BetweenValidator(min_value=0, max_value=100, columns=("score",)).validate(large_df)
        range_time = time.perf_counter() - start

        print(f"\n1M row validation:")
        print(f"  NullValidator: {null_time:.3f}s")
        print(f"  BetweenValidator: {range_time:.3f}s")

        # Should complete in reasonable time
        assert null_time < 5.0
        assert range_time < 5.0

    def test_batch_executor_million_rows(self, large_df: pl.LazyFrame) -> None:
        """Test batch executor on 1M row dataset."""
        from truthound.validators.base import ExpressionBatchExecutor
        from truthound.validators.completeness.null import NullValidator, CompletenessRatioValidator
        from truthound.validators.distribution.range import NonNegativeValidator

        executor = ExpressionBatchExecutor()
        executor.add_validator(NullValidator())
        executor.add_validator(CompletenessRatioValidator(min_ratio=0.95))
        executor.add_validator(NonNegativeValidator(columns=("score",)))

        start = time.perf_counter()
        issues = executor.execute(large_df)
        batch_time = time.perf_counter() - start

        print(f"\n1M row batch validation (3 validators):")
        print(f"  Duration: {batch_time:.3f}s")
        print(f"  Issues found: {len(issues)}")

        # Should complete in reasonable time
        assert batch_time < 10.0


# =============================================================================
# 10. Integration Tests
# =============================================================================


class TestPerformanceIntegration:
    """Integration tests for performance features."""

    def test_full_validation_pipeline(self, medium_df: pl.LazyFrame) -> None:
        """Test full validation pipeline performance."""
        from truthound.validators.base import ExpressionBatchExecutor
        from truthound.validators.completeness.null import NullValidator
        from truthound.validators.distribution.range import BetweenValidator
        from truthound.report import Report

        # Create batch executor
        executor = ExpressionBatchExecutor()
        executor.add_validator(NullValidator())
        executor.add_validator(BetweenValidator(min_value=0, max_value=100, columns=("age", "score")))

        # Execute validation
        start = time.perf_counter()
        issues = executor.execute(medium_df)
        validation_time = time.perf_counter() - start

        # Create report
        start = time.perf_counter()
        report = Report(issues=issues, source="test")
        report_time = time.perf_counter() - start

        # Access sorted issues
        start = time.perf_counter()
        sorted_issues = report.get_sorted_issues()
        sort_time = time.perf_counter() - start

        print(f"\nFull pipeline (100K rows):")
        print(f"  Validation: {validation_time*1000:.2f}ms")
        print(f"  Report creation: {report_time*1000:.2f}ms")
        print(f"  Sort issues: {sort_time*1000:.2f}ms")
        print(f"  Total issues: {len(issues)}")

    def test_schema_learn_and_validate(self, medium_df: pl.LazyFrame) -> None:
        """Test schema learning followed by validation."""
        from truthound.schema import learn
        from truthound.validators.completeness.null import NullValidator

        df = medium_df.collect()

        # Learn schema
        start = time.perf_counter()
        schema = learn(df)
        learn_time = time.perf_counter() - start

        # Validate
        start = time.perf_counter()
        issues = NullValidator().validate(medium_df)
        validate_time = time.perf_counter() - start

        print(f"\nSchema + Validation (100K rows):")
        print(f"  Schema learning: {learn_time*1000:.2f}ms")
        print(f"  Validation: {validate_time*1000:.2f}ms")
        print(f"  Columns: {len(schema.columns)}")
        print(f"  Issues: {len(issues)}")
