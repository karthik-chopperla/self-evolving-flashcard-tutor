import streamlit as st
from data.flashcard_generator import FlashcardManager
from ui.display import quiz_interface, display_progress
from utils.session_planner import suggest_daily_goal, get_motivational_phrase

# Initialize FlashcardManager
manager = FlashcardManager(autosave=True)
flashcards = manager.get_all_flashcards()

# Page Setup
st.set_page_config(page_title="🧠 Flashcard Tutor", layout="wide")
st.title("🧠 Self-Evolving Flashcard Tutor")
st.caption("100% AI-driven spaced repetition learning system (no APIs, no static data)")

# Sidebar Input: Add New Flashcard
st.sidebar.header("➕ Add a Flashcard")
with st.sidebar.form(key="add_card"):
    q = st.text_input("Front (Question)", "")
    a = st.text_input("Back (Answer)", "")
    submitted = st.form_submit_button("Add")
    if submitted and q.strip() and a.strip():
        manager.add_flashcard(q.strip(), a.strip())
        st.sidebar.success("Flashcard added!")

# Sidebar Options
st.sidebar.markdown("---")
mode = st.sidebar.radio("📌 Mode", options=["Normal", "Focus"], index=0)
show_progress = st.sidebar.checkbox("📊 Show Progress", value=True)
show_goal = st.sidebar.checkbox("🎯 Daily Goal + Motivation", value=True)

# Main App
if show_goal:
    st.subheader("🎯 Today's Smart Goal")
    st.info(suggest_daily_goal(flashcards))
    st.success(get_motivational_phrase())

if show_progress:
    display_progress(flashcards)

quiz_interface(manager, mode=mode.lower())
