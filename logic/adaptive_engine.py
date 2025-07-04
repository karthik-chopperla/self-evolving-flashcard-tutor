from datetime import datetime
from logic.spaced_repetition import calculate_memory_score

def get_next_flashcard(flashcards, mode="normal", force_all=False):
    now = datetime.utcnow()

    candidates = []
    for card in flashcards:
        if force_all or card["last_reviewed"] is None or now >= datetime.fromisoformat(card["next_review"]):
            candidates.append(card)

    if mode == "focus":
        candidates = [c for c in candidates if calculate_memory_score(c) < 50]

    if not candidates:
        return None

    candidates.sort(key=lambda c: calculate_memory_score(c))
    return candidates[0]
