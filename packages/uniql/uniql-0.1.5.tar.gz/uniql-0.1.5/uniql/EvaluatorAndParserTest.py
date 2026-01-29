from .parser import QueryParser
from .evaluator import QueryEvaluator
from datetime import datetime


# -----------------------------
# 初始化 parser 與 evaluator
# -----------------------------
parser = QueryParser()
evaluator = QueryEvaluator()

# -----------------------------
# 查詢範例
# -----------------------------
# query = 'users / NOT (age > 25 AND city = "Taipei") / select DISTINCT name, age / order by created_at asc'
query = 'users / (age > 25 AND city = "Taipei") / select DISTINCT name, age / order by city desc / group by city'
# query = '''
# users
# / age > 20
# / select DISTINCT name, age
# / order by age desc
# / limit 2 offset 2
# '''
# query = """
# users
# / NOT (YEAR(created_at) = 2022 AND age > 30)
# / select DISTINCT name
# """
# 測 DATE()（只取年月日）
# query = """
# users
# / DATE(created_at) = "2023-05-10"
# / select name
# """
# query = """
# users
# / LOWER(name) = "alice"
# / select CONCAT(name, age)
# """
# 測 ROUND、CEIL、FLOOR
# query = """
# users
# / age > 20
# / select ROUND(age,2), CEIL(age), FLOOR(age)
# """

# query = 'users / show types'
# query = 'users / sample 2'
# query = 'users / head 2'

# query = 'users / stats age'





# 解析 query
parsed = parser.parse(query)
# print(parsed["select"]["fields"])
# 格式
# parsed["select"] = {
#     "fields": ["name", "age"],
#     "distinct": True
# }



# -----------------------------
# 測試資料
# -----------------------------
# data = [
#     {"name": "Alice", "age": 30, "city": "Taipei"},
#     {"name": "Bob", "age": 22, "city": "Taipei"},
#     {"name": "Charlie", "age": 35, "city": "Taichung"},
#     {"name": "David", "age": 28, "city": "Taichung"},
#     {"name": "Eve", "age": 25, "city": "Taoung"},
#     # 重複資料
#     {"name": "Bob", "age": 22, "city": "Taipei"},
#     {"name": "David", "age": 28, "city": "Taichung"},
# ]
data = [
    {
        "name": "Alice",
        "age": 30.634,
        "city": "Taipei",
        "created_at": datetime(2023, 5, 10, 14, 30)
    },
    {
        "name": "Bob",
        "age": 22.5,
        "city": "Taipei",
        "created_at": datetime(2024, 1, 3, 9, 0)
    },
    {
        "name": "Bob2",
        "age": 22.1,
        "city": "Taipei",
        "created_at": datetime(2024, 1, 3, 9, 0)
    },
    {
        "name": "Charlie",
        "age": 35.4,
        "city": "Taichung",
        "created_at": datetime(2022, 12, 25, 18, 0)
    },
]


# 探索型指令判斷
command = parsed.get("command")
if command == "show types":
    types = {k: type(v).__name__ for k, v in data[0].items()}
    print("Column types:", types)
elif command == "sample":
    n = parsed.get("sample_count", 1)
    import random
    for r in random.sample(data, min(n, len(data))):
        print(r)
elif command == "head":
    n = parsed.get("head_count", 5)
    for r in data[:n]:
        print(r)
elif command == "count":
    fields = parsed.get("fields", [])
    from collections import Counter
    for field in fields:
        cnt = Counter(row[field] for row in data)
        print(f"Count for {field}:", dict(cnt))
elif command == "stats":
    fields = parsed.get("fields", [])
    import math
    for field in fields:
        values = [row[field] for row in data if isinstance(row[field], (int, float))]
        if not values:
            print(f"Stats for {field}: no numeric data")
            continue
        avg = sum(values)/len(values)
        maximum = max(values)
        minimum = min(values)
        std = math.sqrt(sum((v-avg)**2 for v in values)/len(values))
        print(f"Stats for {field}: avg={avg}, max={maximum}, min={minimum}, std={std}, count={len(values)}")
elif command == "unique":
    fields = parsed.get("fields", [])
    for field in fields:
        uniques = set(row[field] for row in data)
        print(f"Unique values for {field}:", uniques)
else:

    select = {
        "fields": parsed["select"]["fields"],
        "distinct": parsed["select"].get("distinct", False)
    }

    # -----------------------------
    # 執行查詢
    # -----------------------------
    results = evaluator.execute(
        ast=parsed["filter"],
        rows=data,
        select=select,
        order_by=parsed.get("order_by"),
        group_by=parsed.get("group_by"),
        limit=parsed.get("limit"),
    )

    # -----------------------------
    # 輸出結果
    # -----------------------------
    if isinstance(results, dict):
        # 有 GROUP BY
        for group_key, group_rows in results.items():
            if len(group_key) == 1:
                group_key = group_key[0]
            print(f"Group {group_key}:")
            for r in group_rows:
                print(" ", {f: r[f] for f in select["fields"]})
    else:
        # 沒有 GROUP BY（LIMIT 會走這裡）
        # 為了只有打印出select的欄位
        for r in results:
            print({f: r[f] for f in select["fields"]})
