import streamlit as st
from database import init_db
from logic import analyze_journal_locally, get_user_entries

init_db()

st.title("🧠 AI-Powered Journal Analyzer")
user_id = 1  # Simplified for now

journal_text = st.text_area("Write your journal entry here:", height=200)

if st.button("Submit Entry"):
    if journal_text.strip():
        analysis = analyze_journal_locally(journal_text)
        st.success("Entry analyzed and saved!")
        st.subheader("🧠 AI Analysis")
        st.write(f"**Mental State**: {analysis['mental_state']}")
        st.write(f"**Emotional Intensity**: {analysis['emotional_intensity']}")
        st.write(f"**Cognitive Distortions**: {analysis['cognitive_distortions']}")
        st.write(f"**Summary**: {analysis['summary']}")
        st.write(f"**Recommendations**: {analysis['recommendation_tags']}")
    else:
        st.error("Please write something before submitting.")

st.subheader("🗂️ Your Past Entries")
entries = get_user_entries(user_id)
for entry in entries:
    st.markdown(f"**{entry.timestamp.strftime('%Y-%m-%d')}** — {entry.content}")
