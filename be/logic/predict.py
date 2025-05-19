import pandas as pd
import joblib
import json
import os
import shap
from config import MODEL_PATH, SESSION_DIR, UPLOAD_DIR, SHAP_PATH

def run_prediction():
    pair_file = os.path.join(SESSION_DIR, "record_pairs.json")
    if not os.path.exists(pair_file):
        raise FileNotFoundError("record_pairs.json not found. Run pairgen first.")

    with open(pair_file, "r") as f:
        pairs = json.load(f)

    df = pd.read_excel(os.path.join(UPLOAD_DIR, "customers.xlsx"))
    model = joblib.load(MODEL_PATH)
    X = pd.DataFrame(pairs)[["tfidf_sim", "embedding_sim"]]
    preds = model.predict_proba(X)[:, 1]

    for i, p in enumerate(pairs):
        p["prob"] = round(float(preds[i]), 4)
        p["entity1"] = df.iloc[p["id1"]].to_dict()
        p["entity2"] = df.iloc[p["id2"]].to_dict()

    pred_path = os.path.join(SESSION_DIR, "predicted_pairs.json")
    with open(pred_path, "w") as f:
        json.dump(pairs, f, indent=2)

    # Save SHAP explainer
    explainer = shap.Explainer(model)
    joblib.dump(explainer, SHAP_PATH)

    suspicious = [p for p in pairs if 0.4 <= p["prob"] < 0.7]

    return {
        "all_pairs": pairs,
        "suspicious_pairs": suspicious
    }