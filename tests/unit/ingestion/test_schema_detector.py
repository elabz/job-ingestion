from __future__ import annotations

from job_ingestion.ingestion.schema_detector import detect_schema


def test_detect_schema_returns_unknown_on_empty_input() -> None:
    assert detect_schema([]) == "unknown"


def test_detect_schema_schema_a_when_company_name_present() -> None:
    data = [
        {"id": 1, "title": "Engineer", "company_name": "Acme"},
        {"id": 2, "title": "Analyst"},
    ]
    assert detect_schema(data) == "schema_a"


def test_detect_schema_schema_b_when_employer_present() -> None:
    data = [
        {"id": 1, "title": "Engineer", "employer": "Globex"},
        {"id": 2, "title": "Analyst"},
    ]
    assert detect_schema(data) == "schema_b"


def test_detect_schema_unknown_on_tie_between_a_and_b() -> None:
    data = [
        {"company_name": "A"},
        {"employer": "B"},
    ]
    assert detect_schema(data) == "unknown"


def test_detect_schema_prefers_schema_with_higher_count() -> None:
    data_more_a = [
        {"company_name": "A"},
        {"company_name": "A2"},
        {"employer": "B"},
    ]
    assert detect_schema(data_more_a) == "schema_a"

    data_more_b = [
        {"company_name": "A"},
        {"employer": "B"},
        {"employer": "B2"},
    ]
    assert detect_schema(data_more_b) == "schema_b"
