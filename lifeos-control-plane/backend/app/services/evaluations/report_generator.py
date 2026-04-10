def summarize(metrics: list[dict[str, float]]) -> dict[str, float]:
    if not metrics:
        return {}
    keys = metrics[0].keys()
    return {k: round(sum(m[k] for m in metrics)/len(metrics), 3) for k in keys}
