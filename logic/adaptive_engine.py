from datetime import datetime
from logic.spaced_repetition import calculate_memory_score

def get_next_flashcard(flashcards, mode="normal", force_all=False):
    now = datetime.utcnow()

    candidates = []
    for card in flashcards:
        # Show if due or if forcing all
        if force_all or card["last_reviewed"] is None or now >= datetime.fromisoformat(card["next_review"]):
            candidates.append(card)

    # If in focus mode, only show low-scoring cards
    if mode == "focus":
        candidates = [c for c in candidates if calculate_memory_score(c) < 50]

    # Nothing due right now
    if not candidates:
        return None

    # Sort by lowest memory score (most urgent)
    candidates.sort(key=lambda c: calculate_memory_score(c))
    return candidates[0]

def prioritize_flashcards(flashcards, mode="normal"):
    now = datetime.utcnow()

    # Sort based on due status and score
    def is_due(card):
        return card["last_reviewed"] is None or now >= datetime.fromisoformat(card["next_review"])

    if mode == "focus":
        flashcards = [c for c in flashcards if calculate_memory_score(c) < 50]

    # Prioritize: due cards with low memory score come first
    return sorted(flashcards, key=lambda c: (
        not is_due(c),  # due cards first
        calculate_memory_score(c)  # lower score = higher priority
    ))
