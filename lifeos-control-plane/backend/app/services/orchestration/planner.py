from app.config import settings
from app.services.orchestration.provider import MockPlannerProvider


def get_planner_provider():
    # OpenAI provider can be added behind same interface.
    return MockPlannerProvider() if not settings.openai_api_key else MockPlannerProvider()
