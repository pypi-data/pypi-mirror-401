import typer
import json
from ...parser import QueryParser
from ...evaluator import QueryEvaluator
from ...engines.mongodb.MongoTransformer import MongoTransformer
import random
from pymongo import MongoClient
from .commands import eval_cmd, mongodb_cmd

# app = typer.Typer()
# uri = "mongodb+srv://kaojj222_db_user:ojvHod1J3niVyvQt@cluster0.mnbjvo5.mongodb.net/"
# client = MongoClient(uri)

# @app.command() # 本地查詢,使用evaluator.execute
# def eval(
#     query_file: str,
#     data_file: str
# ):
#     """
#     使用 SimpleQL 語法對本地 JSON 資料進行查詢
#     語法：python -m simpleql.cli eval query.json data.json
#     """
#     # 讀取 query
#     with open(query_file, "r", encoding="utf-8") as f:
#         query = f.read()

#     # 讀取資料
#     with open(data_file, "r", encoding="utf-8") as f:
#         rows = json.load(f)

#     # 解析 query
#     parser = QueryParser()
#     parsed = parser.parse(query)

#     # ----------------------------
#     # 探索型指令處理
#     # ----------------------------
#     if "command" in parsed:
#         cmd = parsed["command"]
#         collection = parsed["collection"]

#         if cmd == "show types":
#             if rows:
#                 typer.echo(f"Types for {collection}:")
#                 types_info = {k: type(v).__name__ for k, v in rows[0].items()}
#                 typer.echo(json.dumps(types_info, indent=2, ensure_ascii=False))
#             else:
#                 typer.echo(f"No data in collection {collection}")
#             return

#         elif cmd == "sample":
#             n = parsed.get("sample_count", 1)
#             n = min(n, len(rows))
#             sampled_rows = random.sample(rows, n)
#             typer.echo(json.dumps(sampled_rows, indent=2, ensure_ascii=False))
#             return

#         elif cmd == "head":
#             n = parsed.get("head_count", 5)
#             typer.echo(json.dumps(rows[:n], indent=2, ensure_ascii=False))
#             return

#         elif cmd == "count":
#             fields = parsed.get("fields", [])
#             result = {}
#             for f in fields:
#                 result[f] = sum(1 for row in rows if f in row and row[f] is not None)
#             typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
#             return

#         elif cmd == "stats":
#             import statistics
#             fields = parsed.get("fields", [])
#             result = {}
#             for f in fields:
#                 vals = [row[f] for row in rows if f in row and isinstance(row[f], (int, float))]
#                 if vals:
#                     result[f] = {
#                         "mean": statistics.mean(vals),
#                         "median": statistics.median(vals),
#                         "min": min(vals),
#                         "max": max(vals)
#                     }
#                 else:
#                     result[f] = None
#             typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
#             return

#         elif cmd == "unique":
#             fields = parsed.get("fields", [])
#             result = {}
#             for f in fields:
#                 result[f] = list({row[f] for row in rows if f in row})
#             typer.echo(json.dumps(result, indent=2, ensure_ascii=False))
#             return

#         else:
#             typer.echo(f"Unknown command: {cmd}")
#             return

#     # ----------------------------
#     # 普通查詢處理
#     # ----------------------------
#     if "filter" not in parsed:
#         typer.echo("No filter found in query")
#         return

#     ast = parsed["filter"]
#     select = parsed["select"]
#     order_by = parsed["order_by"]
#     group_by = parsed["group_by"]
#     limit = parsed["limit"]

#     evaluator = QueryEvaluator()
#     result = evaluator.execute(ast, rows, select, order_by, group_by, limit)

#     # ----------------------------
#     # 格式化輸出，只保留 select 指定欄位
#     # ----------------------------
#     def format_row(row):
#         return {evaluator.format_field_name(f): row[evaluator.format_field_name(f)] for f in select["fields"]}

#     if group_by:
#         output = {}
#         for key, group_rows in result.items():
#             key_str = ", ".join(str(k) for k in key) if isinstance(key, tuple) else str(key)
#             filtered_rows = [format_row(r) for r in group_rows]
#             output[key_str] = filtered_rows
#     else:
#         output = [format_row(r) for r in result]

#     typer.echo(json.dumps(output, indent=2, ensure_ascii=False))

# @app.command()
# def mongodb(query_file: str):
#     """
#     將 SimpleQL 轉換為 MongoDB aggregation pipeline
#     語法：python -m simpleql.cli mongodb query.sql
#     """
#     with open(query_file, "r", encoding="utf-8") as f:
#         query = f.read()

#     parser = QueryParser()
#     parsed = parser.parse(query)

#     transformer = MongoTransformer()
#     pipeline = transformer.transform_to_pipeline(parsed)

#     # 2️⃣ 連接 MongoDB
#     db = client["test_db"]
#     collection = db[parsed["collection"]]

#     # 3️⃣ 執行 aggregate pipeline
#     results = list(collection.aggregate(pipeline))

#     # 4️⃣ 列印結果
#     typer.echo(json.dumps(results, indent=2, ensure_ascii=False))

app = typer.Typer()
app.add_typer(eval_cmd.app, name="eval")
app.add_typer(mongodb_cmd.app, name="mongodb")

if __name__ == "__main__":
    app()
