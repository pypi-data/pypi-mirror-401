import re
from datetime import date, datetime  

class MongoTransformer:
    OP_MAP = {
        "=": "$eq",
        "!=": "$ne",
        ">": "$gt",
        "<": "$lt",
        ">=": "$gte",
        "<=": "$lte",
        "in": "$in",
        "not in": "$nin",
    }

    LOGIC_MAP = {
        "and": "$and",
        "or": "$or",
    }

    DATE_FUNCS = {"YEAR", "MONTH", "DATE"}
    STRING_FUNCS = {"UPPER", "LOWER", "CONCAT"}
    NUMERIC_FUNCS = {"ROUND", "CEIL", "FLOOR"}

    # -------------------------------
    # 將整個 query 轉成 aggregation pipeline
    # -------------------------------
    def transform_to_pipeline(self, parsed):
        pipeline = []

        # ------------------
        # 1. $match
        # ------------------
        if "filter" in parsed:
            pipeline.append({"$match": self.transform_filter(parsed["filter"])})

        # ------------------
        # 2. $project
        # ------------------
        if "select" in parsed and parsed["select"]["fields"]:
            project_stage = {"$project": {"_id": 0}}

            # select 欄位
            for f in parsed["select"]["fields"]:
                if isinstance(f, str):
                    project_stage["$project"][f] = f"${f}"
                elif isinstance(f, dict) and f.get("type") == "function":
                    project_stage["$project"][self.format_field_name(f)] = self.transform_function(f)

            # ⭐ group by 欄位一定要保留
            if parsed.get("group_by"):
                for g in parsed["group_by"]:
                    project_stage["$project"][g] = f"${g}"

            pipeline.append(project_stage)

        # ------------------
        # 3. ⭐ GROUP BY
        # ------------------
        if parsed.get("group_by"):
            group_fields = parsed["group_by"]

            group_id = {g: f"${g}" for g in group_fields}

            pipeline.append({
                "$group": {
                    "_id": group_id,
                    "items": {"$push": "$$ROOT"}
                }
            })

        # ------------------
        # 4. $sort
        # ------------------
        if parsed.get("order_by"): # 如果有 order by 
            # mongodb中排序要用 $sort，先建立一個空的 $sort dict，之後會把欄位與排序方向加入這個 dict。
            sort_stage = {"$sort": {}} 
           
            # parsed["order_by"] 是解析後的排序列表，格式大概像這樣：
            # [{"field": "city", "direction": "asc"}]
            for o in parsed["order_by"]: 
                # MongoDB 的 $sort 裡，排序方向不是 "asc"/"desc"，而是數字：
                # 1 表示升冪，-1 表示降冪
                direction = 1 if o["direction"].lower() == "asc" else -1 
                field_name = o["field"] # 取得要排序的欄位名稱。例如 "city"。
                # 核心關鍵：如果你的 query 有 GROUP BY，MongoDB 的 $group stage 會把群組欄位放到 _id 裡。
                if parsed.get("group_by") and field_name in parsed["group_by"]:
                    # 如果有 group，排序欄位要改成 _id.xxx。例如_id.city。
                    field_name = f"_id.{field_name}"
                # 把欄位名稱與排序方向加入 $sort dict。
                # 例如： {"$sort": {"_id.city": 1}}
                sort_stage["$sort"][field_name] = direction
            # 最後把這個 $sort stage 加入 aggregation pipeline。
            # 這樣 MongoDB 在執行 $group 後就會根據 _id.city 排序群組。
            pipeline.append(sort_stage)

        # ------------------
        # 5. $skip + $limit
        # ------------------
        if parsed.get("limit"):
            offset = parsed["limit"].get("offset", 0)
            limit = parsed["limit"].get("limit")
            if offset > 0:
                pipeline.append({"$skip": offset})
            if limit is not None:
                pipeline.append({"$limit": limit})

        return pipeline


    # -------------------------------
    # transform filter
    # -------------------------------
    def transform_filter(self, ast):
        node_type = ast["type"]

        if node_type == "condition":
            return self.transform_condition(ast)

        if node_type in ("and", "or"):
            # 支持多條件列表
            return {self.LOGIC_MAP[node_type]: [self.transform_filter(cond) for cond in ast.get("conditions", [])]}

        if node_type == "not":
            return {"$nor": [self.transform_filter(ast["condition"])]}

        raise ValueError(f"Unknown AST node type: {node_type}")

    # -------------------------------
    # transform condition
    # -------------------------------
    def transform_condition(self, node):
        field = node["field"]
        op = node["op"]
        value = node["value"]

        if isinstance(value, date) and not isinstance(value, datetime):
            # 因為你 DATE() 用的是 $dateToString → 字串比較最安全
            value = value.strftime("%Y-%m-%d")
        
        # 函數欄位
        if isinstance(field, dict) and field.get("type") == "function":
            expr_field = self.transform_function(field)
            mongo_op = self.OP_MAP.get(op)
            if mongo_op is None:
                raise ValueError(f"Unsupported operator: {op}")
            return {"$expr": {mongo_op: [expr_field, value]}}

        # LIKE
        if op == "like":
            pattern = str(value)
            if pattern.startswith("%") and pattern.endswith("%"):
                regex = f".*{re.escape(pattern[1:-1])}.*"
            elif pattern.startswith("%"):
                regex = f".*{re.escape(pattern[1:])}"
            elif pattern.endswith("%"):
                regex = f"{re.escape(pattern[:-1])}.*"
            else:
                regex = re.escape(pattern)
            return {field: {"$regex": regex}}

        # 其他操作符
        mongo_op = self.OP_MAP.get(op)
        if mongo_op is None:
            raise ValueError(f"Unsupported operator: {op}")
        return {field: {mongo_op: value}}

    # -------------------------------
    # transform function
    # -------------------------------
    def transform_function(self, field):
        func = field["name"].upper()
        args = field["args"]

        # 日期函數
        if func in self.DATE_FUNCS:
            if func == "YEAR":
                return {"$year": f"${args[0]}"}
            if func == "MONTH":
                return {"$month": f"${args[0]}"}
            if func == "DATE":
                return {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": f"${args[0]}"
                    }
                }

        # 字串函數
        if func in self.STRING_FUNCS:
            if func == "UPPER":
                return {"$toUpper": f"${args[0]}"}
            if func == "LOWER":
                return {"$toLower": f"${args[0]}"}
            if func == "CONCAT":
                expr_args = []
                for a in args:
                    # 欄位一律轉成字串
                    if isinstance(a, str):
                        expr_args.append({"$toString": f"${a}"})
                    else:
                        # 常數也轉成字串，最安全
                        expr_args.append({"$toString": a})
                return {"$concat": expr_args}

        # 數值函數
        if func in self.NUMERIC_FUNCS:
            if func == "ROUND":
                n = args[1] if len(args) > 1 else 0
                return {"$round": [f"${args[0]}", n]}
            if func == "CEIL":
                return {"$ceil": f"${args[0]}"}
            if func == "FLOOR":
                return {"$floor": f"${args[0]}"}

        raise ValueError(f"Unsupported function: {func}")

    # -------------------------------
    # 格式化函數欄位名稱
    # -------------------------------
    def format_field_name(self, field):
        if isinstance(field, str):
            return field
        if isinstance(field, dict) and field.get("type") == "function":
            args = ", ".join(str(a) for a in field["args"])
            return f"{field['name']}({args})"
        return str(field)
