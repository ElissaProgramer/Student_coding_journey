# Student Coding Journey

A simple, usable command-line system for planning and tracking your learning projects.

## What this system does
- Create coding projects.
- Track status (`planned`, `active`, `completed`).
- Add milestones to each project.
- Mark milestones as done.
- Persist everything in a local JSON database.

## Quick start
```bash
python -m src.journey_system add-project "Portfolio" "Build and deploy my personal portfolio"
python -m src.journey_system set-project-status 1 active
python -m src.journey_system add-milestone 1 "Deploy v1" --due-on 2026-02-01
python -m src.journey_system done-milestone 1
python -m src.journey_system list-projects
python -m src.journey_system list-milestones --project-id 1
```

The data is stored by default in:
- `data/journey_db.json`

## Run tests
```bash
pytest -q
```

## Project documentation
For more complete documentation, see:
- `docs/PROJECT_DOCUMENTATION.md`
