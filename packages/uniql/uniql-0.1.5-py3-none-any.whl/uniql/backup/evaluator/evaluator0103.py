from collections import defaultdict
from datetime import datetime, date
import math
from .bytecode_compiler import BytecodeCompiler
from .vm import VM

class QueryEvaluator:
    def eval_with_vm(self, ast, row):
        """
        使用 bytecode + VM 來執行 WHERE 條件
        """
        compiler = BytecodeCompiler()
        code = compiler.compile(ast)

        vm = VM()
        return vm.run(code, row)
    
    # def eval(self, node, row):
    #     node_type = node["type"]

    #     if node_type == "and":
    #         return all(self.eval(child, row) for child in node["conditions"])

    #     if node_type == "or":
    #         return any(self.eval(child, row) for child in node["conditions"])

    #     if node_type == "not":
    #         return not self.eval(node["condition"], row)

    #     if node_type == "condition":
    #         return self.eval_condition(node, row)

    #     raise ValueError(f"Unknown node type: {node_type}")

    # =================================================
    # NEW：欄位 / 函數求值
    # =================================================
    def eval_field(self, field, row):
        """
        field:
        - "age"
        - {"type": "function", "name": "YEAR", "args": ["created_at"]}
        """

        # 普通欄位
        if isinstance(field, str):
            return row.get(field)

        if isinstance(field, dict) and field.get("type") == "function":
            func = field["name"]
            args = field["args"]

            # 遍歷 args，欄位取 row，數字/字串直接用
            values = []
            for arg in args:
                if isinstance(arg, str) and arg in row:
                    values.append(row[arg])
                else:
                    values.append(arg)

            if any(v is None for v in values):
                return None

            # 日期函數
            if func in ("YEAR", "MONTH", "DATE"):
                return self.apply_date_function(func, values[0])

            # 字串函數
            if func in ("UPPER", "LOWER", "CONCAT"):
                return self.apply_string_function(func, values)

            # 數值函數
            if func in ("ROUND", "CEIL", "FLOOR"):
                return self.apply_numeric_function(func, values)

            raise ValueError(f"Unsupported function: {func}")

        raise ValueError(f"Invalid field: {field}")


    # =================================================
    # NEW：數值函數實作
    # =================================================
    def apply_numeric_function(self, func, values):
        """
        數值函數：
        - ROUND(x[, n]) : 四捨五入到 n 位小數（n 可省略，預設 0）
        - CEIL(x)      : 無條件進位
        - FLOOR(x)     : 無條件捨去
        """
        if func == "ROUND":
            x = values[0]
            n = values[1] if len(values) > 1 else 0
            return round(x, n)
        elif func == "CEIL":
            return math.ceil(values[0])
        elif func == "FLOOR":
            return math.floor(values[0])
        else:
            raise ValueError(f"Unsupported numeric function: {func}")


    # =================================================
    # NEW：日期函數實作
    # =================================================
    def apply_date_function(self, func, value):
        """
        value 可以是：
        - datetime
        - date
        - ISO string: "2024-08-01"
        """

        # 字串 → datetime
        if isinstance(value, str):
            value = datetime.fromisoformat(value)

        if isinstance(value, date) and not isinstance(value, datetime):
            value = datetime.combine(value, datetime.min.time())

        if func == "YEAR":
            return value.year

        if func == "MONTH":
            return value.month

        if func == "DATE":
            return value.date()

        raise ValueError(f"Unsupported function: {func}")

    def apply_string_function(self, func, values):
        """
        values: list[str]
        """

        if func == "UPPER":
            return str(values[0]).upper()

        if func == "LOWER":
            return str(values[0]).lower()

        if func == "CONCAT":
            return "".join(str(v) for v in values)

        raise ValueError(f"Unsupported string function: {func}")


    # ----------------------------
    # 條件比較
    # ----------------------------
    # def eval_condition(self, node, row):
    #     field_value = self.eval_field(node["field"], row)
    #     op = node["op"]
    #     value = node["value"]

    #     if field_value is None:
    #         return False

    #     if op == "=":
    #         return field_value == value
    #     if op == "!=":
    #         return field_value != value
    #     if op == ">":
    #         return field_value > value
    #     if op == "<":
    #         return field_value < value
    #     if op == ">=":
    #         return field_value >= value
    #     if op == "<=":
    #         return field_value <= value
    #     if op == "in":
    #         return field_value in value
    #     if op == "not in":
    #         return field_value not in value
    #     if op == "like":
    #         return self.match_like(field_value, value)

    #     raise ValueError(f"Unsupported operator: {op}")
 
 
    def match_like(self, field_value, pattern):
        if field_value is None:
            return False

        field_value = str(field_value)
        pattern = str(pattern)

        # %abc%
        if pattern.startswith("%") and pattern.endswith("%"):
            return pattern[1:-1] in field_value

        # %abc
        if pattern.startswith("%"):
            return field_value.endswith(pattern[1:])

        # abc%
        if pattern.endswith("%"):
            return field_value.startswith(pattern[:-1])

        # 完全比對
        return field_value == pattern


    def group_rows(self, rows, group_fields):
        """
        rows: 已經通過 WHERE 的資料
        group_fields: ["city", "age"]
        """
        groups = defaultdict(list)

        for row in rows:
            key = tuple(row.get(f) for f in group_fields)
            groups[key].append(row)

        return groups

    # =================================================
    # NEW：投影欄位（SELECT）
    # =================================================
    def project(self, row, fields):
        """
        將單列資料 row 投影成 SELECT 的結果。
        
        參數：
            row: dict，一列資料，例如 {"name": "Alice", "age": 30, "city": "Taipei"}
            fields: list，SELECT 欄位列表，可以是：
                - 普通欄位名稱，例如 "name", "age"
                - 函數欄位，例如 {"type": "function", "name": "CONCAT", "args": ["name", "city"]}
        
        回傳：
            dict，key 為欄位名稱（或函數名稱字串），value 為對應值
        """
        result = {}
        for field in fields:
            # 計算欄位的實際值（普通欄位或函數欄位）
            value = self.eval_field(field, row)
            # 將欄位名稱或函數欄位轉成可作為 dict key 的字串
            key = self.format_field_name(field)
            # 將欄位值放入結果
            result[key] = value
        return result

    def format_field_name(self, field):
        """
        將欄位轉成可當 dict key 的字串名稱。
        
        參數：
            field: 欄位，可以是字串或函數 dict
        
        回傳：
            str，可作為 dict key 的名稱
            - 普通欄位: 直接返回欄位名稱
            - 函數欄位: 返回 FUNC(arg1, arg2, ...) 的格式字串
        """
        if isinstance(field, str):
            # 普通欄位,直接返回欄位名稱
            return field
        
        if isinstance(field, dict) and field.get("type") == "function":
            # 函數欄位,組合函數名稱與參數
            args = ", ".join(str(a) for a in field["args"])
            return f"{field['name']}({args})"
        
        # 其他情況，轉成字串保險
        return str(field)

    # =================================================
    # NEW：整合 filter + select
    # =================================================
    def execute(self, ast, rows, select, order_by=None, group_by=None, limit=None):
        """
        ast: parser.parse(...)[\"filter\"]
        rows: list of dict
        select: dict, 例如 {"fields": ["name", "age"], "distinct": True}
        order_by: parser.parse(...)[\"order_by\"]，格式:
                  [{"field": "age", "direction": "asc"}, ...]
        group_by: parser.parse(...)[\"group_by\"]，格式: ["city", ...]
        """

        # 先過濾 + 投影
        fields_to_project = select["fields"] + (group_by if group_by else [])
        # print("ast:", fields_to_project)
        projected = [
            self.project(row, fields_to_project)
            for row in rows
            if self.eval_with_vm(ast, row)
        ]

        # --------------------
        # DISTINCT 處理
        # --------------------
        if select.get("distinct"):
            seen = set()
            unique = []
            for row in projected:
                key = tuple(row[f] for f in select["fields"])
                if key not in seen:
                    seen.add(key)
                    unique.append(row)
            projected = unique

        # 如果有 order_by，進行排序
        if order_by:
            for order in reversed(order_by):
                field = order["field"]
                reverse = order["direction"].lower() == "desc"
                projected.sort(key=lambda r: r.get(field), reverse=reverse)

        # 如果有 group_by，進行分組
        if group_by:
            grouped = defaultdict(list)
            for row in projected:
                key = tuple(row.get(field) for field in group_by)
                grouped[key].append(row)

            grouped_items = list(grouped.items()) # 轉成 list

            # LIMIT 套在 group 上
            if limit:
                offset = limit.get("offset", 0)
                grouped_items = grouped_items[offset : offset + limit["limit"]]

            return dict(grouped_items)

        # 如果有 limit，進行分頁
        if limit and not group_by:
            offset = limit.get("offset", 0)
            projected = projected[offset : offset + limit["limit"]]
            

        return projected
        
    


