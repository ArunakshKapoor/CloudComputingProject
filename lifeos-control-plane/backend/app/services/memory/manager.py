from app.services.memory.scorer import score_memory


def relevant_memories(memories, request_text: str):
    ranked = sorted(memories, key=lambda m: score_memory(m.key, request_text) * m.confidence, reverse=True)
    return ranked[:5]
