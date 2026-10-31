import sqlite3
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi

DB_NAME = "gym_notes.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS note_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            video_title TEXT,
            full_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def fetch_and_process_youtube(video_id: str, session_id: str, api_key: str):
    init_db()
    client = genai.Client(api_key=api_key)
    
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return False

    full_transcript_text = " ".join([item['text'] for item in transcript_list])

    prompt = f"""
    You are an elite technical note-taking partner. Review this full video transcript and synthesize comprehensive, structured study notes.
    
    Structure your notes cleanly using markdown headers (#, ##, ###) and bullet points:
    1. Executive Summary / Overview
    2. Key Concepts & Architectural Logic
    3. Important Definitions & Details

    Full Transcript:
    {full_transcript_text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        synthesized_notes = response.text
    except Exception as e:
        print(f"Error generating content from Gemini: {e}")
        return False

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = """
        INSERT INTO note_sessions (session_id, video_title, full_notes) 
        VALUES (?, ?, ?)
    """
    cursor.execute(query, (session_id, f"YouTube Video {video_id}", synthesized_notes))
    conn.commit()

    cursor.close()
    conn.close()
    return True