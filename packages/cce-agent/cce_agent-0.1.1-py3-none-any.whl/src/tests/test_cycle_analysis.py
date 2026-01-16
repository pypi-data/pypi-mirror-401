import json
from pathlib import Path

from src.analysis import cycle_report
from src.analysis.empirical_questions import check_empirical_questions, summarize_runs


def test_empirical_questions_summary() -> None:
    run_logs = [
        {
            "run_id": "run-1",
            "execution_cycles": [
                {"step_count": 10, "steps_in_wrap_up_phase": 2},
                {"step_count": 14, "steps_in_wrap_up_phase": 3},
            ],
        }
    ]

    summaries = summarize_runs(run_logs)
    assert summaries[0].avg_steps_per_cycle == 12.0
    assert summaries[0].avg_wrap_up_steps == 2.5

    report = check_empirical_questions(summaries)
    assert report["Q1_soft_limit"]["data_points"] == 1
    assert report["Q1_soft_limit"]["avg_steps_per_cycle"] == 12.0
    assert report["Q2_wrap_up_duration"]["avg_wrap_up_steps"] == 2.5


def test_generate_cycle_analysis_report(tmp_path: Path, monkeypatch) -> None:
    runs_dir = tmp_path / "runs"
    run_dir = runs_dir / "run-123"
    run_dir.mkdir(parents=True)

    manifest = {
        "run_id": "run-123",
        "ticket": {"number": 110, "title": "Cycle Metrics"},
        "status": "completed",
        "execution_cycles": [{"step_count": 8, "steps_in_wrap_up_phase": 2, "commit_sha": "abc"}],
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    monkeypatch.setattr(cycle_report, "get_runs_directory", lambda: runs_dir)

    output_path = tmp_path / "cycle_report.md"
    report_path = cycle_report.generate_cycle_analysis_report(output_path=output_path)

    assert report_path == output_path
    content = report_path.read_text(encoding="utf-8")
    assert "Runs analyzed: 1" in content
    assert "Total cycles: 1" in content
    assert "Total commits: 1" in content
