import re

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

        # $match
        if "filter" in parsed:
            pipeline.append({"$match": self.transform_filter(parsed["filter"])})

        # $project
        if "select" in parsed and parsed["select"]["fields"]:
            project_stage = {"$project": {"_id": 0}}
            for f in parsed["select"]["fields"]:
                if isinstance(f, str):
                    project_stage["$project"][f] = f"${f}"
                elif isinstance(f, dict) and f.get("type") == "function":
                    project_stage["$project"][self.format_field_name(f)] = self.transform_function(f)
            pipeline.append(project_stage)

        # $sort
        if parsed.get("order_by"):
            sort_stage = {"$sort": {}}
            for o in parsed["order_by"]:
                direction = 1 if o["direction"] == "asc" else -1
                sort_stage["$sort"][o["field"]] = direction
            pipeline.append(sort_stage)

        # $skip + $limit
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
            mongo_func_map = {"YEAR": "$year", "MONTH": "$month", "DATE": "$dayOfMonth"}
            return {mongo_func_map[func]: f"${args[0]}"}

        # 字串函數
        if func in self.STRING_FUNCS:
            if func == "UPPER":
                return {"$toUpper": f"${args[0]}"}
            if func == "LOWER":
                return {"$toLower": f"${args[0]}"}
            if func == "CONCAT":
                expr_args = [f"${a}" if isinstance(a, str) else a for a in args]
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
