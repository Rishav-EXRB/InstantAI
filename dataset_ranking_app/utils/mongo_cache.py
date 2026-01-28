from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb://localhost:27017")
db = client["ranking_cache"]
collection = db["query_results"]


def _hash_string(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def dataset_hash(df):
    csv = df.to_csv(index=False)
    return _hash_string(csv)


def cache_key(query: str, df):
    return _hash_string(query + dataset_hash(df))


def fetch_cached_result(query, df):
    key = cache_key(query, df)
    doc = collection.find_one({"_id": key})
    if doc:
        return doc["result"]
    return None


def save_cached_result(query, df, result):
    key = cache_key(query, df)
    collection.replace_one(
        {"_id": key},
        {
            "_id": key,
            "query": query,
            "dataset_hash": dataset_hash(df),
            "result": result
        },
        upsert=True
    )
