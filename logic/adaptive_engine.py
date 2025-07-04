from logic.spaced_repetition import calculate_next_review_time, calculate_memory_score
from datetime import datetime


def prioritize_flashcards(flashcards, focus_mode=False):
    """
    Sorts flashcards by review urgency.
    If focus_mode=True, only returns struggling cards (memory_score < 50).
    """
    review_list = []

    for i, card in enumerate(flashcards):
        due_time = calculate_next_review_time(card)
        memory_score = calculate_memory_score(card)
        is_due = due_time <= datetime.now()

        if is_due and (not focus_mode or memory_score < 50):
            review_list.append((i, memory_score))

    # Sort: lowest memory score = highest priority
    sorted_list = sorted(review_list, key=lambda x: x[1])
    return [i for i, _ in sorted_list]
