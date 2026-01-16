from tempfile import TemporaryDirectory

from src.models import Ticket
from src.run_manifest import RunManifest


def test_run_manifest_list_and_load():
    with TemporaryDirectory() as tmpdir:
        manifest = RunManifest(runs_directory=tmpdir)

        ticket = Ticket(
            number=101,
            title="Manifest test",
            description="Check run manifest storage",
            url="https://example.com/issues/101",
        )
        run_log = manifest.start_run(ticket)
        manifest.record_planning_start()
        manifest.complete_run(status="completed", final_summary="ok")

        other_ticket = Ticket(
            number=202,
            title="Other run",
            description="Second run",
            url="https://example.com/issues/202",
        )
        manifest.start_run(other_ticket)
        manifest.complete_run(status="completed", final_summary="ok")

        runs = manifest.list_runs(ticket_number=ticket.number)
        assert len(runs) == 1
        assert runs[0]["run_id"] == run_log.run_id
        assert runs[0]["ticket_number"] == ticket.number

        loaded = manifest.load_run(run_log.run_id)
        assert loaded is not None
        assert loaded.run_id == run_log.run_id
        assert loaded.ticket.number == ticket.number
        assert loaded.status == "completed"
