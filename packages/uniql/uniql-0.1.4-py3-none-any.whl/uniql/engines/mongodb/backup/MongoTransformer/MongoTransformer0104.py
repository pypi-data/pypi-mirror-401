import re

class MongoTransformer:
    # 單欄位比較對應
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

    def transform(self, ast):
        """
        將 AST 轉成 MongoDB 查詢 dict
        """
        node_type = ast["type"]

        if node_type == "condition":
            return self.transform_condition(ast)

        if node_type in ("and", "or"):
            return {self.LOGIC_MAP[node_type]: [self.transform(ast["left"]), self.transform(ast["right"])]}

        if node_type == "not":
            # MongoDB $not 需要配合欄位，使用 $nor 包整個條件比較簡單
            return {"$nor": [self.transform(ast["condition"])]}

        raise ValueError(f"Unknown AST node type: {node_type}")

    def transform_condition(self, node):
        field = node["field"]
        op = node["op"]
        value = node["value"]

        # 處理函數欄位
        if isinstance(field, dict) and field.get("type") == "function":
            expr_field = self.transform_function(field)
            mongo_op = self.OP_MAP.get(op)
            if mongo_op is None:
                raise ValueError(f"Unsupported operator: {op}")
            return {"$expr": {mongo_op: [expr_field, value]}}

        # LIKE 特殊處理
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

    def transform_function(self, field):
        """
        將函數欄位轉 MongoDB 表達式，用於 $expr
        例子:
            {"type":"function","name":"YEAR","args":["created_at"]}
            → {"$year": "$created_at"}
        """
        func = field["name"].upper()
        args = field["args"]

        # 只處理單參數函數
        if func in self.DATE_FUNCS:
            mongo_func_map = {"YEAR": "$year", "MONTH": "$month", "DATE": "$dayOfMonth"}
            return {mongo_func_map[func]: f"${args[0]}"}

        if func in self.STRING_FUNCS:
            if func == "UPPER":
                return {"$toUpper": f"${args[0]}"}
            if func == "LOWER":
                return {"$toLower": f"${args[0]}"}
            if func == "CONCAT":
                # MongoDB $concat 接收列表
                expr_args = [f"${a}" if isinstance(a, str) else a for a in args]
                return {"$concat": expr_args}

        if func in self.NUMERIC_FUNCS:
            if func == "ROUND":
                # MongoDB $round 接收 [value, place]
                x = args[0]
                n = args[1] if len(args) > 1 else 0
                return {"$round": [f"${x}", n]}
            if func == "CEIL":
                return {"$ceil": f"${args[0]}"}
            if func == "FLOOR":
                return {"$floor": f"${args[0]}"}

        raise ValueError(f"Unsupported function: {func}")
