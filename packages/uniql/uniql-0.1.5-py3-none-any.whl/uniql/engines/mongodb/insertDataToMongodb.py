from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://kaojj222_db_user:ojvHod1J3niVyvQt@cluster0.mnbjvo5.mongodb.net/")
db = client["test_db"]
collection = db["users"]

# 清空舊資料
collection.delete_many({})

rows = [
    {
        "name": "Alice",
        "age": 30.634,
        "city": "Taipei",
        "created_at": datetime(2023, 5, 10, 14, 30, 0)
    },
    {
        "name": "Bob",
        "age": 22.5,
        "city": "Taipei",
        "created_at": datetime(2025, 1, 3, 9, 0, 0)
    },
    {
        "name": "Bob2",
        "age": 22.1,
        "city": "Taipei",
        "created_at": datetime(2024, 1, 3, 9, 0, 0)
    },
    {
        "name": "Charlie",
        "age": 35.4,
        "city": "Taichung",
        "created_at": datetime(2022, 12, 25, 18, 0, 0)
    }
]

collection.insert_many(rows)
print("已將假資料插入 MongoDB")
