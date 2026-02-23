from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import List

DEFAULT_DB_PATH = Path("data/journey_db.json")


@dataclass
class Project:
    id: int
    name: str
    description: str
    status: str = "planned"  # planned | active | completed
    started_on: str | None = None
    completed_on: str | None = None


@dataclass
class Milestone:
    id: int
    project_id: int
    title: str
    due_on: str | None = None
    done: bool = False


class JourneyDB:
    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self._write({"projects": [], "milestones": []})

    def _read(self) -> dict:
        return json.loads(self.db_path.read_text(encoding="utf-8"))

    def _write(self, payload: dict) -> None:
        self.db_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def list_projects(self) -> List[Project]:
        return [Project(**p) for p in self._read()["projects"]]

    def add_project(self, name: str, description: str) -> Project:
        payload = self._read()
        next_id = max([p["id"] for p in payload["projects"]], default=0) + 1
        project = Project(id=next_id, name=name, description=description)
        payload["projects"].append(asdict(project))
        self._write(payload)
        return project

    def update_project_status(self, project_id: int, status: str) -> Project:
        if status not in {"planned", "active", "completed"}:
            raise ValueError("Status must be one of: planned, active, completed")

        payload = self._read()
        for project in payload["projects"]:
            if project["id"] == project_id:
                project["status"] = status
                if status == "active" and not project["started_on"]:
                    project["started_on"] = str(date.today())
                if status == "completed":
                    project["completed_on"] = str(date.today())
                self._write(payload)
                return Project(**project)
        raise ValueError(f"Project with ID {project_id} was not found")

    def add_milestone(self, project_id: int, title: str, due_on: str | None = None) -> Milestone:
        payload = self._read()
        project_ids = {p["id"] for p in payload["projects"]}
        if project_id not in project_ids:
            raise ValueError(f"Project with ID {project_id} was not found")

        next_id = max([m["id"] for m in payload["milestones"]], default=0) + 1
        milestone = Milestone(id=next_id, project_id=project_id, title=title, due_on=due_on)
        payload["milestones"].append(asdict(milestone))
        self._write(payload)
        return milestone

    def mark_milestone_done(self, milestone_id: int) -> Milestone:
        payload = self._read()
        for milestone in payload["milestones"]:
            if milestone["id"] == milestone_id:
                milestone["done"] = True
                self._write(payload)
                return Milestone(**milestone)
        raise ValueError(f"Milestone with ID {milestone_id} was not found")

    def list_milestones(self, project_id: int | None = None) -> List[Milestone]:
        milestones = [Milestone(**m) for m in self._read()["milestones"]]
        if project_id is None:
            return milestones
        return [m for m in milestones if m.project_id == project_id]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="journey",
        description="Manage a coding journey with projects and milestones.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add_project = sub.add_parser("add-project", help="Create a new project")
    add_project.add_argument("name")
    add_project.add_argument("description")

    list_projects = sub.add_parser("list-projects", help="Show all projects")
    list_projects.add_argument("--status", choices=["planned", "active", "completed"])

    update_project = sub.add_parser("set-project-status", help="Update project status")
    update_project.add_argument("project_id", type=int)
    update_project.add_argument("status", choices=["planned", "active", "completed"])

    add_milestone = sub.add_parser("add-milestone", help="Create a project milestone")
    add_milestone.add_argument("project_id", type=int)
    add_milestone.add_argument("title")
    add_milestone.add_argument("--due-on")

    done_milestone = sub.add_parser("done-milestone", help="Mark milestone done")
    done_milestone.add_argument("milestone_id", type=int)

    list_milestones = sub.add_parser("list-milestones", help="Show milestones")
    list_milestones.add_argument("--project-id", type=int)

    return parser


def run(args: list[str] | None = None, db_path: Path = DEFAULT_DB_PATH) -> str:
    parser = build_parser()
    parsed = parser.parse_args(args)
    db = JourneyDB(db_path)

    if parsed.command == "add-project":
        project = db.add_project(parsed.name, parsed.description)
        return f"Created project #{project.id}: {project.name}"

    if parsed.command == "list-projects":
        projects = db.list_projects()
        if parsed.status:
            projects = [p for p in projects if p.status == parsed.status]
        if not projects:
            return "No projects found."
        return "\n".join(
            f"#{p.id} | {p.name} | {p.status} | started={p.started_on or '-'} | completed={p.completed_on or '-'}"
            for p in projects
        )

    if parsed.command == "set-project-status":
        project = db.update_project_status(parsed.project_id, parsed.status)
        return f"Project #{project.id} status updated to {project.status}."

    if parsed.command == "add-milestone":
        milestone = db.add_milestone(parsed.project_id, parsed.title, parsed.due_on)
        return f"Created milestone #{milestone.id} for project #{milestone.project_id}."

    if parsed.command == "done-milestone":
        milestone = db.mark_milestone_done(parsed.milestone_id)
        return f"Milestone #{milestone.id} marked as done."

    if parsed.command == "list-milestones":
        milestones = db.list_milestones(parsed.project_id)
        if not milestones:
            return "No milestones found."
        return "\n".join(
            f"#{m.id} | project={m.project_id} | {'done' if m.done else 'open'} | {m.title} | due={m.due_on or '-'}"
            for m in milestones
        )

    raise RuntimeError("Unknown command")


def main() -> None:
    try:
        print(run())
    except ValueError as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
