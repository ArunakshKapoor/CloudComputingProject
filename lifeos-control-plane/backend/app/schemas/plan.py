from pydantic import BaseModel


class PlanStep(BaseModel):
    name: str
    service: str
    action_type: str
    depends_on: list[int] = []
