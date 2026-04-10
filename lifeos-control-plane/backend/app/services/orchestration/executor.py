from app.services.connectors.calendar_connector import CalendarConnector
from app.services.connectors.email_connector import EmailConnector
from app.services.connectors.github_connector import GitHubConnector
from app.services.connectors.task_connector import TaskConnector


CONNECTOR_MAP = {
    "github": GitHubConnector(),
    "task": TaskConnector(),
    "calendar": CalendarConnector(),
    "email": EmailConnector(),
}


def execute_step(step, payload: dict) -> dict:
    connector = CONNECTOR_MAP[step.service]
    return connector.execute(step.action_type, payload)
