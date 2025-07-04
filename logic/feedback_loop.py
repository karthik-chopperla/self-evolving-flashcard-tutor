from datetime import datetime, timedelta
from logic.spaced_repetition import calculate_next_review_time

def update_flashcard_after_feedback(manager, card_id, correct):
    # Find the flashcard by ID
    flashcard = next((c for c in manager.flashcards if c["id"] == card_id), None)
    if not flashcard:
        return

    flashcard["last_reviewed"] = datetime.utcnow().isoformat()
    flashcard["attempts"] += 1

    if correct:
        flashcard["correct"] += 1
    else:
        flashcard["correct"] = max(flashcard["correct"] - 1, 0)  # Optional: penalize slightly

    # Calculate new next review time
    flashcard["next_review"] = calculate_next_review_time(flashcard).isoformat()

    # Save updates
    manager.save_flashcards()
