# 🎧 Background AI Video Note-Taking Data Pipeline & Agent

An end-to-end data engineering pipeline and AI-driven agent designed to incrementally ingest video transcripts, synthesize technical notes with human-like contextual reasoning, store them in a relational database, and serve them via a mobile-responsive web dashboard with on-device PDF exports.

Built for seamless background learning during workouts, commutes, or deep-work sessions.

---

## 🏗️ Architecture & Data Flow

```text
[ YouTube Transcript Source ] 
           │
           ▼
[ Python Ingestion ETL Worker ] ──> (Chunking Strategy & State Tracking)
           │
           ▼
[ Gemini 2.5 Flash API ] ───────> (Agentic Synthesis & Human-Like Contextual Parsing)
           │
           ▼
[ MySQL Relational Store ] ─────> (Indexed Tables for Low-Latency Retrieval)
           │
           ▼
[ Streamlit Mobile Dashboard ] ─> (Accessible via Mobile Data via Secure Tunnel)
           │
           ▼
[ Client-Side PDF Generator ] ──> (Instant Local Device Export)
