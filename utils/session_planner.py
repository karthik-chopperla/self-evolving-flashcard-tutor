import random


def suggest_daily_goal(flashcards):
    """
    Suggests how many cards user should review today based on card count.
    """
    total = len(flashcards)
    if total == 0:
        return "Add some flashcards to begin!"
    elif total < 10:
        return f"🎯 Goal: Review all {total} cards today!"
    elif total < 30:
        return "🎯 Goal: Review at least 10 cards today!"
    else:
        return "🎯 Goal: Focus on 15+ high-priority cards today!"


def get_motivational_phrase():
    """
    Returns a random encouragement phrase.
    """
    phrases = [
        "🚀 Keep it up! Your brain loves this!",
        "🔥 You're training like a memory athlete!",
        "📚 Every review is one step closer to mastery.",
        "💡 Repetition creates recall. Keep going!",
        "🥇 Great job! You’re outsmarting forgetting!"
    ]
    return random.choice(phrases)
