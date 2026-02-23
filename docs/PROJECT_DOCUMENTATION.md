# Project Documentation - Student Coding Journey System

## 1. Purpose
This project converts the original repository into a usable system for beginner developers who want to manage their coding journey in a structured way.

The system supports:
- Creating projects.
- Updating project status over time.
- Creating milestones for each project.
- Tracking milestone completion.

## 2. Architecture
The system is intentionally lightweight and uses only Python standard library modules.

### Components
- **CLI layer** (`run`, `build_parser`, `main`): Handles command parsing and output.
- **Data layer** (`JourneyDB`): Manages persistence to JSON file.
- **Domain models** (`Project`, `Milestone` dataclasses): Defines structured records.

## 3. Data model
Database file: `data/journey_db.json`

```json
{
  "projects": [
    {
      "id": 1,
      "name": "Portfolio",
      "description": "Build and deploy portfolio",
      "status": "active",
      "started_on": "2026-01-15",
      "completed_on": null
    }
  ],
  "milestones": [
    {
      "id": 1,
      "project_id": 1,
      "title": "Deploy v1",
      "due_on": "2026-02-01",
      "done": false
    }
  ]
}
```

## 4. Command reference
### Project commands
- `add-project <name> <description>`
- `list-projects [--status planned|active|completed]`
- `set-project-status <project_id> <planned|active|completed>`

### Milestone commands
- `add-milestone <project_id> <title> [--due-on YYYY-MM-DD]`
- `done-milestone <milestone_id>`
- `list-milestones [--project-id N]`

## 5. Error handling
The system validates:
- Invalid project/milestone IDs.
- Invalid project statuses.

When validation fails, it returns clear error messages and exits non-zero when running via CLI.

## 6. Testing strategy
Tests are written with `pytest` and validate:
- End-to-end flow for project and milestone management.
- Validation behavior for missing project references.

## 7. Future enhancements
- User authentication for multi-user support.
- Tags/priority for projects and milestones.
- Reporting dashboard (web UI).
- Export to CSV/Markdown progress reports.
