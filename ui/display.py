from logic.adaptive_engine import get_next_flashcard
from logic.feedback_loop import update_flashcard_feedback
from logic.hint_generator import generate_hint
import streamlit as st

def quiz_interface(manager, mode="normal", force_show_all=False):
    next_card = get_next_flashcard(manager.get_all_flashcards(), mode=mode, force_all=force_show_all)

    if next_card is None:
        st.success("🎉 No cards due for review right now.")
        return

    st.subheader("📝 Quiz Time")
    st.markdown(f"**Q:** {next_card['question']}")
    
    if st.checkbox("🔍 Show Hint"):
        st.info(f"Hint: {generate_hint(next_card['answer'])}")

    if st.button("Show Answer"):
        st.success(f"**A:** {next_card['answer']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Correct"):
            update_flashcard_feedback(manager, next_card, "correct")
            st.experimental_rerun()
    with col2:
        if st.button("❌ Incorrect"):
            update_flashcard_feedback(manager, next_card, "incorrect")
            st.experimental_rerun()
    with col3:
        if st.button("🔁 Remind Me Later"):
            update_flashcard_feedback(manager, next_card, "defer")
            st.experimental_rerun()
