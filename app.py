import streamlit as st
from ui.display import quiz_interface, display_progress
from data.flashcard_generator import FlashcardManager

# Initialize session state
if "manager" not in st.session_state:
    st.session_state.manager = FlashcardManager()

manager = st.session_state.manager

st.title("🧠 Self-Evolving Flashcard Tutor")
st.caption("100% AI-driven spaced repetition learning system (no APIs, no static data)")

# Sidebar: Add Flashcard
st.sidebar.header("➕ Add a Flashcard")
with st.sidebar.form(key="add_card"):
    question = st.text_input("Front (Question)")
    answer = st.text_input("Back (Answer)")
    submitted = st.form_submit_button("Add")
    if submitted and question and answer:
        manager.add_flashcard(question, answer)
        st.success("Flashcard added!")

# Sidebar: Mode Switch
st.sidebar.header("📌 Mode")
mode_option = st.sidebar.radio("Choose Review Mode", options=["Normal", "Focus"])
mode = "focus" if mode_option == "Focus" else "normal"

# Display Quiz Interface
quiz_interface(manager, mode=mode)

# Smart Goal
st.markdown("### 🎯 Today's Smart Goal")
st.markdown(f"🎯 Goal: Review all {len(manager.flashcards)} cards today!")

# Display Progress Chart
display_progress(manager.flashcards)

st.markdown("💡 Repetition creates recall. Keep going!")
