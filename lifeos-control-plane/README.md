# LifeOS Control Plane

LifeOS Control Plane is a simulation-first, governed personal operations control plane that plans, previews, approves, executes, and audits multi-step workflows across independent services.

## Architecture summary
- **Frontend (Next.js + TypeScript + Tailwind):** Dashboard for requests, plans, approvals, trace, memory, policies, connectors, and evaluations.
- **Backend (FastAPI + SQLAlchemy + Pydantic):** Logical microservices in one app for orchestration, policy, simulation, observability, memory, connectors, evaluations.
- **Data:** SQLite by default, PostgreSQL-compatible via `DATABASE_URL`.

## Tech stack
- Frontend: Next.js App Router, React, TypeScript strict, Tailwind CSS
- Backend: FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic, pytest

## Local setup
```bash
cp .env.example .env
```

### Run backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Run frontend
```bash
cd frontend
npm install
npm run dev
```

## Env vars
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `GITHUB_TOKEN`
- `DATABASE_URL`
- `ENABLE_HIGH_RISK_ACTIONS`
- `APP_ENV`

## Seed data
Seed data is auto-loaded at backend startup for:
- Demo user (`demo-user`)
- Policy rules
- Demo memories

## Demo walkthrough
1. Open `/` and submit the recommended prompt.
2. Open workflow details at `/workflows/{id}`.
3. Run simulation, inspect preview, visit trace.
4. Handle approvals at `/workflows/{id}/approvals` if required.
5. Execute and inspect completion status + timeline.

## API summary
All APIs are under `/api/v1`. Key groups:
- health, workflows, approvals, trace, memory, policies, connectors, evaluations

## Limitations
- OpenAI planner provider is abstracted but mock-backed in this MVP.
- GitHub connector live mode is read-only and requires token.
- Frontend hooks are lightweight and can be expanded.

## Future work
- Durable task queue + retries
- richer policy DSL
- richer evaluation dashboards and export
- full OpenAI provider implementation
