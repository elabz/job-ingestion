from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any

import job_ingestion.ingestion.service as service_module
import pytest
from job_ingestion.ingestion.service import IngestionService
from job_ingestion.storage.models import ApprovalStatus, Job


@dataclass
class _Recorded:
    evaluated: list[dict[str, Any]]
    added: list[Job]


@pytest.fixture()  # type: ignore[misc]
def recorded() -> _Recorded:
    return _Recorded(evaluated=[], added=[])


@pytest.fixture(autouse=True)  # type: ignore[misc]
def patch_dependencies(monkeypatch: pytest.MonkeyPatch, recorded: _Recorded) -> None:
    # Schema detector returns fixed value and records input
    def fake_detect_schema(jobs: list[dict[str, Any]]) -> str:
        assert isinstance(jobs, list)
        return "schema_test"

    # Patch detect_schema via string target to avoid mypy attr-defined on module attrs
    monkeypatch.setattr("job_ingestion.ingestion.schema_detector.detect_schema", fake_detect_schema)

    # Fake ApprovalEngine that records evaluated jobs and alternates decisions
    class FakeApprovalEngine:
        def __init__(self, rules: list[Any] | None = None) -> None:  # noqa: ANN401
            self.rules = rules or []

        @dataclass
        class _Decision:
            approved: bool
            reasons: list[str]

        def evaluate_job(self, job: dict[str, Any]) -> Any:  # noqa: ANN401
            recorded.evaluated.append(job)
            # Approve jobs with title not containing 'reject'
            ok = "reject" not in str(job.get("title", "")).lower()
            return self._Decision(approved=ok, reasons=[] if ok else ["rule failed"])

    monkeypatch.setattr(service_module, "ApprovalEngine", FakeApprovalEngine)

    # Fake DB session machinery that records Job adds
    @contextmanager
    def fake_get_session(_session_maker: Any) -> Iterator[Any]:  # noqa: ANN401
        class _S:
            def add(self, obj: Any) -> None:  # noqa: ANN401
                assert isinstance(obj, Job)
                recorded.added.append(obj)

        yield _S()

    def fake_get_engine(_url: str) -> Any:  # noqa: ANN401
        return object()

    def fake_get_sessionmaker(_engine: Any) -> Any:  # noqa: ANN401
        return object()

    def fake_create_all(**_: Any) -> None:  # noqa: ANN401
        return None

    monkeypatch.setattr(service_module, "get_session", fake_get_session)
    monkeypatch.setattr(service_module, "get_engine", fake_get_engine)
    monkeypatch.setattr(service_module, "get_sessionmaker", fake_get_sessionmaker)
    monkeypatch.setattr(service_module.Base.metadata, "create_all", fake_create_all)  # type: ignore[attr-defined]


def test_orchestration_counts_and_persistence(recorded: _Recorded) -> None:
    svc = IngestionService()
    jobs = [
        {"title": "Approve me", "description": "d" * 25, "location": "NY"},
        {"title": "Please reject", "description": "d" * 25, "location": "SF"},
    ]

    pid = svc.ingest_batch(jobs)
    assert isinstance(pid, str) and len(pid) > 0

    status = svc.get_processing_status(pid)
    assert status["total"] == 2
    assert status["processed"] == 2
    assert status["approved"] == 1
    assert status["rejected"] == 1
    assert status["errors"] == 0
    assert status["started_at"] is not None
    assert status["finished_at"] is not None

    # DB adds recorded with expected approval status
    assert len(recorded.added) == 2
    statuses = {j.title: j.approval_status for j in recorded.added}
    assert statuses["Approve me"] == ApprovalStatus.APPROVED
    assert statuses["Please reject"] == ApprovalStatus.REJECTED

    # Approval engine saw canonical jobs
    assert len(recorded.evaluated) == 2
    assert all("external_id" in j for j in recorded.evaluated)
