from datetime import datetime
from logic.spaced_repetition import calculate_memory_score

def get_next_flashcard(flashcards, mode="normal", force_all=False):
    now = datetime.utcnow()

    candidates = []
    for card in flashcards:
        # Show if due or forced
        if force_all or card["last_reviewed"] is None or now >= datetime.fromisoformat(card["next_review"]):
            candidates.append(card)

    if mode == "focus":
        candidates = [c for c in candidates if calculate_memory_score(c) < 50]

    if not candidates:
        return None

    candidates.sort(key=lambda c: calculate_memory_score(c))
    return candidates[0]

def prioritize_flashcards(flashcards, mode="normal"):
    now = datetime.utcnow()

    def is_due(card):
        return card["last_reviewed"] is None or now >= datetime.fromisoformat(card["next_review"])

    if mode == "focus":
        flashcards = [c for c in flashcards if calculate_memory_score(c) < 50]

    return sorted(
        flashcards,
        key=lambda c: (
            not is_due(c),
            calculate_memory_score(c)
        )
    )
