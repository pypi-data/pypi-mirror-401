import typer
from ..parser import QueryParser
from ..evaluator import QueryEvaluator
from ..engines.mongodb.MongoTransformer import MongoTransformer
import random
from pymongo import MongoClient
from bson import json_util


app = typer.Typer()
uri = "mongodb+srv://kaojj222_db_user:ojvHod1J3niVyvQt@cluster0.mnbjvo5.mongodb.net/"
client = MongoClient(uri)

# 語法：python -m simpleql.cli mongodb run query.sql
@app.command(name="")  # 不使用evaluator.execute
def run(query_file: str):
    """
    將 SimpleQL 轉換為 MongoDB aggregation pipeline
    """
    with open(query_file, "r", encoding="utf-8") as f:
        query = f.read()

    parser = QueryParser()
    parsed = parser.parse(query)

    # 2️⃣ 連接 MongoDB
    db = client["test_db"]
    collection_name = parsed["collection"]
    collection = db[collection_name]
    command = parsed.get("command")

    # ---------- 探索型指令 ----------
    if command == "show_types":
        show_types_mongodb(collection)
        return
    elif command == "sample":
        n = parsed.get("sample_count", 1)
        show_sample(collection, n)
        return
    elif command == "head":
        n = parsed.get("head_count", 5)
        show_head(collection, n)
        return
    elif command == "count":
        fields = parsed.get("fields", [])
        show_count(collection, fields)
        return
    elif command == "stats":
        fields = parsed.get("fields", [])
        show_stats(collection, fields)
        return
    elif command == "unique":
        fields = parsed.get("fields", [])
        show_unique(collection, fields)
        return

    transformer = MongoTransformer()
    pipeline = transformer.transform_to_pipeline(parsed)

   
    # 3️⃣ 執行 aggregate pipeline
    results = list(collection.aggregate(pipeline))

    # 4️⃣ 列印結果
    typer.echo(json_util.dumps(results, indent=2, ensure_ascii=False))

# ---------- 工具函數 ----------
def show_types_mongodb(col):
    sample = col.find_one()
    if not sample:
        typer.echo("No data")
        return
    type_map = {k: mongo_type_to_simple_type(v) for k, v in sample.items() if k != "_id"}
    typer.echo(f"Types for {col.name}:")
    typer.echo(json_util.dumps(type_map, indent=2, ensure_ascii=False))


def show_sample(col, n):
    results = list(col.aggregate([{"$sample": {"size": n}}]))
    typer.echo(json_util.dumps(results, indent=2, ensure_ascii=False))


def show_head(col, n):
    results = list(col.find().limit(n))
    typer.echo(json_util.dumps(results, indent=2, ensure_ascii=False))


def show_count(col, fields):
    if not fields:
        count = col.count_documents({})
        typer.echo(f"Total documents: {count}")
        return
    
    group_body = {"_id": None}   # MongoDB 要求一定要有

    for field in fields:
        group_body[f"{field}_count"] = {"$sum": 1}

    pipeline = [
        {"$group": group_body}
    ]

    results = list(col.aggregate(pipeline))
    typer.echo(json_util.dumps(results, indent=2, ensure_ascii=False))


def show_stats(col, fields):
    from bson.son import SON
    if not fields:
        typer.echo("Please specify fields for stats")
        return
    pipeline = [
        {"$group": {
            "_id": None,
            **{f"{field}_min": {"$min": f"${field}"} for field in fields},
            **{f"{field}_max": {"$max": f"${field}"} for field in fields},
            **{f"{field}_avg": {"$avg": f"${field}"} for field in fields},
            **{f"{field}_sum": {"$sum": f"${field}"} for field in fields}
        }}
    ]
    results = list(col.aggregate(pipeline))
    typer.echo(json_util.dumps(results, indent=2, ensure_ascii=False))


def show_unique(col, fields):
    if not fields:
        typer.echo("Please specify fields for unique")
        return
    pipeline = [
        {"$group": {field: {"$addToSet": f"${field}"} for field in fields}}
    ]
    results = list(col.aggregate(pipeline))
    typer.echo(json_util.dumps(results, indent=2, ensure_ascii=False))

def mongo_type_to_simple_type(v):
    from bson import ObjectId
    from datetime import datetime

    if isinstance(v, str):
        return "str"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, datetime):
        return "str"
    if isinstance(v, ObjectId):
        return "str"
    if isinstance(v, list):
        return "list"
    if isinstance(v, dict):
        return "dict"
    return type(v).__name__