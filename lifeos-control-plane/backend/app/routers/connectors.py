from fastapi import APIRouter

from app.services.connectors.calendar_connector import CalendarConnector
from app.services.connectors.email_connector import EmailConnector
from app.services.connectors.github_connector import GitHubConnector
from app.services.connectors.task_connector import TaskConnector

router = APIRouter(prefix="/connectors", tags=["connectors"])
CONNECTORS = {
    "github": GitHubConnector(),
    "task": TaskConnector(),
    "calendar": CalendarConnector(),
    "email": EmailConnector(),
}


@router.get("")
def list_connectors():
    return [c.health_check() for c in CONNECTORS.values()]


@router.get("/status")
def status():
    return {"status": "ok", "connectors": list_connectors()}


@router.post("/{connector_name}/test")
def test_connector(connector_name: str):
    connector = CONNECTORS.get(connector_name)
    if not connector:
        return {"status": "error", "message": "unknown connector"}
    return {"status": "ok", "result": connector.simulate("test", {})}
