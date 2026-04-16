# LifeOS Control Plane

LifeOS Control Plane is a **simulation-first, governed Personal Assistant-as-a-Service prototype** that plans, previews, approves, executes, and audits multi-step workflows across independent services.

Rather than acting as a single opaque chatbot, the system treats a personal assistant as a **control plane** composed of logical services for orchestration, policy review, simulation, memory, observability, connectors, and evaluation.

## What the system does

Given a natural-language request, LifeOS Control Plane can:

- decompose the request into structured workflow steps
- assign risk levels and policy decisions to each step
- simulate likely outputs, latency, and cost before execution
- block or approval-gate risky actions
- execute approved steps through service connectors
- trace the workflow lifecycle end to end
- run evaluation datasets against the workflow engine

## Example behavior

### Safe workflow
A prompt such as:

> I had a project sync today. Draft a polite follow-up email, suggest two meeting slots next week based on my preferences, create a task checklist from the meeting outcome, and summarize the top open GitHub issues in the project repo.

produces a structured plan, simulation preview, and traceable execution path.

### Risky workflow
A prompt such as:

> Send an email to my professor confirming the meeting and create a calendar event for tomorrow at 9 AM.

demonstrates governance behavior:
- `email.send` is treated as high-risk and blocked by default
- `calendar.create_event` is treated as high-risk and approval-required
- the workflow can move through approvals before partial execution

This makes the platform suitable for demonstrating **governed orchestration**, not just assistant-style response generation.

## Architecture summary

The current MVP is implemented as a **single FastAPI deployment with logical microservices**:

- **Orchestration service**  
  Receives requests, retrieves relevant memory, plans structured steps, and coordinates execution.

- **Policy engine**  
  Assigns risk levels, decides whether actions are allowed, blocked, or approval-required.

- **Simulation service**  
  Produces dry-run previews, estimated latency, cost, and side-effect summaries.

- **Connector services**  
  Wrap external or mock-safe capabilities behind stable interfaces:
  - GitHub
  - Email
  - Calendar
  - Task

- **Observability service**  
  Captures workflow events, stages, timestamps, and metadata for traceability.

- **Memory service**  
  Stores user context and supports scoped retrieval for planning and execution.

- **Evaluation service**  
  Runs datasets through the workflow engine and summarizes metrics for analysis and demo.

## Current system characteristics

### Planner
The current planner is **deterministic planning**, not a fully LLM-backed planner. It uses:
- intent detection from natural-language requests
- contextual extraction for recipients, repo names, event hints, and task patterns
- memory-aware naming and decision context

This keeps the planner stable and demo-safe while still supporting non-trivial workflow generation.

### Memory-aware planning
The system uses scoped memory context during planning, so remembered values such as:
- preferred meeting time
- default email recipient
- configured repository
- default event title

can influence generated steps and connector payloads.

### Payload-aware execution
Connectors receive structured payloads including:
- request text
- action type
- repo name
- meeting preferences
- email subject/body/recipient
- event title/time hint
- memory context

This makes the connector layer realistic even when running in mock-safe mode.

## Connector modes

The current connector setup is intentionally hybrid:

| Connector | Current mode |
|---|---|
| GitHub | Mock by default, **live-readonly** when `GITHUB_TOKEN` is configured |
| Email draft | Mock-safe |
| Email send | Blocked by policy by default |
| Calendar | Mock-safe |
| Task | Mock-safe |

This design supports safer demos while still allowing selective live integration.

## Frontend

The frontend is built with **Next.js + TypeScript + Tailwind CSS** and includes pages for:

- Dashboard
- Workflow details
- Approvals
- Trace
- Memory
- Policies
- Connectors
- Evaluations
- Settings

The UI supports:
- dark/light mode
- clear workflow status presentation
- connector and evaluation summaries

## Backend

The backend is built with:

- FastAPI
- SQLAlchemy 2.0
- Pydantic v2
- Alembic
- pytest

Data defaults to SQLite but remains compatible with PostgreSQL via `DATABASE_URL`.

## Evaluation support

The project includes three evaluation datasets:

- `productivity_prompts`
- `risky_action_prompts`
- `failure_injection_prompts`

The evaluation engine runs prompts through the workflow pipeline and reports summary metrics such as:

- task completion rate
- partial completion rate
- policy correctness
- average latency
- failure recovery rate

These evaluations are still **prototype-grade**, but they are more meaningful than a purely hardcoded stub.

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
### Flow 1 - Safe Workflow
1. Open `/`
2. Submit a productivity-style prompt
3. Open workflow details
4. Run simulation
5. Inspect trace
6. Review connector and evaluation pages

### Flow 2 - Risky Workflow
1. Submit a risky prompt involving email send and calendar creation
2. Inspect blocked / approval-required steps
3. Open the approvals page
4. Approve the calendar step
5. Execute the workflow
6. Inspect trace and final status

## API summary
All APIs are under `/api/v1`. Key groups:
- health, workflows, approvals, trace, memory, policies, connectors, evaluations

## Strengths
- Clear logical service decomposition
- Meaningful risky-action governance
- Simulation-first design
- Traceability and approval flow
- Selective live-readonly GitHub support
- Usable evaluation layer

## Limitations
- The planner is still deterministic and not yet truly LLM-backed
- GitHub is the only connector with selective live-readonly support
- Calendar and email draft remain mock-safe
- Evaluation is useful for prototype benchmarking, but not yet research-grade
- Some services are logically decomposed more strongly than they are fully implemented

## Future work
- Full OpenAI-backed planner provider
- Richer policy DSL and approval reasoning
- Real calendar and email draft integrations
- Stronger memory scoring and retrieval
- Connector-specific simulation previews
- More rigorous evaluation and export tooling
- Durable task queues and retries

## Project positioning
This project should be understood as a governed, simulation-first PA control-plane prototype rather than a production-ready assistant platform.

Its main contribution is not just “an assistant UI,” but a system design that makes assistant actions:

- decomposed,
- inspectable,
- policy-aware,
- previewable,
- and traceable
