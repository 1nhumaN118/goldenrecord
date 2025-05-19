import pandas as pd
import json
import os
import joblib
import shap
import numpy as np
import matplotlib.pyplot as plt

from logic.cluster import cluster_records
from config import SESSION_DIR, OUTPUT_REPORT, UPLOAD_DIR, MODEL_PATH, SHAP_PATH

def load_input_data():
    filepath = os.path.join(UPLOAD_DIR, "customers.xlsx")
    return pd.read_excel(filepath)

def generate_report():
    df = load_input_data()
    id_to_cluster, components = cluster_records(threshold=0.8)

    df["cluster"] = df.index.map(id_to_cluster).fillna(-1).astype(int)

    golden_df = df.groupby("cluster").first().reset_index() if not df.empty else pd.DataFrame()
    cluster_df = df.sort_values("cluster")

    with open(os.path.join(SESSION_DIR, "predicted_pairs.json"), "r") as f:
        suspicious = json.load(f)
    suspicious_df = pd.DataFrame(suspicious)

    with pd.ExcelWriter(OUTPUT_REPORT, engine="openpyxl") as writer:
        golden_df.to_excel(writer, sheet_name="Golden Records", index=False)
        cluster_df.to_excel(writer, sheet_name="Clusters", index=False)
        suspicious_df.to_excel(writer, sheet_name="Suspicious Pairs", index=False)

    return OUTPUT_REPORT

def get_report_stats():
    with open(os.path.join(SESSION_DIR, "predicted_pairs.json"), "r") as f:
        suspicious = json.load(f)
    df = pd.DataFrame(suspicious)
    uncertain = (df["prob"] >= 0.4) & (df["prob"] < 0.7)
    golden_count = len(set(df["id1"]).union(df["id2"]))
    return {
        "golden_records": int(golden_count),
        "duplicates": int((df["prob"] >= 0.7).sum()),
        "low_certainty": int(uncertain.sum())
    }

def get_shap_beeswarm_plot():
    model = joblib.load(MODEL_PATH)
    explainer = joblib.load(SHAP_PATH)
    with open(os.path.join(SESSION_DIR, "record_pairs.json"), "r") as f:
        records = json.load(f)
    df = pd.DataFrame(records)
    X = df[["tfidf_sim", "embedding_sim"]]

    shap_values = explainer(X)

    plt.figure(figsize=(8, 4))
    shap.plots.beeswarm(shap_values, show=False)
    out_path = os.path.join(SESSION_DIR, "shap_beeswarm.png")
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()
    return out_path