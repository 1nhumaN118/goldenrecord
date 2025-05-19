import json
import os
from config import SESSION_DIR

FEEDBACK_PATH = os.path.join(SESSION_DIR, "feedback.json")

def save_feedback(feedback: list):
    with open(FEEDBACK_PATH, "w") as f:
        json.dump(feedback, f, indent=2)

def load_feedback():
    if not os.path.exists(FEEDBACK_PATH):
        return []
    with open(FEEDBACK_PATH, "r") as f:
        return json.load(f)