
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from models import JournalEntry  # Your ORM model for journal entries
from database import SessionLocal

# Load a Hugging Face instruct model — only needed once
def load_model():
    model_id = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_id, low_cpu_mem_usage=True)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

# Initialize the pipeline (do this once when app starts)
generator = load_model()

def analyze_journal_locally(text):
    prompt = f"""
You are a cognitive behavioral therapist. Analyze the provided journal entry and return a JSON object like this populated with a recommendation for the user:
{{
  "mental_state": "...",
  "emotional_intensity": "...",
  "cognitive_distortions": ["..."],
  "summary": "...",
  "recommendation_tags": ["..."]
}}

Journal: {text}
"""

    result = generator(prompt, max_new_tokens=512, temperature=0.7)[0]["generated_text"]

    # Extract the JSON response from the generated output
    start = result.find("{")
    end = result.rfind("}") + 1

    if start != -1 and end != -1:
        json_text = result[start:end]
    else:
        json_text = "{}"

    try:
        return json.loads(json_text)
    except Exception:
        return {
            "mental_state": "Unknown",
            "emotional_intensity": "Unknown",
            "cognitive_distortions": [],
            "summary": "Could not parse response.",
            "recommendation_tags": []
        }
    
def get_user_entries(user_id):
    db = SessionLocal()
    try:
        entries = db.query(JournalEntry).filter(JournalEntry.user_id == user_id).order_by(JournalEntry.timestamp.desc()).all()
        return entries
    finally:
        db.close()

