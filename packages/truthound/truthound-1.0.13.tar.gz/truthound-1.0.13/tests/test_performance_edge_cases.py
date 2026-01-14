"""Edge case and stress tests for performance optimization features.

This module tests edge cases that might not be covered by regular tests:
1. Very wide DataFrames (many columns)
2. Very deep issues (high severity counts)
3. Memory pressure scenarios
4. Concurrent access patterns
5. Boundary conditions
"""

from __future__ import annotations

import random
import time
import gc
from concurrent.futures import ThreadPoolExecutor, as_completed

import polars as pl
import pytest

from truthound.types import Severity


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestExpressionBatchExecutorEdgeCases:
    """Edge cases for expression batch executor."""

    def test_wide_dataframe(self) -> None:
        """Test with many columns (100+)."""
        from truthound.validators.base import ExpressionBatchExecutor
        from truthound.validators.completeness.null import NullValidator

        # Create wide DataFrame
        n_cols = 100
        n_rows = 1000
        data = {f"col_{i}": [random.randint(0, 100) if random.random() > 0.05 else None for _ in range(n_rows)]
                for i in range(n_cols)}
        lf = pl.DataFrame(data).lazy()

        executor = ExpressionBatchExecutor()
        executor.add_validator(NullValidator())

        start = time.perf_counter()
        issues = executor.execute(lf)
        duration = time.perf_counter() - start

        print(f"\nWide DataFrame (100 cols x 1K rows):")
        print(f"  Duration: {duration*1000:.2f}ms")
        print(f"  Issues: {len(issues)}")

        # Should handle 100 columns efficiently
        assert len(issues) == n_cols  # One null issue per column expected

    def test_all_null_column(self) -> None:
        """Test column that is entirely null."""
        from truthound.validators.completeness.null import NullValidator

        lf = pl.DataFrame({
            "all_null": [None] * 1000,
            "partial_null": [None if i % 2 == 0 else i for i in range(1000)],
        }).lazy()

        validator = NullValidator()
        issues = validator.validate(lf)

        # Should report both columns
        assert len(issues) == 2
        all_null_issue = next(i for i in issues if i.column == "all_null")
        assert all_null_issue.count == 1000

    def test_no_null_columns(self) -> None:
        """Test DataFrame with no nulls."""
        from truthound.validators.completeness.null import NullValidator

        lf = pl.DataFrame({
            "a": range(1000),
            "b": ["value"] * 1000,
        }).lazy()

        validator = NullValidator()
        issues = validator.validate(lf)

        # No issues expected
        assert len(issues) == 0

    def test_mixed_types(self) -> None:
        """Test with mixed column types."""
        from truthound.validators.base import ExpressionBatchExecutor
        from truthound.validators.completeness.null import NullValidator
        from truthound.validators.distribution.range import BetweenValidator

        lf = pl.DataFrame({
            "int_col": [1, 2, 3, None, 5],
            "float_col": [1.1, 2.2, None, 4.4, 5.5],
            "str_col": ["a", "b", None, "d", "e"],
            "bool_col": [True, False, None, True, False],
            "date_col": [
                pl.date(2024, 1, 1),
                pl.date(2024, 1, 2),
                None,
                pl.date(2024, 1, 4),
                pl.date(2024, 1, 5),
            ],
        }).lazy()

        # Test NullValidator with all types
        null_validator = NullValidator()
        null_issues = null_validator.validate(lf)

        # Should find nulls in all columns
        assert len(null_issues) == 5  # One per column

        # Test BetweenValidator with numeric types only
        between_validator = BetweenValidator(
            min_value=0, max_value=10,
            columns=("int_col", "float_col")
        )
        between_issues = between_validator.validate(lf)

        # Should handle numeric columns
        assert isinstance(between_issues, list)

    def test_single_row(self) -> None:
        """Test with single row DataFrame."""
        from truthound.validators.completeness.null import NullValidator

        lf = pl.DataFrame({"a": [None], "b": [1]}).lazy()
        issues = NullValidator().validate(lf)

        # Should find null in column 'a'
        assert len(issues) == 1
        assert issues[0].column == "a"

    def test_single_column(self) -> None:
        """Test with single column DataFrame."""
        from truthound.validators.completeness.null import NullValidator

        lf = pl.DataFrame({"only_col": [1, None, 3, None, 5]}).lazy()
        issues = NullValidator().validate(lf)

        assert len(issues) == 1
        assert issues[0].count == 2


class TestLazyLoadingEdgeCases:
    """Edge cases for lazy loading."""

    def test_concurrent_loading(self) -> None:
        """Test concurrent validator loading."""
        from truthound.validators._lazy import LazyValidatorLoader, VALIDATOR_IMPORT_MAP

        loader = LazyValidatorLoader(VALIDATOR_IMPORT_MAP)
        validator_names = ["NullValidator", "BetweenValidator", "RegexValidator",
                          "UniqueValidator", "NotNullValidator"]

        results = []

        def load_validator(name):
            try:
                return loader.load(name)
            except Exception as e:
                return e

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(load_validator, name): name for name in validator_names}
            for future in as_completed(futures):
                results.append(future.result())

        # All should succeed
        assert len(results) == 5
        assert all(not isinstance(r, Exception) for r in results)

    def test_invalid_validator_name(self) -> None:
        """Test loading non-existent validator."""
        from truthound.validators._lazy import LazyValidatorLoader, VALIDATOR_IMPORT_MAP

        loader = LazyValidatorLoader(VALIDATOR_IMPORT_MAP)

        with pytest.raises(AttributeError):
            loader.load("NonExistentValidator")

    def test_module_path_error(self) -> None:
        """Test loading from invalid module path."""
        from truthound.validators._lazy import LazyValidatorLoader

        bad_map = {"BadValidator": "nonexistent.module.path"}
        loader = LazyValidatorLoader(bad_map)

        with pytest.raises(AttributeError):
            loader.load("BadValidator")


class TestCacheEdgeCases:
    """Edge cases for cache system."""

    def test_hash_collision_probability(self) -> None:
        """Test that hash collisions are rare."""
        from truthound.cache import _fast_hash

        # Generate many hashes
        n = 10000
        hashes = set()
        for i in range(n):
            h = _fast_hash(f"content_{i}_{random.random()}")
            hashes.add(h)

        # Collision rate should be very low
        collision_rate = 1 - (len(hashes) / n)
        print(f"\nHash collision rate: {collision_rate:.6%}")
        assert collision_rate < 0.001  # Less than 0.1% collisions

    def test_empty_content_hash(self) -> None:
        """Test hash of empty string."""
        from truthound.cache import _fast_hash

        h = _fast_hash("")
        assert isinstance(h, str)
        assert len(h) == 16

    def test_unicode_content_hash(self) -> None:
        """Test hash of unicode content."""
        from truthound.cache import _fast_hash

        h1 = _fast_hash("한글 테스트")
        h2 = _fast_hash("日本語テスト")
        h3 = _fast_hash("한글 테스트")

        assert isinstance(h1, str)
        assert len(h1) == 16
        assert h1 != h2  # Different content
        assert h1 == h3  # Same content


class TestReportEdgeCases:
    """Edge cases for report heap operations."""

    def test_empty_report(self) -> None:
        """Test operations on empty report."""
        from truthound.report import Report

        report = Report()

        assert report.get_most_severe() is None
        assert len(report.get_sorted_issues()) == 0
        assert len(report.get_top_issues(5)) == 0

    def test_single_issue_report(self) -> None:
        """Test report with single issue."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue

        issue = ValidationIssue(
            column="test",
            issue_type="test_type",
            count=10,
            severity=Severity.HIGH,
        )
        report = Report(issues=[issue])

        assert report.get_most_severe() == issue
        assert len(report.get_sorted_issues()) == 1
        assert len(report.get_top_issues(10)) == 1

    def test_all_same_severity(self) -> None:
        """Test report with all same severity."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue

        issues = [
            ValidationIssue(column=f"col{i}", issue_type="test", count=i, severity=Severity.MEDIUM)
            for i in range(100)
        ]
        report = Report(issues=issues)

        # All issues should be returned for get_top_issues
        top10 = report.get_top_issues(10)
        assert len(top10) == 10
        assert all(i.severity == Severity.MEDIUM for i in top10)

    def test_heap_after_clear_and_readd(self) -> None:
        """Test heap behavior after clearing and re-adding."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue

        report = Report()

        # Add initial issues
        for i in range(5):
            report.add_issue(
                ValidationIssue(column=f"col{i}", issue_type="test", count=i, severity=Severity.LOW)
            )

        assert len(report.issues) == 5
        assert len(report._issues_heap) == 5

        # Clear by creating new report (Report is immutable-ish)
        report = Report()
        assert len(report.issues) == 0

        # Re-add
        report.add_issue(
            ValidationIssue(column="new", issue_type="test", count=1, severity=Severity.CRITICAL)
        )
        assert report.get_most_severe().severity == Severity.CRITICAL


class TestMaskingEdgeCases:
    """Edge cases for masking operations."""

    def test_mask_empty_dataframe(self) -> None:
        """Test masking empty DataFrame."""
        from truthound.maskers import mask_data

        lf = pl.DataFrame({"email": []}).lazy()
        result = mask_data(lf, columns=["email"], strategy="hash")

        assert len(result) == 0

    def test_mask_all_nulls(self) -> None:
        """Test masking column with all nulls."""
        from truthound.maskers import _apply_hash

        df = pl.DataFrame({"col": [None, None, None]})
        result = _apply_hash(df, "col")

        # All should remain null
        assert all(v is None for v in result["col"])

    def test_mask_special_characters(self) -> None:
        """Test masking strings with special characters."""
        from truthound.maskers import _apply_hash, _apply_redact

        df = pl.DataFrame({
            "special": [
                "user@domain.com",
                "test<script>alert('xss')</script>",
                "path/to/file.txt",
                "中文字符",
                "emoji🎉test",
            ]
        })

        hash_result = _apply_hash(df, "special")
        assert all(len(v) == 16 for v in hash_result["special"] if v is not None)

        redact_result = _apply_redact(df, "special")
        assert all(v is not None for v in redact_result["special"])


class TestSchemaLearningEdgeCases:
    """Edge cases for schema learning."""

    def test_learn_empty_dataframe(self) -> None:
        """Test learning schema from empty DataFrame."""
        from truthound.schema import learn

        df = pl.DataFrame({"a": [], "b": []})
        schema = learn(df)

        # Should learn columns but with no stats
        assert len(schema.columns) == 2
        assert schema.row_count == 0

    def test_learn_single_value(self) -> None:
        """Test learning schema from single value columns."""
        from truthound.schema import learn

        df = pl.DataFrame({
            "constant": [42] * 100,
            "unique": list(range(100)),
        })
        schema = learn(df, infer_constraints=True)

        # Constant column
        const_schema = schema.columns["constant"]
        assert const_schema.min_value == const_schema.max_value == 42
        assert const_schema.unique_ratio == 0.01  # 1 unique / 100 rows

        # Unique column
        unique_schema = schema.columns["unique"]
        assert unique_schema.unique_ratio == 1.0

    def test_learn_with_all_nulls(self) -> None:
        """Test learning with column that is all nulls."""
        from truthound.schema import learn

        df = pl.DataFrame({
            "all_null": [None] * 100,
            "normal": list(range(100)),
        })
        schema = learn(df)

        assert schema.columns["all_null"].null_ratio == 1.0
        assert schema.columns["all_null"].nullable is True


class TestQueryPlanEdgeCases:
    """Edge cases for query plan optimization."""

    def test_optimized_collect_with_filters(self) -> None:
        """Test optimized collect with filter predicates."""
        from truthound.validators.base import optimized_collect

        n = 100_000
        lf = pl.DataFrame({
            "id": range(n),
            "value": [i % 100 for i in range(n)],
        }).lazy()

        # Filter should be pushed down
        result = optimized_collect(
            lf.filter(pl.col("value") > 50).select(pl.len())
        )
        assert result.item() < n  # Less rows after filter

    def test_optimized_collect_with_projection(self) -> None:
        """Test optimized collect with column projection."""
        from truthound.validators.base import optimized_collect

        lf = pl.DataFrame({
            "a": range(1000),
            "b": range(1000),
            "c": range(1000),
            "d": range(1000),
        }).lazy()

        # Only 'a' should be read
        result = optimized_collect(lf.select("a"))
        assert list(result.columns) == ["a"]


class TestStressScenarios:
    """Stress test scenarios."""

    def test_rapid_report_updates(self) -> None:
        """Test rapid consecutive report updates."""
        from truthound.report import Report
        from truthound.validators.base import ValidationIssue

        report = Report()

        start = time.perf_counter()
        for i in range(10000):
            report.add_issue(
                ValidationIssue(
                    column=f"col{i % 100}",
                    issue_type="test",
                    count=i,
                    severity=random.choice(list(Severity)),
                )
            )
        duration = time.perf_counter() - start

        print(f"\n10K rapid additions: {duration*1000:.2f}ms")
        assert duration < 1.0  # Should complete in under 1 second

        # Verify heap consistency
        most_severe = report.get_most_severe()
        assert most_severe is not None

    def test_memory_efficient_large_batch(self) -> None:
        """Test memory efficiency with large batch."""
        from truthound.validators.base import ExpressionBatchExecutor
        from truthound.validators.completeness.null import NullValidator

        # Force GC
        gc.collect()

        n = 500_000
        lf = pl.DataFrame({
            "a": [random.random() if random.random() > 0.01 else None for _ in range(n)],
            "b": [random.random() if random.random() > 0.02 else None for _ in range(n)],
        }).lazy()

        executor = ExpressionBatchExecutor()
        executor.add_validator(NullValidator())

        start = time.perf_counter()
        issues = executor.execute(lf)
        duration = time.perf_counter() - start

        print(f"\n500K row batch: {duration*1000:.2f}ms, {len(issues)} issues")
        assert duration < 5.0

    def test_concurrent_validations(self) -> None:
        """Test concurrent validation on different DataFrames."""
        from truthound.validators.completeness.null import NullValidator

        def validate_df(df_id: int):
            n = 10_000
            lf = pl.DataFrame({
                "col": [random.random() if random.random() > 0.05 else None for _ in range(n)]
            }).lazy()
            return len(NullValidator().validate(lf))

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(validate_df, i) for i in range(8)]
            results = [f.result() for f in as_completed(futures)]

        assert len(results) == 8
        assert all(r == 1 for r in results)  # Each should find 1 column with nulls


class TestValidatorSpecificEdgeCases:
    """Edge cases for specific validators."""

    def test_between_validator_edge_values(self) -> None:
        """Test BetweenValidator at boundary values."""
        from truthound.validators.distribution.range import BetweenValidator

        lf = pl.DataFrame({
            "value": [0.0, 100.0, 50.0, -0.0001, 100.0001, None],
        }).lazy()

        # Inclusive bounds [0, 100]
        validator = BetweenValidator(min_value=0, max_value=100, inclusive=True)
        issues = validator.validate(lf)

        # Should find 2 out of range (-0.0001, 100.0001)
        assert len(issues) == 1
        assert issues[0].count == 2

    def test_between_validator_exclusive(self) -> None:
        """Test BetweenValidator with exclusive bounds."""
        from truthound.validators.distribution.range import BetweenValidator

        lf = pl.DataFrame({
            "value": [0, 100, 50, 1, 99],
        }).lazy()

        # Exclusive bounds (0, 100)
        validator = BetweenValidator(min_value=0, max_value=100, inclusive=False)
        issues = validator.validate(lf)

        # Should find 2 (0 and 100 are out of exclusive range)
        assert len(issues) == 1
        assert issues[0].count == 2

    def test_completeness_ratio_at_threshold(self) -> None:
        """Test CompletenessRatioValidator at exact threshold."""
        from truthound.validators.completeness.null import CompletenessRatioValidator

        # 95% non-null (exactly at threshold)
        lf = pl.DataFrame({
            "col": [1] * 95 + [None] * 5,
        }).lazy()

        validator = CompletenessRatioValidator(min_ratio=0.95)
        issues = validator.validate(lf)

        # Should pass (at or above threshold)
        assert len(issues) == 0

    def test_completeness_ratio_below_threshold(self) -> None:
        """Test CompletenessRatioValidator below threshold."""
        from truthound.validators.completeness.null import CompletenessRatioValidator

        # 94% non-null (below threshold)
        lf = pl.DataFrame({
            "col": [1] * 94 + [None] * 6,
        }).lazy()

        validator = CompletenessRatioValidator(min_ratio=0.95)
        issues = validator.validate(lf)

        # Should fail
        assert len(issues) == 1
        assert issues[0].count == 6
