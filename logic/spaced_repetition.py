from datetime import datetime, timedelta
import math


def calculate_next_review_time(card):
    """
    Calculates next ideal review time for a flashcard using simplified forgetting curve.
    Returns a datetime object indicating when the card should be shown again.
    """
    base_interval = 60  # seconds

    correct = card.get("correct", 0)
    attempts = card.get("attempts", 1)
    last_reviewed = card.get("last_reviewed", None)

    # Higher correct count → longer delay
    difficulty_factor = 1 + (attempts - correct) * 0.5
    mastery_factor = max(1, correct)

    interval_seconds = base_interval * mastery_factor * difficulty_factor

    if last_reviewed:
        last_dt = datetime.fromisoformat(last_reviewed)
    else:
        last_dt = datetime.now()

    return last_dt + timedelta(seconds=interval_seconds)


def calculate_memory_score(card):
    """
    Returns a memory score between 0 and 100 based on correctness and recentness.
    """
    correct = card.get("correct", 0)
    attempts = card.get("attempts", 0)
    last_reviewed = card.get("last_reviewed")

    if attempts == 0:
        return 0

    base_score = (correct / attempts) * 100

    if last_reviewed:
        seconds_since_review = (datetime.now() - datetime.fromisoformat(last_reviewed)).total_seconds()
        decay_factor = max(0, 1 - math.log1p(seconds_since_review) / 10)
        return round(base_score * decay_factor, 2)

    return round(base_score, 2)
