import streamlit as st
from datetime import datetime
from logic.feedback_loop import update_flashcard_after_feedback
from logic.hint_generator import generate_hint
from logic.adaptive_engine import prioritize_flashcards
from utils.memory_score import calculate_memory_score
import random

def quiz_interface(manager, mode="normal"):
    st.subheader("🧠 Flashcard Quiz")

    flashcards = manager.flashcards

    if not flashcards:
        st.info("Please add some flashcards first.")
        return

    # Prioritize which flashcards to quiz based on the mode
    prioritized_cards = prioritize_flashcards(flashcards, mode=mode)
    
    if not prioritized_cards:
        st.success("🎉 No cards due for review right now.")
        return

    # Pick the top-priority card
    card = prioritized_cards[0]
    st.markdown(f"**❓ Question:** {card['question']}")

    show_hint = st.checkbox("🔍 Show Hint")
    if show_hint:
        st.markdown(f"**Hint:** {generate_hint(card['answer'])}")

    show_answer = st.button("Show Answer")
    if show_answer:
        st.markdown(f"**✅ Answer:** {card['answer']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Correct"):
            update_flashcard_after_feedback(manager, card["id"], correct=True)
            st.experimental_rerun()
    with col2:
        if st.button("❌ Incorrect"):
            update_flashcard_after_feedback(manager, card["id"], correct=False)
            st.experimental_rerun()
    with col3:
        if st.button("🔁 Remind Me Later"):
            # Just rerun without updating
            st.experimental_rerun()

def display_progress(manager):
    flashcards = manager.flashcards
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
