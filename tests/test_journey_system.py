from pathlib import Path

from src.journey_system import run


def test_project_and_milestone_flow(tmp_path: Path) -> None:
    db_file = tmp_path / "db.json"

    msg = run(["add-project", "Portfolio", "Build and deploy portfolio"], db_file)
    assert "Created project #1" in msg

    msg = run(["set-project-status", "1", "active"], db_file)
    assert "updated to active" in msg

    msg = run(["add-milestone", "1", "Deploy first version", "--due-on", "2026-02-01"], db_file)
    assert "Created milestone #1" in msg

    msg = run(["done-milestone", "1"], db_file)
    assert "marked as done" in msg

    projects = run(["list-projects"], db_file)
    assert "Portfolio" in projects
    assert "active" in projects

    milestones = run(["list-milestones", "--project-id", "1"], db_file)
    assert "done" in milestones


def test_missing_project_error(tmp_path: Path) -> None:
    db_file = tmp_path / "db.json"

    try:
        run(["add-milestone", "88", "Ghost milestone"], db_file)
    except ValueError as exc:
        assert "was not found" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing project")
