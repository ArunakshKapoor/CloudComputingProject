def score_memory(key: str, request_text: str) -> float:
    return 1.0 if key.lower().replace("_", " ") in request_text.lower() else 0.5
