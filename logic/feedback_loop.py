from datetime import datetime


def update_card_on_feedback(card, is_correct):
    """
    Updates flashcard stats based on quiz result.
    """
    card["attempts"] = card.get("attempts", 0) + 1
    if is_correct:
        card["correct"] = card.get("correct", 0) + 1

    card["last_reviewed"] = datetime.now().isoformat()
