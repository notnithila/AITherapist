import streamlit as st
from database import init_db
from logic import save_entry, get_user_entries
import datetime

init_db()

if "cleared_entries" not in st.session_state:
    st.session_state.clear_timestamp = datetime.datetime.min

st.title("🧠 AI Therapist")
user_id = 12345 

journal_text = st.text_area("Write your journal entry here:", height=200)

if st.button("Submit Entry"):
    if journal_text.strip():
        journal, analysis = save_entry(user_id, journal_text)
        st.success("Entry analyzed and saved!")
        st.subheader("🧠 My Recommendation")
        st.write(analysis)

    else:
        st.error("Please write something before submitting.")




st.subheader("🗂️ Your Past Entries")

if st.button("Clear Past Entries"):
    st.session_state.clear_timestamp = datetime.datetime.now()

entries = get_user_entries(user_id, time=st.session_state.clear_timestamp)

if not entries:
        st.markdown("***No past entries.***")
else:
    for entry in entries:
        st.markdown(f"**{entry.timestamp.strftime('%Y-%m-%d')}** — {entry.content}")