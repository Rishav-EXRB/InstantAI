from fastapi import FastAPI, UploadFile, File, Query
import pandas as pd
import tempfile
import shutil
import math

from pipeline.stage_01_intent import infer_intent
from pipeline.stage_02_data_audit import audit_dataset
from pipeline.stage_03_features import generate_features
from pipeline.stage_04_metric_map import (
    resolve_entity_column,
    map_metrics_to_features
)
from pipeline.stage_07_rank import rank_entities
from pipeline.stage_08_explain import generate_explanations
from pipeline.stage_09_pca import generate_pca_data

from utils.mongo_cache import (
    fetch_cached_result,
    save_cached_result
)

app = FastAPI()


def sanitize(obj):
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return 0.0
        return obj
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    return obj


@app.post("/rank")
def rank_dataset(
    query: str = Query(...),
    file: UploadFile = File(...)
):

    # ---------------- SAVE FILE ----------------
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file.file.seek(0)
        shutil.copyfileobj(file.file, tmp)
        path = tmp.name

    # ---------------- READ CSV ----------------
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except Exception:
        df = pd.read_csv(path, encoding="latin1")

    if df.empty:
        return {
            "error": "Ranking failed",
            "details": "Uploaded dataset is empty"
        }

    # ---------------- CACHE LOOKUP ----------------
    cached = fetch_cached_result(query, df)
    if cached:
        return cached

    # ---------------- AUDIT ----------------
    audit = audit_dataset(df)

    # ---------------- INTENT ----------------
    intent = infer_intent(query)

    # ---------------- ENTITY ----------------
    entity_column = resolve_entity_column(
        intent.entity_column,
        audit
    )

    # ---------------- FEATURES ----------------
    features = generate_features(audit)

    # ---------------- METRIC MAP ----------------
    metric_map = map_metrics_to_features(
        intent,
        audit,
        features
    )

    # ---------------- RANKING ----------------
    ranked = rank_entities(
        audit.df,
        entity_column,
        metric_map
    )

    # ---------------- EXPLANATIONS ----------------
    explanations = generate_explanations(
        audit.df,
        ranked,
        entity_column,
        metric_map
    )

    # ---------------- PCA ----------------
    pca_data = generate_pca_data(
        audit.df,
        entity_column,
        metric_map,
        ranked
    )

    response = {
        "entity_column": entity_column,
        "rankings": ranked.to_dict(orient="records"),
        "explanations": explanations,
        "pca": pca_data
    }

    response = sanitize(response)

    # ---------------- SAVE TO MONGO ----------------
    save_cached_result(query, df, response)

    return response
