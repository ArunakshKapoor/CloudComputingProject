def aggregate_metrics(steps: list[dict]) -> dict[str, int]:
    success = sum(1 for s in steps if s.get("execution_status") == "SUCCEEDED")
    failed = sum(1 for s in steps if s.get("execution_status") == "FAILED")
    return {"step_success_count": success, "failure_count": failed}
