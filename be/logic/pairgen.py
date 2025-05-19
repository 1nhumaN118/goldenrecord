import pandas as pd
from itertools import combinations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os
import json
from config import SESSION_DIR

def generate_pairs(df: pd.DataFrame, identifier: str):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    df['combo'] = df['First Name'].astype(str) + ' ' + df['Email'].astype(str)
    df['embedding'] = df['combo'].apply(lambda x: model.encode(x))

    tfidf = TfidfVectorizer().fit(df['combo'])
    tfidf_matrix = tfidf.transform(df['combo'])

    pairs = []

    for i, j in combinations(range(len(df)), 2):
        r1 = df.iloc[i]
        r2 = df.iloc[j]

        tfidf_sim = cosine_similarity(tfidf_matrix[i], tfidf_matrix[j])[0][0]
        emb_sim = cosine_similarity([r1['embedding']], [r2['embedding']])[0][0]

        features = {
            "id1": int(i),
            "id2": int(j),
            "name1": str(r1[identifier]),
            "name2": str(r2[identifier]),
            "tfidf_sim": round(float(tfidf_sim), 4),
            "embedding_sim": round(float(emb_sim), 4)
        }
        pairs.append(features)

    os.makedirs(SESSION_DIR, exist_ok=True)
    with open(os.path.join(SESSION_DIR, "record_pairs.json"), "w") as f:
        json.dump(pairs, f, indent=2)

    return pairs