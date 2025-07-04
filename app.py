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
st.caption("100% AI-powered spaced repetition learning system")

# Sidebar Input: Add New Flashcard
st.sidebar.header("➕ Add a Flashcard")
with st.sidebar.form(key="add_card"):
    q = st.text_input("Front (Question)", "")
    a = st.text_input("Back (Answer)", "")
    submitted = st.form_submit_button("Add")
    if submitted and q.strip() and a.strip():
        manager.add_flashcard(q.strip(), a.strip())
        st.sidebar.success("Flashcard added!")

# 🛠️ Admin Options
st.sidebar.markdown("---")
if st.sidebar.button("⚠️ Reset All Flashcards"):
    manager.reset_flashcards()
    st.sidebar.warning("All flashcards deleted. App will refresh.")
    st.experimental_rerun()

# Sidebar Controls
st.sidebar.markdown("---")
mode = st.sidebar.radio("📌 Mode", options=["Normal", "Focus"], index=0)
force_show = st.sidebar.checkbox("🔁 Force Show All Cards (Ignore Timing)", value=False)
show_progress = st.sidebar.checkbox("📊 Show Progress", value=True)
show_goal = st.sidebar.checkbox("🎯 Daily Goal + Motivation", value=True)

# Main Area
if show_goal:
    st.subheader("🎯 Today's Smart Goal")
    st.info(suggest_daily_goal(flashcards))
    st.success(get_motivational_phrase())

if show_progress:
    display_progress(flashcards)

quiz_interface(manager, mode=mode.lower(), force_show_all=force_show)
