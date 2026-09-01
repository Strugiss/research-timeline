"""Tests for research-timeline CLI (typer-based)."""

import json
import os
import tempfile

from typer.testing import CliRunner

from research_timeline.cli import app

runner = CliRunner()


def _tmp_path():
    tmp = tempfile.mkdtemp()
    return os.path.join(tmp, "tl.json")


def _init(path):
    return runner.invoke(app, [
        "init",
        "--name", "Test Project",
        "--desc", "Test description",
        "--domain", "quantum",
        "--author", "Test Author",
        "--affiliation", "independent",
        "--output", path,
    ])


def test_init_creates_timeline():
    path = _tmp_path()
    result = _init(path)
    assert result.exit_code == 0
    assert os.path.exists(path)
    data = json.load(open(path, encoding="utf-8"))
    assert data["project"]["name"] == "Test Project"
    assert data["events"] == []


def test_log_then_list():
    path = _tmp_path()
    _init(path)
    r = runner.invoke(app, [
        "log", "T0", "--type", "T0",
        "--desc", "First AI interaction", "--tags", "setup,theory",
        "--file", path,
    ])
    assert r.exit_code == 0
    r2 = runner.invoke(app, ["list", "--file", path])
    assert r2.exit_code == 0
    assert "T0" in r2.stdout


def test_log_metrics_and_evidence():
    path = _tmp_path()
    _init(path)
    r = runner.invoke(app, [
        "log", "T1", "--type", "T1",
        "--desc", "First QPU run", "--z-combined", "50.0",
        "--z-score", "12.5", "--shots", "8192", "--backend", "ibm_kingston",
        "--job-ids", "abc,def", "--git-commit", "c3ddc4a",
        "--tags", "qpu", "--file", path,
    ])
    assert r.exit_code == 0
    data = json.load(open(path, encoding="utf-8"))
    event = data["events"][0]
    assert event["metrics"]["z_score_combined"] == 50.0
    assert event["metrics"]["shots"] == 8192
    assert event["metrics"]["backend"] == "ibm_kingston"
    assert event["evidence"]["job_ids"] == ["abc", "def"]
    assert event["evidence"]["git_commit"] == "c3ddc4a"


def test_log_valid_ids():
    path = _tmp_path()
    _init(path)
    for eid in ["T0", "T1", "Tn", "pivot", "control", "submission", "publication", "milestone"]:
        r = runner.invoke(app, [
            "log", eid, "--type", eid, "--desc", f"Test {eid}", "--file", path,
        ])
        assert r.exit_code == 0, f"{eid} should be accepted"


def test_log_invalid_id_rejected():
    path = _tmp_path()
    _init(path)
    r = runner.invoke(app, [
        "log", "X0", "--type", "T0", "--desc", "Bad", "--file", path,
    ])
    assert r.exit_code != 0


def test_log_duplicate_id_rejected():
    path = _tmp_path()
    _init(path)
    runner.invoke(app, ["log", "T0", "--type", "T0", "--desc", "First", "--file", path])
    r = runner.invoke(app, ["log", "T0", "--type", "T0", "--desc", "Dup", "--file", path])
    assert r.exit_code != 0
    assert "already exists" in r.stdout.lower()


def test_export_latex():
    path = _tmp_path()
    _init(path)
    runner.invoke(app, ["log", "T0", "--type", "T0", "--desc", "Start", "--file", path])
    r = runner.invoke(app, ["export", "--format", "latex", "--file", path])
    assert r.exit_code == 0
    assert "tabular" in r.stdout
    assert "T0" in r.stdout


def test_export_jsonld():
    path = _tmp_path()
    _init(path)
    r = runner.invoke(app, ["export", "--format", "jsonld", "--file", path])
    assert r.exit_code == 0
    assert '"@context": "https://schema.org"' in r.stdout
    assert '"@type": "ResearchProject"' in r.stdout


def test_export_html_to_file():
    path = _tmp_path()
    _init(path)
    runner.invoke(app, ["log", "Tn", "--type", "Tn", "--desc", "Discovery", "--file", path])
    out = os.path.join(os.path.dirname(path), "out.html")
    r = runner.invoke(app, ["export", "--format", "html", "--file", path, "-o", out])
    assert r.exit_code == 0
    assert os.path.exists(out)
    assert "<html>" in open(out, encoding="utf-8").read()


def test_validate_ok_and_fail():
    path = _tmp_path()
    _init(path)
    runner.invoke(app, ["log", "T0", "--type", "T0", "--desc", "Ok", "--file", path])
    r = runner.invoke(app, ["validate", "--file", path])
    assert r.exit_code == 0
    r2 = runner.invoke(app, ["validate", "--file", os.path.join(os.path.dirname(path), "none.json")])
    assert r2.exit_code != 0


def test_help():
    r = runner.invoke(app, ["--help"])
    assert r.exit_code == 0
    assert "research-timeline" in r.stdout


def test_export_csv():
    path = _tmp_path()
    _init(path)
    runner.invoke(app, ["log", "T0", "--type", "T0", "--desc", "Start", "--tags", "setup", "--file", path])
    r = runner.invoke(app, ["export", "--format", "csv", "--file", path])
    assert r.exit_code == 0
    assert "id,type,date" in r.stdout
    assert "T0" in r.stdout


def test_export_gantt():
    path = _tmp_path()
    _init(path)
    runner.invoke(app, ["log", "T0", "--type", "T0", "--desc", "Start", "--date", "2026-01-01", "--end-date", "2026-01-10", "--file", path])
    r = runner.invoke(app, ["export", "--format", "gantt", "--file", path])
    assert r.exit_code == 0
    assert "tikzpicture" in r.stdout
    assert "rectangle" in r.stdout


def test_log_end_date_stored():
    path = _tmp_path()
    _init(path)
    r = runner.invoke(app, [
        "log", "T1", "--type", "T1", "--desc", "Range",
        "--date", "2026-02-01", "--end-date", "2026-02-15", "--file", path,
    ])
    assert r.exit_code == 0
    data = json.load(open(path, encoding="utf-8"))
    assert data["events"][0]["end_date"] == "2026-02-15"


def test_stats():
    path = _tmp_path()
    _init(path)
    runner.invoke(app, ["log", "T0", "--type", "T0", "--desc", "Start", "--date", "2026-01-01", "--file", path])
    runner.invoke(app, ["log", "T1", "--type", "T1", "--desc", "Run", "--date", "2026-01-15", "--tags", "qpu", "--file", path])
    r = runner.invoke(app, ["stats", "--file", path])
    assert r.exit_code == 0
    assert "Events:      2" in r.stdout
    assert "14 days" in r.stdout
    assert "qpu" in r.stdout


def test_list_filters():
    path = _tmp_path()
    _init(path)
    runner.invoke(app, ["log", "T0", "--type", "T0", "--desc", "Start", "--date", "2026-01-01", "--tags", "setup", "--file", path])
    runner.invoke(app, ["log", "T1", "--type", "T1", "--desc", "Run", "--date", "2026-01-15", "--tags", "qpu", "--file", path])
    r = runner.invoke(app, ["list", "--file", path, "--type", "T1"])
    assert r.exit_code == 0
    assert "T1" in r.stdout
    assert "T0" not in r.stdout
    r2 = runner.invoke(app, ["list", "--file", path, "--tag", "qpu"])
    assert r2.exit_code == 0
    assert "T1" in r2.stdout
    assert "T0" not in r2.stdout
    r3 = runner.invoke(app, ["list", "--file", path, "--since", "2026-01-10"])
    assert r3.exit_code == 0
    assert "T0" not in r3.stdout