from pydantic import BaseModel


class EvaluationRunRequest(BaseModel):
    dataset: str


class EvaluationRunOut(BaseModel):
    run_id: str
    status: str
    metrics: dict[str, float]
