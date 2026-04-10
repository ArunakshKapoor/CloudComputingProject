import json
from pathlib import Path


def load_seed_rules() -> list[dict]:
    path = Path(__file__).resolve().parents[2] / "seed" / "policies.json"
    return json.loads(path.read_text())
