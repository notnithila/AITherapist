import os
import openai
from dotenv import load_dotenv
from database import SessionLocal
from models import JournalEntry, AnalysisResult


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
    
def analyze_journal_locally(text):
    prompt = f"""
Analyze the following journal entry and return a string containing advice or recommendations based on the entry. Say "Sorry, I can't help with that right now." if the entry has anything not relevant to mood or emotion.

Journal:
{text}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a kind, concise cognitive behavioral therapist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        output = response["choices"][0]["message"]["content"]

        return output

    except Exception as e:
        print(f"Error from OpenAI: {e}")
        return "Sorry, AITherapist is down right now. Please try again later."

def save_entry(user_id, text):
    analysis_output = analyze_journal_locally(text)
    db = SessionLocal()
    try:
        journal = JournalEntry(user_id=user_id, content=text)
        db.add(journal)
        db.flush()  

        analysis = AnalysisResult(
            journal_id=journal.id,
            recommendation = analysis_output
        )
        db.add(analysis)
        db.commit()
        return journal.timestamp, analysis.recommendation
    finally:
        db.close()


def get_user_entries(user_id, time=None):
    db = SessionLocal()
    try:
        if time:
            db.query(JournalEntry).filter(JournalEntry.user_id == user_id, JournalEntry.timestamp < time).delete()
            db.commit()

        return db.query(JournalEntry).filter(JournalEntry.user_id == user_id).order_by(JournalEntry.timestamp.desc()).all()
    finally:
        db.close()