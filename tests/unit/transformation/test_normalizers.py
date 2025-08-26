import pytest

from src.job_ingestion.transformation.normalizers import (
    CompanyValidator,
    LocationNormalizer,
    SalaryNormalizer,
)


class TestLocationNormalizer:
    def test_blank_returns_none(self) -> None:
        n = LocationNormalizer()
        assert n.normalize("") is None
        assert n.normalize("   ") is None

    def test_collapses_whitespace(self) -> None:
        n = LocationNormalizer()
        assert n.normalize("  New   York   City  ") == "New York City"


class TestSalaryNormalizer:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("1200 - 3400", (1200, 3400)),
            ("50k–70k", (50_000, 70_000)),  # en-dash
            ("5000", (5000, 5000)),
            ("n/a", (None, None)),
            ("1.5M - 2M", (1_500_000, 2_000_000)),
            ("100k - 90k", (90_000, 100_000)),  # enforce ordering
        ],
    )
    def test_parse_range_basic(self, raw: str, expected: tuple[int | None, int | None]) -> None:
        n = SalaryNormalizer()
        assert n.parse_range(raw) == expected


class TestCompanyValidator:
    def test_valid_company(self) -> None:
        v = CompanyValidator()
        assert v.validate("Acme Inc.") is True

    @pytest.mark.parametrize("raw", ["", "   ", "12345", "  42  "])
    def test_invalid_company(self, raw: str) -> None:
        v = CompanyValidator()
        assert v.validate(raw) is False
