from pydantic import BaseModel


class SimulationStepPreview(BaseModel):
    step_id: str
    preview: str
    approval_required: bool


class SimulationResult(BaseModel):
    estimated_latency_ms: int
    estimated_cost_usd: float
    side_effect_summary: str
    steps: list[SimulationStepPreview]
