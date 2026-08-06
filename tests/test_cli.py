"""Tests for research-timeline."""

import tempfile
from pathlib import Path
from click.testing import CliRunner

from research_timeline.cli import main, load_timeline, save_timeline, validate_timeline


def test_init_creates_file():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "timeline.yaml"
        result = runner.invoke(main, ["init", "-f", str(path)])
        assert result.exit_code == 0
        assert path.exists()
        data = load_timeline(path)
        assert "entries" in data
        assert data["entries"] == []


def test_log_adds_entry():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "timeline.yaml"
        runner.invoke(main, ["init", "-f", str(path)])
        result = runner.invoke(main, ["log", "-f", str(path), "Test entry", "-s", "completed", "-t", "tag1,tag2"])
        assert result.exit_code == 0
        data = load_timeline(path)
        assert len(data["entries"]) == 1
        assert data["entries"][0]["title"] == "Test entry"
        assert data["entries"][0]["status"] == "completed"
        assert "tag1" in data["entries"][0]["tags"]


def test_list_shows_entries():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "timeline.yaml"
        runner.invoke(main, ["init", "-f", str(path)])
        runner.invoke(main, ["log", "-f", str(path), "Entry 1", "-s", "pending"])
        runner.invoke(main, ["log", "-f", str(path), "Entry 2", "-s", "completed"])
        result = runner.invoke(main, ["list", "-f", str(path)])
        assert result.exit_code == 0
        assert "Entry 1" in result.output
        assert "Entry 2" in result.output


def test_validate_passes_on_valid():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "timeline.yaml"
        runner.invoke(main, ["init", "-f", str(path)])
        runner.invoke(main, ["log", "-f", str(path), "Valid entry", "-s", "completed"])
        result = runner.invoke(main, ["validate", "-f", str(path)])
        assert result.exit_code == 0
        assert "valid" in result.output.lower()


def test_validate_fails_on_invalid():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "timeline.yaml"
        save_timeline(path, {"entries": [{"title": "Missing date"}]} )
        result = runner.invoke(main, ["validate", "-f", str(path)])
        assert result.exit_code != 0
        assert "error" in result.output.lower()


def test_export_json():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "timeline.yaml"
        runner.invoke(main, ["init", "-f", str(path)])
        runner.invoke(main, ["log", "-f", str(path), "Test", "-s", "completed"])
        out = Path(tmp) / "out.json"
        result = runner.invoke(main, ["export", "-f", str(path), "-F", "json", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        import json
        data = json.loads(out.read_text())
        assert len(data["entries"]) == 1


def test_validate_timeline_function():
    # Valid
    errors = validate_timeline({"entries": [{"date": "2024-01-01", "title": "Test", "status": "completed"}]})
    assert errors == []
    # Missing date
    errors = validate_timeline({"entries": [{"title": "Test", "status": "completed"}]})
    assert any("date" in e for e in errors)
    # Invalid status
    errors = validate_timeline({"entries": [{"date": "2024-01-01", "title": "Test", "status": "invalid"}]})
    assert any("invalid status" in e for e in errors)