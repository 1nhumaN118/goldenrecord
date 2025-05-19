import json
import os
import networkx as nx
from config import SESSION_DIR
from logic.feedback import load_feedback

def cluster_records(threshold=0.8):
    pred_path = os.path.join(SESSION_DIR, "predicted_pairs.json")
    if not os.path.exists(pred_path):
        raise FileNotFoundError("Run prediction first.")

    with open(pred_path, "r") as f:
        pairs = json.load(f)

    feedback = load_feedback()
    feedback_map = {(f['id1'], f['id2']): f['decision'] for f in feedback}

    G = nx.Graph()

    for pair in pairs:
        id1, id2 = pair["id1"], pair["id2"]
        decision = feedback_map.get((id1, id2)) or feedback_map.get((id2, id1))

        if decision == "Yes":
            G.add_edge(id1, id2)
        elif decision == "No":
            continue
        elif decision == "Undecided":
            continue
        else:
            if pair["prob"] >= threshold:
                G.add_edge(id1, id2)

    components = list(nx.connected_components(G))
    id_to_cluster = {}
    for cluster_id, comp in enumerate(components):
        for rid in comp:
            id_to_cluster[rid] = cluster_id

    return id_to_cluster, components