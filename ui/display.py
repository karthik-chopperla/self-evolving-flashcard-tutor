import streamlit as st
from datetime import datetime
from logic.feedback_loop import update_flashcard_after_feedback
from logic.hint_generator import generate_hint
from logic.adaptive_engine import prioritize_flashcards
from utils.memory_score import calculate_memory_score


def quiz_interface(manager, mode="normal"):
    st.subheader("🧠 Flashcard Quiz")

    flashcards = manager.flashcards

    if not flashcards:
        st.info("Please add some flashcards first.")
        return

    prioritized_cards = prioritize_flashcards(flashcards, mode=mode)

    if not prioritized_cards:
        st.success("🎉 No cards due for review right now.")
        return

    card = prioritized_cards[0]
    st.markdown(f"**❓ Question:** {card['question']}")

    if st.checkbox("💡 Show Hint"):
        st.markdown(f"**Hint:** {generate_hint(card['answer'])}")

    if st.button("👁️ Show Answer"):
        st.markdown(f"**✅ Answer:** {card['answer']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Correct"):
            update_flashcard_after_feedback(manager, card["id"], correct=True)
            st.rerun()

    with col2:
        if st.button("❌ Incorrect"):
            update_flashcard_after_feedback(manager, card["id"], correct=False)
            st.rerun()

    with col3:
        if st.button("🔁 Remind Me Later"):
            st.rerun()


def display_progress(flashcards):
    if not flashcards:
        st.info("No flashcards to display progress yet.")
        return

    st.subheader("📊 Progress Overview")

    mastered = sum(1 for c in flashcards if calculate_memory_score(c) >= 80)
    struggling = sum(1 for c in flashcards if calculate_memory_score(c) < 50)
    pending = len(flashcards) - mastered - struggling

    st.markdown(f"- 🧠 Mastered: **{mastered}**")
    st.markdown(f"- ⚠️ Struggling: **{struggling}**")
    st.markdown(f"- ⌛ Pending: **{pending}**")

    chart_data = {
        "Mastered": mastered,
        "Struggling": struggling,
        "Pending": pending
    }
    st.bar_chart(chart_data)
