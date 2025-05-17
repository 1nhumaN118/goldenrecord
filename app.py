import streamlit as st
import pandas as pd
import joblib
import networkx as nx
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_auc_score

st.set_page_config(layout="wide")
st.title("🧠 GoldenRecord: Confirm & Merge")

session_state = st.session_state

uploaded_file = st.file_uploader("📥 Upload Excel file", type=["xlsx"])
if uploaded_file:
    if "df" not in session_state:
        df = pd.read_excel(uploaded_file).reset_index(drop=True)
        session_state.df = df
        session_state.model = joblib.load("src/trained_model.pkl")
        session_state.pairs_df = pd.read_csv("output/pair_scores.csv")
        df["cluster_id"] = pd.read_csv("output/cluster_mapping.csv")["cluster_id"]
        session_state.df = df

    df = session_state.df
    pairs_df = session_state.pairs_df

    st.metric("Total Records", len(df))
    threshold = st.slider("🔗 Match threshold", 0.5, 0.99, 0.85, 0.01)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if "ready_to_run" not in session_state:
            session_state.ready_to_run = False
        if st.button("Continue"):
            session_state.ready_to_run = True
            session_state.threshold = threshold

    with col_b:
        if st.button("🔄 Reset"):
            for key in list(session_state.keys()):
                del session_state[key]
            st.experimental_rerun()

    if session_state.ready_to_run:
        threshold = session_state.threshold
        uncertain = pairs_df[(pairs_df["predicted_proba"] > 0.5) & (pairs_df["predicted_proba"] < threshold)].copy()
        feedback_yes = []
        feedback_log = []

        st.subheader("📊 EDA Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(df['Gender'].value_counts())
        with col2:
            st.bar_chart(df['Country'].value_counts())
        st.bar_chart(df['City'].value_counts().head(10))
        st.subheader("📈 Birthdate Distribution")
        fig, ax = plt.subplots()
        sns.histplot(pd.to_datetime(df['Birthdate']), kde=False, bins=30, ax=ax)
        st.pyplot(fig)

        st.subheader("🧐 Confirm uncertain matches")
        for idx, row in uncertain.iterrows():
            i, j = int(row["record1_index"]), int(row["record2_index"])
            r1, r2 = df.iloc[i], df.iloc[j]
            cols = st.columns([2, 2, 1])
            with cols[0]:
                st.write(f"**Record {i}**")
                st.json(r1[["First Name", "Last Name", "Email", "Phone", "Birthdate"]].to_dict())
            with cols[1]:
                st.write(f"**Record {j}**")
                st.json(r2[["First Name", "Last Name", "Email", "Phone", "Birthdate"]].to_dict())
            with cols[2]:
                choice = st.radio(f"Match?", ["Undecided", "Yes", "No"], key=f"choice_{idx}")
                feedback_log.append({
                    "record1_index": i,
                    "record2_index": j,
                    "record1_email": r1["Email"],
                    "record2_email": r2["Email"],
                    "predicted_proba": row["predicted_proba"],
                    "feedback": choice
                })
                if choice == "Yes":
                    feedback_yes.append((i, j))

        if st.button("📦 Confirm Feedback & Generate Report"):
            G = nx.Graph()
            G.add_nodes_from(df.index)
            for row in df[df["cluster_id"] >= 0].itertuples():
                G.add_node(row.Index)
            for row in pairs_df.itertuples():
                if row.predicted_proba >= threshold:
                    G.add_edge(row.record1_index, row.record2_index)
            for i, j in feedback_yes:
                G.add_edge(i, j)

            components = list(nx.connected_components(G))
            cluster_map = {}
            for cid, nodes in enumerate(components):
                for node in nodes:
                    cluster_map[node] = cid
            df["final_cluster_id"] = df.index.map(cluster_map).fillna(-1).astype(int)

            def merge_group(group):
                merged = {}
                for col in ['First Name', 'Last Name', 'Email', 'Phone', 'Gender', 'City', 'Country']:
                    merged[col] = group[col].mode().iloc[0] if not group[col].mode().empty else ''
                merged['Birthdate'] = group['Birthdate'].min()
                merged['Notes'] = ' '.join(group['Notes'].dropna().astype(str))[:500]
                merged['cluster_id'] = group['final_cluster_id'].iloc[0]
                return pd.Series(merged)

            golden = df[df["final_cluster_id"] >= 0].groupby("final_cluster_id").apply(merge_group).reset_index(drop=True)

            st.subheader("📈 Final Cluster Distribution")
            fig, ax = plt.subplots()
            sns.histplot(df["final_cluster_id"].value_counts(), bins=30, ax=ax)
            st.pyplot(fig)

            st.subheader("📐 Model AUC Evaluation")
            y_true = [1 if df.loc[int(i), "cluster_id"] == df.loc[int(j), "cluster_id"] else 0
                      for i, j in zip(pairs_df["record1_index"], pairs_df["record2_index"])]
            y_pred_proba = pairs_df["predicted_proba"]
            auc_score = roc_auc_score(y_true, y_pred_proba)
            st.metric(label="ROC-AUC Score", value=f"{auc_score:.4f}")

            # Save feedback log
            feedback_df = pd.DataFrame(feedback_log)
            feedback_df.to_csv("output/feedback_log.csv", index=False)

            # Export result
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                golden.to_excel(writer, sheet_name="Golden Records", index=False)
                df.to_excel(writer, sheet_name="All Records + Final Cluster", index=False)
                feedback_df.to_excel(writer, sheet_name="Uncertain Pairs + Feedback", index=False)
            st.download_button(
                label="📥 Download Excel Report",
                data=output.getvalue(),
                file_name="golden_record_feedback_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
