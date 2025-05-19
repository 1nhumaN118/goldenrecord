import os

UPLOAD_DIR = "data/uploads"
SESSION_DIR = "data/session"
MODEL_PATH = "model/trained_model.pkl"
SHAP_PATH = "model/shap_explainer.pkl"
OUTPUT_REPORT = "output/golden_record.xlsx"
SUSPICIOUS_PAIRS = "output/suspicious_pairs.csv"

IDENTIFIER_KEY = "First Name"  # Default; can be updated by frontend