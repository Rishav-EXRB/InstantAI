import streamlit as st
import pandas as pd
import requests
import tempfile
import plotly.express as px

BACKEND_URL = "http://127.0.0.1:8000/rank"

st.set_page_config(
    page_title="Universal Dataset Ranking",
    layout="wide"
)

st.title("📊 Universal Dataset Ranking Engine")
st.caption("Upload any dataset, describe how to rank it, and get explainable ML-driven rankings.")

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)

query = st.text_input(
    "Ranking Query",
    placeholder="e.g. Rank customers based on sales and profit"
)

run = st.button("Run Ranking")

# -----------------------------
# Dataset Preview
# -----------------------------
if uploaded_file:
    try:
        preview_df = pd.read_csv(uploaded_file, nrows=10, encoding="utf-8")
    except Exception:
        preview_df = pd.read_csv(uploaded_file, nrows=10, encoding="latin1")

    st.subheader("📄 Dataset Preview")
    st.dataframe(preview_df, use_container_width=True)

# -----------------------------
# Ranking Request
# -----------------------------
if run and uploaded_file and query:

    with st.spinner("Running ranking pipeline..."):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            uploaded_file.seek(0)
            tmp.write(uploaded_file.read())
            file_path = tmp.name

        with open(file_path, "rb") as f:
            response = requests.post(
                BACKEND_URL,
                params={"query": query},
                files={"file": f}
            )

    if response.status_code != 200:
        st.error("Ranking failed")
        st.code(response.text)
        st.stop()

    data = response.json()

    # -----------------------------
    # Rankings Table
    # -----------------------------
    rankings = data.get("rankings", [])

    if not rankings:
        st.warning("No rankings returned.")
        st.stop()

    rank_df = pd.DataFrame(rankings)

    st.subheader("🏆 Rankings")
    st.dataframe(rank_df, use_container_width=True)

    # -----------------------------
    # Metric Explanations
    # -----------------------------
    explanations = data.get("explanations")

    if explanations:
        st.subheader("🧠 Ranking Explanations")

        for entity, exp in explanations.items():
            with st.expander(entity):
                for metric, text in exp.items():
                    st.markdown(f"**{metric}**: {text}")

    # -----------------------------
    # PCA Visualization
    # -----------------------------
    pca = data.get("pca")

    if pca and pca.get("components"):

        st.subheader("📊 PCA Cluster Visualization")

        pca_df = pd.DataFrame(pca["components"])

        fig = px.scatter(
            pca_df,
            x="x",
            y="y",
            color="cluster",
            size="score",
            hover_name="entity",
            title="PCA Projection of Ranked Entities",
            labels={
                "x": "PCA Component 1",
                "y": "PCA Component 2",
                "cluster": "Cluster"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

        ev = pca.get("explained_variance", [])
        if ev:
            st.caption(
                f"Explained Variance — PC1: {ev[0]*100:.1f}%, PC2: {ev[1]*100:.1f}%"
            )

    else:
        st.info("PCA visualization not available for this run.")
