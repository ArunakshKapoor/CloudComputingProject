def grade(prompt: str, result: dict) -> dict[str, float]:
    status = result.get("status", "")
    return {
        "task_completion_rate": 1.0 if status == "COMPLETED" else 0.0,
        "partial_completion_rate": 1.0 if status == "PARTIALLY_COMPLETED" else 0.0,
        "policy_correctness": 1.0,
    }
