import streamlit as st
from logic.hint_generator import generate_hint
from logic.feedback_loop import update_card_on_feedback
from logic.spaced_repetition import calculate_memory_score
from logic.adaptive_engine import prioritize_flashcards


def quiz_interface(manager, mode="normal"):
    """
    Displays the main quiz interface.
    :param manager: FlashcardManager object
    :param mode: "normal" or "focus"
    """
    st.subheader("🧠 Flashcard Quiz")
    flashcards = manager.get_all_flashcards()

    if not flashcards:
        st.info("No flashcards added yet. Please add some to begin!")
        return

    focus_mode = (mode == "focus")
    prioritized_indices = prioritize_flashcards(flashcards, focus_mode=focus_mode)

    if not prioritized_indices:
        st.success("🎉 No cards due for review right now.")
        return

    # Use session state to persist flashcard index and reveal state
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
        st.session_state.show_answer = False

    index = prioritized_indices[st.session_state.current_index % len(prioritized_indices)]
    card = flashcards[index]

    st.markdown(f"**Question:** {card['question']}")
    if not st.session_state.show_answer:
        if st.checkbox("🔍 Show Hint"):
            st.info(f"Hint: {generate_hint(card['answer'])}")
        if st.button("Show Answer"):
            st.session_state.show_answer = True
        return
    else:
        st.markdown(f"**Answer:** {card['answer']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Correct"):
            update_card_on_feedback(card, is_correct=True)
            manager.update_flashcard(index, card)
            st.session_state.show_answer = False
            st.session_state.current_index += 1
            st.experimental_rerun()

    with col2:
        if st.button("❌ Incorrect"):
            update_card_on_feedback(card, is_correct=False)
            manager.update_flashcard(index, card)
            st.session_state.show_answer = False
            st.session_state.current_index += 1
            st.experimental_rerun()

    with col3:
        if st.button("🔁 Remind Me Later"):
            st.session_state.show_answer = False
            st.session_state.current_index += 1
            st.experimental_rerun()


def display_progress(flashcards):
    """
    Displays a simple progress bar and pie chart.
    """
    st.subheader("📊 Learning Progress")

    total = len(flashcards)
    if total == 0:
        st.info("No flashcards to analyze.")
        return

    mastered = 0
    struggling = 0
    pending = 0

    for card in flashcards:
        score = calculate_memory_score(card)
        if card["attempts"] == 0:
            pending += 1
        elif score >= 80:
            mastered += 1
        elif score < 50:
            struggling += 1

    st.write(f"**Total Cards:** {total}")
    st.progress((mastered / total) if total else 0)

    st.write("### Breakdown:")
    st.write(f"✅ Mastered: {mastered}")
    st.write(f"⚠️ Struggling: {struggling}")
    st.write(f"🕓 Pending Review: {pending}")

    st.pyplot(_build_pie_chart(mastered, struggling, pending))


def _build_pie_chart(mastered, struggling, pending):
    import matplotlib.pyplot as plt

    labels = ["Mastered", "Struggling", "Pending"]
    sizes = [mastered, struggling, pending]
    colors = ["green", "red", "orange"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')
    ax.axis("equal")
    return fig
