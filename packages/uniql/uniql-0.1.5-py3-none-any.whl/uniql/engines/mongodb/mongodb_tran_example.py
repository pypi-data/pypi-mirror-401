import sys, os
from simpleql.evaluator import QueryEvaluator
from datetime import datetime
from .MongoTransformer import MongoTransformer

# -----------------------------
# 假設 AST (通常由 Parser 生成)
# -----------------------------
ast = {
    "type": "and",
    "left": {
        "type": "condition",
        "field": "age",
        "op": ">=",
        "value": 18
    },
    "right": {
        "type": "condition",
        "field": {"type": "function", "name": "YEAR", "args": ["created_at"]},
        "op": "=",
        "value": 2024
    }
}

# -----------------------------
# 假資料
# -----------------------------
rows = [
    {"name": "Alice", "age": 20, "created_at": datetime.fromisoformat("2024-01-01")},
    {"name": "Bob", "age": 17, "created_at": datetime.fromisoformat("2024-06-01")},
    {"name": "Charlie", "age": 25, "created_at": datetime.fromisoformat("2023-12-31")},
    {"name": "David", "age": 30, "created_at": datetime.fromisoformat("2024-03-15")},
]

# -----------------------------
# 1️⃣ 使用 Python Evaluator + VM 過濾
# -----------------------------
evaluator = QueryEvaluator()

filtered_rows_python = [row for row in rows if evaluator.eval_with_vm(ast, row)]

print("=== Python VM 過濾結果 ===")
for row in filtered_rows_python:
    print(row)

# -----------------------------
# 2️⃣ 使用 MongoTransformer 生成 MongoDB 查詢
# -----------------------------
transformer = MongoTransformer()
mongo_query = transformer.transform(ast)

print("\n=== 對應 MongoDB 查詢條件 ===")
print(mongo_query)

# -----------------------------
# 3️⃣ MongoDB 查詢示範（需要安裝 pymongo）
# -----------------------------
# 從 pymongo import MongoClient
# 並假設資料已經存在 MongoDB collection 中
# -----------------------------
try:
    from pymongo import MongoClient

    uri = "mongodb+srv://kaojj222_db_user:ojvHod1J3niVyvQt@cluster0.mnbjvo5.mongodb.net/"

    client = MongoClient(uri)
    db = client["test_db"]
    collection = db["users"]

    # 假設 collection 已經插入過 rows
    # collection.insert_many(rows)  # 只在第一次使用

    mongo_results = list(collection.find(mongo_query))

    print("\n=== MongoDB 查詢結果 ===")
    for doc in mongo_results:
        print(doc)

except ImportError:
    print("\n請安裝 pymongo 才能做 MongoDB 查詢")
except Exception as e:
    print("\nMongoDB 查詢錯誤:", e)
