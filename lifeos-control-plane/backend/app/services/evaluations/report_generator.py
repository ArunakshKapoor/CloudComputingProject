def summarize(metrics: list[dict[str, float]]) -> dict[str, float]:
    if not metrics:
        return {}

    keys = metrics[0].keys()
    summary = {
        k: round(sum(m[k] for m in metrics) / len(metrics), 3)
        for k in keys
    }
    summary["sample_count"] = float(len(metrics))
    return summary
