from fastapi import APIRouter

from app.schemas.evaluation import EvaluationRunRequest
from app.services.evaluations.dataset_runner import run_dataset

router = APIRouter(prefix="/evaluations", tags=["evaluations"])

_CACHE: dict[str, dict] = {}


@router.post("/run")
def run_eval(payload: EvaluationRunRequest):
    output = run_dataset(payload.dataset)
    _CACHE[output["run_id"]] = output
    return output


@router.get("/{run_id}")
def get_eval(run_id: str):
    return _CACHE.get(run_id, {"status": "not_found"})
