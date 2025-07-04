from logic.spaced_repetition import calculate_memory_score


def get_card_scores(flashcards):
    """
    Returns a list of tuples: (index, memory_score)
    """
    scores = []
    for i, card in enumerate(flashcards):
        score = calculate_memory_score(card)
        scores.append((i, score))
    return scores


def get_average_memory_score(flashcards):
    """
    Returns the average memory score across all cards.
    """
    if not flashcards:
        return 0.0
    scores = [calculate_memory_score(c) for c in flashcards]
    return round(sum(scores) / len(scores), 2)
