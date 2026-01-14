#!/usr/bin/env python3
"""Comprehensive DataDocs Feature Testing Script.

This script tests all documented DataDocs features against actual implementation.
"""

import sys
import tempfile
from pathlib import Path
from datetime import datetime

# Test results tracking
RESULTS = []
PASSED = 0
FAILED = 0


def test(name: str):
    """Decorator for test functions."""
    def decorator(func):
        def wrapper():
            global PASSED, FAILED
            try:
                func()
                RESULTS.append(("PASS", name, None))
                PASSED += 1
                print(f"  ✅ {name}")
            except Exception as e:
                RESULTS.append(("FAIL", name, str(e)))
                FAILED += 1
                print(f"  ❌ {name}: {e}")
        return wrapper
    return decorator


# ============================================================
# 1. Pipeline Engine Tests
# ============================================================
print("\n" + "=" * 60)
print("1. Pipeline Engine Tests")
print("=" * 60)


@test("ReportContext creation from dict")
def test_context_from_dict():
    from truthound.datadocs.engine import ReportContext, ReportData

    data = ReportData(raw={"row_count": 100, "column_count": 5})
    ctx = ReportContext(data=data, locale="ko", theme="dark")

    assert ctx.locale == "ko"
    assert ctx.theme == "dark"
    assert ctx.data.raw["row_count"] == 100


test_context_from_dict()


@test("ReportContext.from_profile factory method")
def test_context_from_profile():
    from truthound.datadocs.engine import ReportContext

    profile = {
        "title": "Test Report",
        "row_count": 1000,
        "column_count": 10,
        "source": "test.csv"
    }

    ctx = ReportContext.from_profile(profile, locale="en", theme="professional")

    assert ctx.title == "Test Report"
    assert ctx.locale == "en"
    assert ctx.theme == "professional"
    assert ctx.metadata["row_count"] == 1000


test_context_from_profile()


@test("ReportContext immutability (fluent API)")
def test_context_immutability():
    from truthound.datadocs.engine import ReportContext, ReportData

    ctx = ReportContext(data=ReportData(), locale="en", theme="default")
    ctx2 = ctx.with_locale("ko")
    ctx3 = ctx2.with_theme("dark")

    # Original should be unchanged
    assert ctx.locale == "en"
    assert ctx.theme == "default"

    # New contexts should have updated values
    assert ctx2.locale == "ko"
    assert ctx3.theme == "dark"

    # Version should increment
    assert ctx2.version > ctx.version
    assert ctx3.version > ctx2.version


test_context_immutability()


@test("ReportContext with_trace")
def test_context_trace():
    from truthound.datadocs.engine import ReportContext, ReportData

    ctx = ReportContext(data=ReportData())
    ctx = ctx.with_trace("I18nTransformer")
    ctx = ctx.with_trace("FilterTransformer")

    assert "I18nTransformer" in ctx.trace
    assert "FilterTransformer" in ctx.trace
    assert len(ctx.trace) == 2


test_context_trace()


@test("ReportData immutable methods")
def test_report_data_immutability():
    from truthound.datadocs.engine import ReportData

    data = ReportData()
    data2 = data.with_section("overview", {"score": 95})
    data3 = data2.with_alert({"level": "warning", "message": "test"})

    # Original unchanged
    assert "overview" not in data.sections
    assert len(data.alerts) == 0

    # New data has changes
    assert data2.sections["overview"]["score"] == 95
    assert len(data3.alerts) == 1


test_report_data_immutability()


@test("PipelineBuilder basic usage")
def test_pipeline_builder():
    from truthound.datadocs.engine import PipelineBuilder, ReportContext, ReportData

    pipeline = (
        PipelineBuilder()
        .set_theme("default")
        .set_exporter("html")
        .build()
    )

    ctx = ReportContext(data=ReportData(raw={"title": "Test"}))
    result = pipeline.generate(ctx)

    assert result.success
    assert result.format == "html"
    assert isinstance(result.content, str)


test_pipeline_builder()


@test("ReportPipeline fluent API")
def test_pipeline_fluent_api():
    from truthound.datadocs.engine import ReportPipeline, ReportContext, ReportData

    pipeline = (
        ReportPipeline()
        .theme("default")
        .export_as("html")
        .with_option("page_size", "A4")
    )

    ctx = ReportContext(data=ReportData())
    result = pipeline.generate(ctx)

    assert result.success


test_pipeline_fluent_api()


@test("PipelineResult save method")
def test_pipeline_result_save():
    from truthound.datadocs.engine import ReportPipeline, ReportContext, ReportData

    pipeline = ReportPipeline().theme("default").export_as("html")
    ctx = ReportContext(data=ReportData(raw={"title": "Test"}))
    result = pipeline.generate(ctx)

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "test_report.html"
        result.save(str(path))

        assert path.exists()
        content = path.read_text()
        assert "html" in content.lower() or "<!DOCTYPE" in content


test_pipeline_result_save()


# ============================================================
# 2. i18n Tests
# ============================================================
print("\n" + "=" * 60)
print("2. i18n (Internationalization) Tests")
print("=" * 60)


@test("get_catalog returns correct locale")
def test_get_catalog():
    from truthound.datadocs.i18n import get_catalog

    catalog = get_catalog("ko")
    assert catalog.locale == "ko"

    en_catalog = get_catalog("en")
    assert en_catalog.locale == "en"


test_get_catalog()


@test("Korean catalog translations")
def test_korean_catalog():
    from truthound.datadocs.i18n import get_catalog

    catalog = get_catalog("ko")

    assert catalog.get("report.title") == "데이터 품질 보고서"
    assert catalog.get("section.overview") == "개요"
    assert catalog.get("quality.excellent") == "우수"


test_korean_catalog()


@test("15 language catalogs available")
def test_15_languages():
    from truthound.datadocs.i18n import get_supported_locales

    locales = get_supported_locales()
    expected = ["en", "ko", "ja", "zh", "de", "fr", "es", "pt", "it", "ru", "ar", "th", "vi", "id", "tr"]

    for loc in expected:
        assert loc in locales, f"Missing locale: {loc}"

    print(f"    [INFO] {len(locales)} locales available: {locales}")


test_15_languages()


@test("RTL support for Arabic")
def test_rtl_arabic():
    from truthound.datadocs.i18n import get_catalog

    catalog = get_catalog("ar")

    assert catalog.metadata.get("direction") == "rtl"
    assert catalog.get("report.title") == "تقرير جودة البيانات"


test_rtl_arabic()


@test("pluralize function - English")
def test_pluralize_english():
    from truthound.datadocs.i18n import pluralize

    assert pluralize(1, "file", "files", "en") == "1 file"
    assert pluralize(5, "file", "files", "en") == "5 files"
    assert pluralize(0, "file", "files", "en") == "0 files"


test_pluralize_english()


@test("pluralize function - Russian CLDR rules")
def test_pluralize_russian():
    from truthound.datadocs.i18n import pluralize, get_plural_category, PluralCategory

    # Russian has ONE, FEW, MANY forms
    cat1 = get_plural_category(1, "ru")
    cat2 = get_plural_category(2, "ru")
    cat5 = get_plural_category(5, "ru")
    cat21 = get_plural_category(21, "ru")
    cat22 = get_plural_category(22, "ru")

    assert cat1 == PluralCategory.ONE
    assert cat2 == PluralCategory.FEW
    assert cat5 == PluralCategory.MANY
    assert cat21 == PluralCategory.ONE
    assert cat22 == PluralCategory.FEW


test_pluralize_russian()


@test("pluralize_with_forms - multi-form languages")
def test_pluralize_with_forms():
    from truthound.datadocs.i18n import pluralize_with_forms, PluralCategory

    result = pluralize_with_forms(
        3,
        {
            "one": "{count} файл",
            "few": "{count} файла",
            "many": "{count} файлов",
            "other": "{count} файла",
        },
        "ru"
    )

    assert result == "3 файла"  # FEW form


test_pluralize_with_forms()


@test("format_number - locale-specific formatting")
def test_format_number():
    from truthound.datadocs.i18n import format_number

    result_de = format_number(1234567.89, "de")
    result_ko = format_number(1234567.89, "ko")

    assert "1" in result_de and "234" in result_de
    print(f"    [INFO] German: {result_de}, Korean: {result_ko}")


test_format_number()


@test("CatalogBuilder fluent API")
def test_catalog_builder():
    from truthound.datadocs.i18n import create_catalog_builder

    catalog = (
        create_catalog_builder("custom")
        .add("custom.key", "Custom Value")
        .add_report_section(
            title="Custom Report",
            subtitle="Test",
            summary="Summary",
            details="Details"
        )
        .add_quality_labels(
            excellent="A++",
            good="A",
            fair="B",
            poor="C",
            critical="F"
        )
        .build()
    )

    assert catalog.locale == "custom"
    assert catalog.get("custom.key") == "Custom Value"
    assert catalog.get("report.title") == "Custom Report"
    assert catalog.get("quality.excellent") == "A++"


test_catalog_builder()


@test("Catalog message with parameters")
def test_catalog_params():
    from truthound.datadocs.i18n import get_catalog

    catalog = get_catalog("en")
    result = catalog.get("alert.count", count=42)
    assert "42" in result


test_catalog_params()


# ============================================================
# 3. Theme Tests
# ============================================================
print("\n" + "=" * 60)
print("3. Theme Tests")
print("=" * 60)


@test("Built-in themes available")
def test_builtin_themes():
    from truthound.datadocs.themes import get_available_themes, get_theme

    themes = get_available_themes()
    expected = ["default", "light", "dark", "minimal", "modern", "professional"]

    for theme_name in expected:
        assert theme_name in themes, f"Missing theme: {theme_name}"
        theme = get_theme(theme_name)
        assert theme is not None


test_builtin_themes()


@test("Theme instances")
def test_theme_instances():
    from truthound.datadocs.themes import (
        LIGHT_THEME, DARK_THEME, PROFESSIONAL_THEME,
        MINIMAL_THEME, MODERN_THEME
    )

    assert LIGHT_THEME is not None
    assert DARK_THEME is not None
    assert PROFESSIONAL_THEME is not None
    assert MINIMAL_THEME is not None
    assert MODERN_THEME is not None


test_theme_instances()


@test("EnterpriseTheme basic creation")
def test_enterprise_theme_basic():
    from truthound.datadocs.themes import EnterpriseTheme

    theme = EnterpriseTheme(
        company_name="ACME Corp",
        primary_color="#FF5722",
        logo_url="https://acme.com/logo.png"
    )

    assert theme.company_name == "ACME Corp"
    assert theme.branding.company_name == "ACME Corp"
    assert theme.branding.logo_url == "https://acme.com/logo.png"


test_enterprise_theme_basic()


@test("EnterpriseTheme from_config")
def test_enterprise_theme_from_config():
    from truthound.datadocs.themes import (
        EnterpriseTheme, EnterpriseThemeConfig,
        BrandingConfig, ThemeColors
    )

    config = EnterpriseThemeConfig(
        name="acme",
        branding=BrandingConfig(
            company_name="ACME Corp",
            logo_url="https://acme.com/logo.png",
            copyright_text="© 2025 ACME Corp"
        ),
        colors=ThemeColors(primary="#1a73e8", secondary="#4f46e5")
    )

    theme = EnterpriseTheme.from_config(config)

    assert theme.company_name == "ACME Corp"
    assert theme.enterprise_config.colors.primary == "#1a73e8"


test_enterprise_theme_from_config()


@test("EnterpriseTheme customize method")
def test_enterprise_theme_customize():
    from truthound.datadocs.themes import EnterpriseTheme

    theme = EnterpriseTheme(company_name="Original Corp")
    new_theme = theme.customize(company_name="New Corp", primary="#FF0000")

    assert theme.company_name == "Original Corp"
    assert new_theme.company_name == "New Corp"


test_enterprise_theme_customize()


@test("EnterpriseTheme with_branding")
def test_enterprise_theme_with_branding():
    from truthound.datadocs.themes import EnterpriseTheme

    theme = EnterpriseTheme(company_name="Corp A")
    theme2 = theme.with_branding(
        company_name="Corp B",
        logo_url="https://corpb.com/logo.png"
    )

    assert theme2.company_name == "Corp B"
    assert theme2.branding.logo_url == "https://corpb.com/logo.png"


test_enterprise_theme_with_branding()


@test("EnterpriseTheme with_colors")
def test_enterprise_theme_with_colors():
    from truthound.datadocs.themes import EnterpriseTheme

    theme = EnterpriseTheme(primary_color="#000000")
    theme2 = theme.with_colors(primary="#FF0000", secondary="#00FF00")

    assert theme2.enterprise_config.colors.primary == "#FF0000"
    assert theme2.enterprise_config.colors.secondary == "#00FF00"


test_enterprise_theme_with_colors()


@test("Theme get_css method")
def test_theme_get_css():
    from truthound.datadocs.themes import EnterpriseTheme

    theme = EnterpriseTheme(
        company_name="Test Corp",
        primary_color="#1a73e8"
    )

    css = theme.get_css()

    assert isinstance(css, str)
    assert len(css) > 0
    print(f"    [INFO] CSS length: {len(css)} chars")


test_theme_get_css()


@test("Theme loader from dict")
def test_theme_loader_from_dict():
    from truthound.datadocs.themes import load_theme_from_dict

    config = {
        "name": "custom",
        "display_name": "Custom Theme",
        "colors": {
            "primary": "#FF5722"
        }
    }

    theme = load_theme_from_dict(config)
    assert theme is not None


test_theme_loader_from_dict()


# ============================================================
# 4. Versioning Tests (Corrected API based on actual implementation)
# ============================================================
print("\n" + "=" * 60)
print("4. Versioning Tests")
print("=" * 60)


@test("IncrementalStrategy - next_version method")
def test_incremental_strategy():
    from truthound.datadocs.versioning import IncrementalStrategy

    strategy = IncrementalStrategy()

    v1 = strategy.next_version(None)
    v2 = strategy.next_version(v1)
    v3 = strategy.next_version(v2)

    assert v1 == 1
    assert v2 == 2
    assert v3 == 3


test_incremental_strategy()


@test("SemanticStrategy - next_version and format")
def test_semantic_strategy():
    from truthound.datadocs.versioning import SemanticStrategy

    strategy = SemanticStrategy()

    v1 = strategy.next_version(None)
    formatted = strategy.format_version(v1)

    # Initial version should be 1.0.0
    assert "1.0.0" in formatted
    print(f"    [INFO] Semantic version: {formatted}")


test_semantic_strategy()


@test("TimestampStrategy - generates timestamp-based version")
def test_timestamp_strategy():
    from truthound.datadocs.versioning import TimestampStrategy

    strategy = TimestampStrategy()

    v1 = strategy.next_version(None)
    formatted = strategy.format_version(v1)

    # Should be a valid timestamp
    assert v1 > 0
    assert len(formatted) > 10  # ISO format datetime


test_timestamp_strategy()


@test("GitLikeStrategy - content-based hashing")
def test_gitlike_strategy():
    from truthound.datadocs.versioning import GitLikeStrategy

    strategy = GitLikeStrategy()

    v1 = strategy.next_version(None, metadata={"content": "test content 1"})
    v2 = strategy.next_version(v1, metadata={"content": "test content 2"})

    # Different content should produce different versions
    assert v1 != v2

    # Format should be hex
    formatted = strategy.format_version(v1)
    assert all(c in "0123456789abcdef" for c in formatted.lower())


test_gitlike_strategy()


@test("InMemoryVersionStorage - save and load")
def test_inmemory_storage():
    from truthound.datadocs.versioning import InMemoryVersionStorage, IncrementalStrategy

    storage = InMemoryVersionStorage(strategy=IncrementalStrategy())

    # Save first version
    version1 = storage.save("test_report", "<html>Version 1</html>", message="Initial")
    assert version1.version == 1

    # Save second version
    version2 = storage.save("test_report", "<html>Version 2</html>", message="Update")
    assert version2.version == 2

    # List versions
    history = storage.list_versions("test_report")
    assert len(history) == 2

    # Load version
    loaded = storage.load("test_report", 1)
    assert "Version 1" in loaded.content


test_inmemory_storage()


@test("FileVersionStorage - save and load")
def test_file_version_storage():
    from truthound.datadocs.versioning import FileVersionStorage, IncrementalStrategy

    with tempfile.TemporaryDirectory() as tmpdir:
        storage = FileVersionStorage(tmpdir, strategy=IncrementalStrategy())

        # Save
        version = storage.save("report", "<html>Test</html>", message="Test version")
        assert version is not None
        assert version.version == 1

        # Load
        loaded = storage.load("report", version.version)
        assert "<html>Test</html>" in loaded.content


test_file_version_storage()


@test("ReportDiffer - compare method with ReportVersion objects")
def test_report_differ():
    from truthound.datadocs.versioning import (
        ReportDiffer, TextDiffStrategy,
        ReportVersion, VersionInfo
    )
    from datetime import datetime

    differ = ReportDiffer(strategy=TextDiffStrategy())

    # Create mock ReportVersion objects
    old_info = VersionInfo(
        version=1,
        report_id="test",
        created_at=datetime.now(),
    )
    new_info = VersionInfo(
        version=2,
        report_id="test",
        created_at=datetime.now(),
    )

    old_version = ReportVersion(
        info=old_info,
        content="<html>\n<h1>Title</h1>\n<p>Old content</p>\n</html>",
    )
    new_version = ReportVersion(
        info=new_info,
        content="<html>\n<h1>Title</h1>\n<p>New content</p>\n<p>Additional</p>\n</html>",
    )

    result = differ.compare(old_version, new_version)

    assert result.has_changes()
    assert len(result.changes) > 0


test_report_differ()


@test("diff_versions convenience function")
def test_diff_versions_func():
    from truthound.datadocs.versioning import (
        diff_versions, ReportVersion, VersionInfo
    )
    from datetime import datetime

    old_info = VersionInfo(version=1, report_id="test", created_at=datetime.now())
    new_info = VersionInfo(version=2, report_id="test", created_at=datetime.now())

    old = ReportVersion(info=old_info, content="Line 1\nLine 2\nLine 3")
    new = ReportVersion(info=new_info, content="Line 1\nLine 2 modified\nLine 3\nLine 4")

    result = diff_versions(old, new)

    assert result.has_changes()


test_diff_versions_func()


# ============================================================
# 5. Custom Templates/Renderers Tests
# ============================================================
print("\n" + "=" * 60)
print("5. Custom Templates/Renderers Tests")
print("=" * 60)


@test("JinjaRenderer basic")
def test_jinja_renderer():
    from truthound.datadocs.renderers import JinjaRenderer

    renderer = JinjaRenderer()
    assert renderer is not None


test_jinja_renderer()


@test("StringTemplateRenderer")
def test_string_template_renderer():
    from truthound.datadocs.renderers.custom import StringTemplateRenderer
    from truthound.datadocs.engine import ReportContext, ReportData

    template = "<html><body>{{ title }}</body></html>"
    renderer = StringTemplateRenderer(template)

    data = ReportData(metadata={"title": "Test Title"})
    ctx = ReportContext(data=data)

    assert renderer is not None


test_string_template_renderer()


@test("CallableRenderer")
def test_callable_renderer():
    from truthound.datadocs.renderers.custom import CallableRenderer
    from truthound.datadocs.engine import ReportContext, ReportData

    def my_render(ctx, theme=None):
        return f"<html><title>{ctx.title}</title></html>"

    renderer = CallableRenderer(my_render)

    data = ReportData(metadata={"title": "Custom Title"})
    ctx = ReportContext(data=data)

    result = renderer.render(ctx, None)
    assert "Custom Title" in result


test_callable_renderer()


# ============================================================
# 6. Exporters Tests
# ============================================================
print("\n" + "=" * 60)
print("6. Exporters Tests")
print("=" * 60)


@test("HtmlExporter")
def test_html_exporter():
    from truthound.datadocs.exporters import HtmlExporter
    from truthound.datadocs.engine import ReportContext, ReportData

    exporter = HtmlExporter()

    html_content = "<html><body>Test</body></html>"
    ctx = ReportContext(data=ReportData())

    result = exporter.export(html_content, ctx)

    assert isinstance(result, str)
    assert "Test" in result


test_html_exporter()


@test("MarkdownExporter")
def test_markdown_exporter():
    from truthound.datadocs.exporters import MarkdownExporter
    from truthound.datadocs.engine import ReportContext, ReportData

    exporter = MarkdownExporter()

    html_content = "<html><body><h1>Title</h1><p>Content</p></body></html>"
    ctx = ReportContext(data=ReportData())

    result = exporter.export(html_content, ctx)

    assert isinstance(result, str)
    print(f"    [INFO] Markdown output length: {len(result)} chars")


test_markdown_exporter()


@test("JsonExporter")
def test_json_exporter():
    from truthound.datadocs.exporters import JsonExporter
    from truthound.datadocs.engine import ReportContext, ReportData
    import json

    exporter = JsonExporter()

    data = ReportData(
        raw={"test": "value"},
        metadata={"title": "JSON Test"}
    )
    ctx = ReportContext(data=data)

    result = exporter.export("<html></html>", ctx)

    parsed = json.loads(result)
    assert isinstance(parsed, dict)


test_json_exporter()


@test("OptimizedPdfExporter initialization")
def test_pdf_exporter_init():
    from truthound.datadocs.exporters import OptimizedPdfExporter

    try:
        exporter = OptimizedPdfExporter(chunk_size=50, parallel=True)
        assert exporter is not None
        print("    [INFO] OptimizedPdfExporter created successfully")
    except ImportError as e:
        print(f"    [INFO] weasyprint not installed: {e}")


test_pdf_exporter_init()


# ============================================================
# 7. Chart Libraries Tests
# ============================================================
print("\n" + "=" * 60)
print("7. Chart Libraries Tests")
print("=" * 60)


@test("ApexChartsRenderer available")
def test_apexcharts_renderer():
    from truthound.datadocs import ApexChartsRenderer

    renderer = ApexChartsRenderer()
    assert renderer is not None


test_apexcharts_renderer()


@test("ChartJSRenderer available")
def test_chartjs_renderer():
    from truthound.datadocs import ChartJSRenderer

    renderer = ChartJSRenderer()
    assert renderer is not None


test_chartjs_renderer()


@test("PlotlyJSRenderer available")
def test_plotly_renderer():
    from truthound.datadocs import PlotlyJSRenderer

    renderer = PlotlyJSRenderer()
    assert renderer is not None


test_plotly_renderer()


@test("SVGChartRenderer available")
def test_svg_renderer():
    from truthound.datadocs import SVGChartRenderer

    renderer = SVGChartRenderer()
    assert renderer is not None


test_svg_renderer()


@test("get_chart_renderer with ChartLibrary enum")
def test_get_chart_renderer():
    from truthound.datadocs import get_chart_renderer, ChartLibrary

    # Use enum values instead of strings
    for lib in [ChartLibrary.APEXCHARTS, ChartLibrary.CHARTJS, ChartLibrary.PLOTLY, ChartLibrary.SVG]:
        renderer = get_chart_renderer(lib)
        assert renderer is not None, f"Failed to get renderer for {lib}"


test_get_chart_renderer()


@test("CDN_URLS available")
def test_cdn_urls():
    from truthound.datadocs import CDN_URLS

    assert isinstance(CDN_URLS, dict)
    assert len(CDN_URLS) > 0
    print(f"    [INFO] CDN URLs: {list(CDN_URLS.keys())}")


test_cdn_urls()


# ============================================================
# 8. HTML Report Builder Tests
# ============================================================
print("\n" + "=" * 60)
print("8. HTML Report Builder Tests")
print("=" * 60)


@test("HTMLReportBuilder basic")
def test_html_report_builder():
    from truthound.datadocs import HTMLReportBuilder, ReportTheme

    builder = HTMLReportBuilder(theme=ReportTheme.PROFESSIONAL)
    assert builder is not None


test_html_report_builder()


@test("generate_html_report function")
def test_generate_html_report():
    from truthound.datadocs import generate_html_report

    profile = {
        "source": "test.csv",
        "row_count": 100,
        "column_count": 5,
        "columns": [
            {"name": "id", "type": "int", "null_count": 0},
            {"name": "name", "type": "str", "null_count": 5},
        ]
    }

    html = generate_html_report(profile, title="Test Report")

    assert isinstance(html, str)
    assert "Test Report" in html or "html" in html.lower()


test_generate_html_report()


@test("export_report function")
def test_export_report():
    from truthound.datadocs import export_report

    profile = {
        "source": "test.csv",
        "row_count": 100,
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "report.html"
        export_report(profile, str(path), format="html")

        assert path.exists()


test_export_report()


# ============================================================
# 9. Section Renderers Tests
# ============================================================
print("\n" + "=" * 60)
print("9. Section Renderers Tests")
print("=" * 60)


@test("Section renderers available")
def test_section_renderers():
    from truthound.datadocs import (
        OverviewSection,
        ColumnsSection,
        QualitySection,
        PatternsSection,
        DistributionSection,
        CorrelationsSection,
        RecommendationsSection,
        AlertsSection,
        CustomSection,
    )

    sections = [
        OverviewSection,
        ColumnsSection,
        QualitySection,
        PatternsSection,
        DistributionSection,
        CorrelationsSection,
        RecommendationsSection,
        AlertsSection,
        CustomSection,
    ]

    for section_class in sections:
        assert section_class is not None


test_section_renderers()


@test("get_section_renderer function")
def test_get_section_renderer():
    from truthound.datadocs import get_section_renderer, SectionType

    renderer = get_section_renderer(SectionType.OVERVIEW)
    assert renderer is not None


test_get_section_renderer()


# ============================================================
# 10. Integration Tests
# ============================================================
print("\n" + "=" * 60)
print("10. Integration Tests")
print("=" * 60)


@test("Full pipeline: Profile -> HTML Report")
def test_full_pipeline_to_html():
    from truthound.datadocs.engine import PipelineBuilder, ReportContext, ReportData
    from truthound.datadocs.themes import EnterpriseTheme

    profile_data = {
        "title": "Integration Test Report",
        "source": "test_data.csv",
        "row_count": 10000,
        "column_count": 15,
        "quality_score": 0.95,
        "columns": [
            {"name": "user_id", "type": "int", "null_count": 0, "unique_count": 10000},
            {"name": "email", "type": "str", "null_count": 50, "unique_count": 9950},
        ]
    }

    theme = EnterpriseTheme(
        company_name="Integration Test Corp",
        primary_color="#2563eb",
    )

    pipeline = (
        PipelineBuilder()
        .set_theme("default")
        .set_exporter("html")
        .build()
    )

    ctx = ReportContext.from_profile(profile_data, locale="en")
    result = pipeline.generate(ctx)

    assert result.success
    assert len(result.content) > 100

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "integration_test.html"
        result.save(str(path))

        content = path.read_text()
        assert "html" in content.lower()


test_full_pipeline_to_html()


@test("Multi-language report generation")
def test_multi_language_report():
    from truthound.datadocs.engine import PipelineBuilder, ReportContext, ReportData
    from truthound.datadocs.i18n import get_catalog

    profile = {"title": "Multi-lang Test", "row_count": 100}

    for locale in ["en", "ko", "ja", "de"]:
        ctx = ReportContext.from_profile(profile, locale=locale)
        catalog = get_catalog(locale)

        title = catalog.get("report.title")
        assert title != "report.title", f"Missing translation for {locale}"


test_multi_language_report()


@test("Theme + Exporter integration")
def test_theme_exporter_integration():
    from truthound.datadocs.engine import ReportPipeline, ReportContext, ReportData
    from truthound.datadocs.themes import EnterpriseTheme

    theme = EnterpriseTheme(
        company_name="Theme Test",
        primary_color="#FF5722"
    )

    pipeline = (
        ReportPipeline()
        .theme(theme)
        .export_as("html")
    )

    ctx = ReportContext(data=ReportData(raw={"title": "Theme Test"}))
    result = pipeline.generate(ctx)

    assert result.success


test_theme_exporter_integration()


@test("Version storage with diff")
def test_version_storage_diff_integration():
    from truthound.datadocs.versioning import (
        InMemoryVersionStorage, IncrementalStrategy,
        ReportDiffer, TextDiffStrategy
    )

    storage = InMemoryVersionStorage(strategy=IncrementalStrategy())

    # Save two versions
    v1 = storage.save("report", "<html>Version 1</html>", message="Initial")
    v2 = storage.save("report", "<html>Version 2</html>", message="Update")

    # Load and diff
    loaded_v1 = storage.load("report", v1.version)
    loaded_v2 = storage.load("report", v2.version)

    differ = ReportDiffer(strategy=TextDiffStrategy())
    result = differ.compare(loaded_v1, loaded_v2)

    assert result.has_changes()


test_version_storage_diff_integration()


# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)

print(f"\n✅ Passed: {PASSED}")
print(f"❌ Failed: {FAILED}")
print(f"📊 Total:  {PASSED + FAILED}")

if FAILED > 0:
    print("\n❌ Failed Tests:")
    for status, name, error in RESULTS:
        if status == "FAIL":
            print(f"  - {name}: {error}")

print("\n" + "=" * 60)
sys.exit(0 if FAILED == 0 else 1)
