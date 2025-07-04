def generate_hint(answer):
    """
    Returns a simple first-letter hint for short answers.
    Example: “Paris” → “P...”
    """
    answer = answer.strip()
    if not answer or len(answer) < 2:
        return ""

    return f"{answer[0].upper()}..."
