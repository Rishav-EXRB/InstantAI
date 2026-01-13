import pandas as pd
import yaml
import streamlit as st
from datetime import timedelta

import plotly.express as px
import plotly.graph_objects as go

from core.metrics import apply_derived_metrics
from core.scorer import score_entities
from core.explain import explain_entity
from core.time_windows import slice_time_window
from core.deltas import compute_rank_delta
from core.improve import improvement_plan
from core.learn_weights import learn_metric_weights

from agents.chat_analyst import ChatAnalyst
from agents.tools.web_enrichment import WebEnrichmentTool

analyst = ChatAnalyst()
web_tool = WebEnrichmentTool()

st.set_page_config(
    page_title="Universal Ranking Engine",
    layout="wide"
)

# =================================================
# Session state (ML weight control)
# =================================================
if "use_ml_weights" not in st.session_state:
    st.session_state.use_ml_weights = False

if "ml_weights" not in st.session_state:
    st.session_state.ml_weights = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =================================================
# Load config
# =================================================
with open("configs/apar.yaml") as f:
    config = yaml.safe_load(f)

# =================================================
# Load dataset
# =================================================
df = pd.read_csv("data/cleaned_apar.csv")

# =================================================
# Normalize column names
# =================================================
if config["schema"].get("normalize_columns", False):
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(" ", "_")
          .str.replace("/", "_", regex=False)
    )

# =================================================
# Parse date safely
# =================================================
if "order_date" not in df.columns:
    st.error("Required column 'order_date' not found in dataset.")
    st.stop()

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# =================================================
# Apply derived metrics
# =================================================
df = apply_derived_metrics(df, config.get("derived_metrics", {}))

# =================================================
# SIDEBAR — ENTITY SWITCH
# =================================================
st.sidebar.title("Entity")

entity_key = st.sidebar.selectbox(
    "Rank by",
    list(config["entities"].keys())
)

entity_col = config["entities"][entity_key]["column"]

# =================================================
# SIDEBAR — WEIGHTS (with ML override)
# =================================================
st.sidebar.title("Ranking Weights")

runtime_metrics = {}
total_weight = 0.0

for name, meta in config["ranking"]["metrics"].items():
    default_weight = (
        st.session_state.ml_weights.get(name, meta["weight"])
        if st.session_state.use_ml_weights
        else meta["weight"]
    )

    w = st.sidebar.slider(
        name,
        0.0, 1.0,
        float(default_weight),
        0.05
    )

    runtime_metrics[name] = {**meta, "weight": w}
    total_weight += w

if total_weight > 0:
    for k in runtime_metrics:
        runtime_metrics[k]["weight"] /= total_weight

# =================================================
# SIDEBAR — TIME WINDOWS
# =================================================
st.sidebar.title("Time Window")

max_date = df["order_date"].max()
min_date = df["order_date"].min()

current_start = st.sidebar.date_input(
    "Current window start",
    max_date - timedelta(days=30)
)

current_end = st.sidebar.date_input(
    "Current window end",
    max_date
)

previous_start = st.sidebar.date_input(
    "Previous window start",
    current_start - timedelta(days=30)
)

previous_end = st.sidebar.date_input(
    "Previous window end",
    current_start - timedelta(days=1)
)

# =================================================
# Slice data
# =================================================
df_current = slice_time_window(df, current_start, current_end)
df_previous = slice_time_window(df, previous_start, previous_end)

# =================================================
# Rank both windows
# =================================================
current_rank = score_entities(
    df_current,
    {"entity": entity_col, "metrics": runtime_metrics}
)

previous_rank = score_entities(
    df_previous,
    {"entity": entity_col, "metrics": runtime_metrics}
)

ranking = compute_rank_delta(
    current_rank,
    previous_rank,
    entity_col
)

# =================================================
# SIDEBAR — CHAT ANALYST
# =================================================
st.sidebar.divider()
st.sidebar.subheader("💬 AI Investigation")

for msg in st.session_state.chat_history:
    with st.sidebar.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.sidebar.chat_input("Ask about rankings..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.sidebar.chat_message("user"):
        st.write(prompt)
    
    with st.sidebar.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = analyst.analyze(prompt, ranking, entity_key, config)
            st.write(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# =================================================
# MAIN UI
# =================================================
st.title("Universal Ranking Engine")
st.caption(f"Ranking {entity_key}s with explainability and intelligence")

st.subheader("Ranked Entities")
st.dataframe(
    ranking[
        [entity_col, "rank", "previous_rank", "rank_change", "final_score"]
    ]
)

# =================================================
# VISUAL 1: RANK DISTRIBUTION & MOVEMENT
# =================================================
st.subheader("Ranking Overview")

col1, col2 = st.columns(2)

with col1:
    fig_rank = px.histogram(
        ranking,
        x="rank",
        nbins=20,
        title="Rank Distribution",
        color_discrete_sequence=["#4C78A8"]
    )
    fig_rank.update_layout(
        bargap=0.1,
        xaxis_title="Rank",
        yaxis_title="Number of Entities"
    )
    st.plotly_chart(fig_rank, use_container_width=True)

with col2:
    fig_delta = px.scatter(
        ranking,
        x="previous_rank",
        y="rank",
        size=ranking["rank_change"].abs(),
        color="rank_change",
        color_continuous_scale="RdYlGn",
        title="Rank Movement (Previous → Current)",
        labels={
            "previous_rank": "Previous Rank",
            "rank": "Current Rank"
        }
    )
    fig_delta.add_shape(
        type="line",
        x0=ranking["rank"].min(),
        y0=ranking["rank"].min(),
        x1=ranking["rank"].max(),
        y1=ranking["rank"].max(),
        line=dict(dash="dash")
    )
    st.plotly_chart(fig_delta, use_container_width=True)

# =================================================
# ENTITY ANALYSIS
# =================================================
st.subheader("Entity Analysis")

entity = st.selectbox(
    f"Select {entity_key}",
    ranking[entity_col]
)

row = ranking[ranking[entity_col] == entity].iloc[0]

st.write(f"Current rank: {row['rank']}")
st.write(f"Previous rank: {row['previous_rank']}")
st.write(f"Rank change: {row['rank_change']}")

# -------------------------------------------------
# Key drivers
# -------------------------------------------------
st.markdown("### Key Drivers")
col_e1, col_e2 = st.columns([3, 1])
with col_e1:
    for e in explain_entity(row, runtime_metrics):
        st.write("•", e)

with col_e2:
    if st.button("✨ Why Trace"):
        with st.spinner("Reasoning..."):
            trace = analyst.generate_why_trace(entity, row, runtime_metrics)
            st.info(trace)

if st.button("🌐 Search Market Context"):
    with st.spinner(f"Searching web for {entity}..."):
        result = web_tool.search_entity_sentiment(entity)
        st.success(f"**{result['signal']}**")
        st.caption(f"Source: {result['source']} | Web Sentiment Score: {result['web_score']}")

# -------------------------------------------------
# VISUAL 2: METRIC CONTRIBUTIONS
# -------------------------------------------------
st.markdown("### Score Contribution Breakdown")

contrib_df = pd.DataFrame([
    {"metric": m, "contribution": row[f"{m}_score"]}
    for m in runtime_metrics
])

fig_contrib = px.bar(
    contrib_df,
    x="metric",
    y="contribution",
    color="contribution",
    color_continuous_scale="Blues",
    title="Metric Contributions to Final Score"
)

fig_contrib.update_layout(
    xaxis_title="Metric",
    yaxis_title="Weighted Contribution"
)

st.plotly_chart(fig_contrib, use_container_width=True)

# -------------------------------------------------
# What to improve
# -------------------------------------------------
st.markdown("### What to Improve")

plans = improvement_plan(row, ranking, runtime_metrics)

if not plans:
    st.success("This entity is already performing at peer-top levels.")
else:
    for p in plans[:3]:
        st.write(f"• {p['recommendation']} (gap: {p['gap']})")

# -------------------------------------------------
# ML-assisted weight suggestions
# -------------------------------------------------
st.markdown("### ML-Assisted Weight Suggestions")

learned_weights = learn_metric_weights(ranking, runtime_metrics)

weight_df = pd.DataFrame([
    {
        "metric": m,
        "current_weight": round(runtime_metrics[m]["weight"], 3),
        "ml_suggested_weight": round(learned_weights.get(m, 0), 3)
    }
    for m in runtime_metrics
])

st.dataframe(weight_df)

col1, col2 = st.columns(2)

with col1:
    if st.button("Apply ML-Suggested Weights"):
        st.session_state.use_ml_weights = True
        st.session_state.ml_weights = learned_weights
        st.rerun()

with col2:
    if st.button("Reset to Manual Weights"):
        st.session_state.use_ml_weights = False
        st.session_state.ml_weights = {}
        st.rerun()

# =================================================
# PORTFOLIO-LEVEL ANALYSIS
# =================================================
st.subheader("Portfolio Insights")

top_movers = ranking.sort_values("rank_change", ascending=False).head(3)
bottom_movers = ranking.sort_values("rank_change").head(3)

avg_score = ranking["final_score"].mean()
score_std = ranking["final_score"].std()

st.markdown("### Key Observations")

st.write(
    f"• Average performance score is **{avg_score:.3f}**, "
    f"with dispersion **{score_std:.3f}**, indicating "
    f"{'high' if score_std > 0.15 else 'moderate'} differentiation."
)

st.write("• **Top positive rank movers**:")
for _, r in top_movers.iterrows():
    st.write(f"  - {r[entity_col]} (↑ {r['rank_change']})")

st.write("• **Largest rank declines**:")
for _, r in bottom_movers.iterrows():
    st.write(f"  - {r[entity_col]} (↓ {abs(r['rank_change'])})")

st.write(
    "• Rankings are primarily influenced by metrics with high variance "
    "and strong contribution weights, as reflected in ML-suggested weights."
)
