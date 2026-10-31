import os
import sqlite3
import streamlit as st
from src.agent import fetch_and_process_youtube, DB_NAME

st.set_page_config(page_title="AI YouTube Note-Taking Agent", page_icon="🎥", layout="centered")

st.title("🎥 AI YouTube Note-Taking Agent")
st.markdown("Extract full video transcripts and synthesize technical notes with Gemini directly in your dashboard.")

# User Inputs
api_key = st.text_input("Enter Gemini API Key", type="password")
video_id = st.text_input("YouTube Video ID (e.g., -moW9jvvMr4)", value="")
session_id = st.text_input("Session Tag / Name", value="default_session")

# Main Action Button
if st.button("Run AI Note Agent"):
    if not api_key:
        st.error("Please enter a Gemini API Key.")
    elif not video_id:
        st.error("Please enter a YouTube Video ID.")
    elif not session_id:
        st.error("Please provide a session tag/name.")
    else:
        with st.spinner("Processing full video transcript with Gemini..."):
            success = fetch_and_process_youtube(video_id.strip(), session_id.strip(), api_key.strip())
            if success:
                st.success("Notes generated and saved successfully!")
            else:
                st.error("Failed to process video. Please check your Video ID or Gemini API key.")

# Display Current or Selected Notes
st.markdown("---")
st.subheader("📝 Synthesized Study Notes")

if os.path.exists(DB_NAME):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT session_id, video_title, created_at FROM note_sessions ORDER BY id DESC")
        sessions = cursor.fetchall()

        if sessions:
            session_options = [s[0] for s in sessions]
            selected_session = st.selectbox("Select a session to view:", session_options)
            
            if selected_session:
                cursor.execute("SELECT video_title, full_notes, created_at FROM note_sessions WHERE session_id = ? ORDER BY id DESC LIMIT 1", (selected_session,))
                row = cursor.fetchone()
                if row:
                    v_title, notes_text, created_at = row
                    st.caption(f"**Source:** {v_title} | **Saved At:** {created_at}")
                    st.markdown("---")
                    st.markdown(notes_text)
        else:
            st.info("No saved sessions found yet. Run an agent above to create one!")
        
        conn.close()
    except Exception as e:
        st.info("Ready for your first run.")
else:
    st.info("No database initialized yet. Run an agent above to get started.")