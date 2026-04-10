from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.db.models.memory import Memory
from app.db.models.policy import PolicyRule
from app.db.models.user import User
from app.db.models.workflow import Base
from app.db.session import SessionLocal, engine
from app.routers import approvals, connectors, evaluations, health, memory, policies, traces, workflows
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LifeOS Control Plane API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router, prefix="/api/v1")
app.include_router(workflows.router, prefix="/api/v1")
app.include_router(approvals.router, prefix="/api/v1")
app.include_router(traces.router, prefix="/api/v1")
app.include_router(memory.router, prefix="/api/v1")
app.include_router(policies.router, prefix="/api/v1")
app.include_router(connectors.router, prefix="/api/v1")
app.include_router(evaluations.router, prefix="/api/v1")


def seed(db: Session):
    if not db.get(User, "demo-user"):
        db.add(User(id="demo-user", name="Demo User", email="demo@example.com"))
    if db.query(PolicyRule).count() == 0:
        rules = [
            ("github.fetch_issues", "LOW", False, True, "Read-only GitHub fetch allowed"),
            ("github.summarize_repo_context", "LOW", False, True, "Read-only summary allowed"),
            ("task.create_checklist", "MEDIUM", False, True, "Checklist generation allowed"),
            ("calendar.read_availability", "LOW", False, True, "Availability read allowed"),
            ("calendar.suggest_slots", "MEDIUM", False, True, "Suggestions allowed"),
            ("email.draft", "MEDIUM", False, True, "Draft generation allowed"),
            ("email.send", "HIGH", False, False, "Sending is blocked by default"),
            ("calendar.create_event", "HIGH", True, False, "Calendar write needs approval"),
        ]
        for a, r, req, allowed, reason in rules:
            db.add(PolicyRule(action_type=a, risk_level=r, requires_approval=req, allowed=allowed, reason_template=reason))
    if db.query(Memory).count() == 0:
        db.add_all([
            Memory(id="mem-1", user_id="demo-user", key="preferred_meeting_time", value="Afternoons on weekdays", source="seed", confidence=0.95),
            Memory(id="mem-2", user_id="demo-user", key="email_tone", value="Polite and concise", source="seed", confidence=0.92),
            Memory(id="mem-3", user_id="demo-user", key="task_style", value="Checklist with short action verbs", source="seed", confidence=0.89),
        ])
    db.commit()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed(db)
    db.close()
