import json
from pathlib import Path
from uuid import uuid4

from app.services.evaluations.graders import grade
from app.services.evaluations.report_generator import summarize


def run_dataset(dataset: str) -> dict:
    path = Path(__file__).resolve().parents[4] / "evals" / "datasets" / f"{dataset}.json"
    prompts = json.loads(path.read_text())
    metrics = [grade(item["prompt"], {"status": "COMPLETED"}) for item in prompts]
    return {"run_id": str(uuid4()), "status": "done", "metrics": summarize(metrics)}
