# See BNF.md for more information
import re
import ast
from ...tokenizer import Tokenizer
from datetime import datetime

class QueryParser:

    # 允許的運算子
    OPERATORS = ["!=", ">=", "<=", "=", ">", "<", "in", "not in", "like"]

    def parse(self, query: str):
        """
        COLLECTION / CONDITION / SELECT / ORDER BY / GROUP BY ->
        Parse query:
        users / age > 25 AND city = Taipei / select name
        - 探索型指令: users / show types, users / sample 5, users / head 3
        """

        parts = [p.strip() for p in query.split("/")]
      
        collection = parts[0]
        
        # --------------------------
        # 探索型指令（show/sample/head/count/stats/unique）
        # --------------------------
        if len(parts) > 1:
            second = parts[1].lower()
            if second.startswith("show types"):
                return {
                    "collection": collection,
                    "command": "show types"
                }
            elif second.startswith("sample"):
                try:
                    n = int(second.split()[1])
                except:
                    n = 1
                return {
                    "collection": collection,
                    "command": "sample",
                    "sample_count": n
                }
            elif second.startswith("head"):
                try:
                    n = int(second.split()[1])
                except:
                    n = 5
                return {
                    "collection": collection,
                    "command": "head",
                    "head_count": n
                }
            elif second.startswith("count"):
                fields = [f.strip() for f in second[len("count"):].split(",") if f.strip()]
                return {"collection": collection, "command": "count", "fields": fields}
            elif second.startswith("stats"):
                fields = [f.strip() for f in second[len("stats"):].split(",") if f.strip()]
                return {"collection": collection, "command": "stats", "fields": fields}
            elif second.startswith("unique"):
                fields = [f.strip() for f in second[len("unique"):].split(",") if f.strip()]
                return {"collection": collection, "command": "unique", "fields": fields}

        
        if len(parts) < 3:
            raise ValueError("Query must have 3 parts: COLLECTION / CONDITION / SELECT")

        condition = self.parse_condition(parts[1])
        select_part = parts[2]
        # order_part = parts[3] if len(parts) > 3 else None
        # group_part = parts[4] if len(parts) > 4 else None
        order_part = None
        group_part = None
        limit_part = None

        for part in parts[3:]:
            part_lower = part.lower()
            if part_lower.startswith("order by"):
                order_part = part
            elif part_lower.startswith("group by"):
                group_part = part
            elif part_lower.startswith("limit"):
                limit_part = part


        select = self.parse_select(select_part)
        order_by = self.parse_order_by(order_part) if order_part else []
        group_by = self.parse_group_by(group_part) if group_part else []
        limit = self.parse_limit(limit_part) if limit_part else None

        return {
            "collection": collection,
            "filter": condition,
            "select": select,
            "order_by": order_by,
            "group_by": group_by,
            "limit": limit
        }

    # region CONDITION 
    # -------------------------------
    #   CONDITION PARSER
    # -------------------------------
    
    # endregion
    def parse_condition(self, segment: str):
        self.tokens = Tokenizer(segment).tokenize()
        self.pos = 0
        node = self.parse_boolean_expr()

        if self.peek() is not None:
            raise ValueError("Unexpected token: " + str(self.peek()))

        return node
    

    # region BOOLEAN EXPRESSION
    def parse_boolean_expr(self):
        """
        對應語法
        <boolean_expr> ::= <boolean_term> ("OR" <boolean_term>)*
        """
        node = self.parse_boolean_term()

        while self.match("OR"):
            right = self.parse_boolean_term()
            node = {
                "type": "or",
                "conditions": [node, right]
            }

        return node
    # endregion

    # region BOOLEAN TERM
    def parse_boolean_term(self):
        """
        對應語法
        <boolean_term> ::= <predicate> ("AND" <predicate>)*
        """
        node = self.parse_boolean_factor()

        while self.match("AND"):
            right = self.parse_boolean_factor()
            node = {
                "type": "and",
                "conditions": [node, right]
            }

        return node
    # endregion

    # region BOOLEAN_Factor
    def parse_boolean_factor(self):
        """
        語意
        例如：NOT age > 25 AND city = "Taipei"
        語意應該是：(NOT (age > 25)) AND (city = "Taipei")
        而不是：NOT ((age > 25 AND city = "Taipei"))
        因為NOT的優先級比AND高,要最先處理
        """
        # NOT <facotr>
        if self.match("NOT"): #判別Token是否為NOT
            operand = self.parse_boolean_factor()
            return {
                "type": "not",
                "condition": operand
            }
        
        # <boolean_exper>
        if self.match("LPAREN"):
            node = self.parse_boolean_expr()
            self.expect("RPAREN")
            return node

        """
        什麼時候會走到這裡？
        沒有NOT,沒有括號，例如
        age > 25
        city = "Taipei"
        """
        return self.parse_predicate()
    # endregion

    # region PREDICATE
    def parse_predicate(self):
        """
        對應語法
        <predicate> ::= IDENT OP VALUE。
        expect("IDENT") → 欄位名稱。
        expect("OP") → 運算子，例如 >, = 等。
        parse_value_token() → 解析值（NUMBER、STRING、LIST）。
        """
        field = self.parse_field()
        op = self.expect("OP")
        value = self.parse_value_token()

        return {
            "type": "condition",
            "field": field,
            "op": op,
            "value": value
        }
    # endregion

    # region FIELD
    def parse_field(self):
        """
        支援範例：
        - YEAR(created_at)
        - MONTH(created_at)
        - DATE(created_at)
        這一步只做一件事
        👉 判斷現在看到的是：
        age
        還是 YEAR(age)
        """

        name = self.expect("IDENT")

        # 如果後面接 '('，代表是 function
        if self.match("LPAREN"):
            args = []

            # 讀取參數（可以是欄位或數字）
            while True:
                tok = self.peek()
                if tok.type == "IDENT":
                    args.append(self.expect("IDENT"))
                elif tok.type == "NUMBER":
                    args.append(self.expect("NUMBER"))
                elif tok.type == "STRING":
                    args.append(self.expect("STRING"))
                else:
                    raise ValueError(f"Unexpected token in function args: {tok}")

                if self.match("COMMA"):
                    continue
                else:
                    break

            self.expect("RPAREN")

            return {
                "type": "function",
                "name": name.upper(),
                "args": args
            }

        # 否則就是一般欄位
        return name
    # endregion





    # region VALUE
    # -------------------------------
    #   VALUE PARSER
    # -------------------------------
    def parse_value(self, value: str):
        """
        將值轉成 int/float/string/list
        """

        # 引號字串
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]

        # list: ["a", "b"]
        if value.startswith("[") and value.endswith("]"):
            inside = value[1:-1].strip()
            if not inside:
                return []
            return [self.parse_value(v.strip()) for v in inside.split(",")]

        # int
        if value.isdigit():
            return int(value)

        # float
        try:
            return float(value)
        except:
            pass

        # fallback: string
        return value
    # endregion

    # region SELECT
    # -------------------------------
    #   SELECT PARSER
    # -------------------------------
    def parse_select(self, segment: str):
        if not segment.lower().startswith("select"):
            raise ValueError("Select clause must start with 'select'")

        raw = segment[len("select"):].strip()

        distinct = False
        if raw.lower().startswith("distinct"):
            distinct = True
            raw = raw[len("distinct"):].strip()

        # ⭐ 關鍵：用 tokenizer + parse_field
        self.tokens = Tokenizer(raw).tokenize()
        self.pos = 0

        fields = []

        while self.pos < len(self.tokens):
            field = self.parse_field()
            fields.append(field)

            # 吃掉逗號（如果有）
            if self.match("COMMA"):
                continue
            else:
                break

        return {
            "fields": fields,
            "distinct": distinct
        }

    # endregion

    # region ORDER BY
    # -------------------------------
    #   ORDER BY PARSER
    # -------------------------------
    def parse_order_by(self, segment: str):
        if not segment.lower().startswith("order by"):
            raise ValueError("ORDER BY clause must start with 'order by'")
        
        raw = segment[len("order by"):].strip() # 去除前綴order by字眼
        fields = [f.strip() for f in raw.split(",")] #將欄位字串用逗號 , 分割，支援多欄位排序。
        order_by = [] # 儲存排序欄位

        for field in fields:
            parts = field.split() # 將欄位字串用空格分割
            col = parts[0] # 第一個元素為欄位名
            direction = "asc" # 預設為升序
            if len(parts) > 1: #如果有第二個元素，就把它當作排序方向（升冪或降冪）。
                direction = parts[1].lower()
                if direction not in ("asc", "desc"):
                    raise ValueError(f"Invalid order direction: {parts[1]}")
            order_by.append({"field": col, "direction": direction})
        
        return order_by
    # endregion

    # region Group By
    # -------------------------------
    #   ORDER BY PARSER
    # -------------------------------
    def parse_group_by(self, segment: str):
        if not segment.lower().startswith("group by"):
            raise ValueError("GROUP BY clause must start with 'group by'")

        raw = segment[len("group by"):].strip() # 去除前綴order by字眼
        fields = [f.strip() for f in raw.split(",") if f.strip()] #將欄位字串用逗號 , 分割，支援多欄位排序。
        return fields
    # endregion

    # region Limit
    # -------------------------------
    #   LIMIT PARSER
    # -------------------------------
    def parse_limit(self, segment: str):
        """
        支援：
        limit 10
        limit 10 offset 5
        """
        raw = segment.lower().strip()
        parts = raw.split()

        limit = None
        offset = 0

        if parts[0] != "limit":
            raise ValueError("LIMIT clause must start with 'limit'")

        limit = int(parts[1]) # limit必須為數字

        if "offset" in parts: # 如果有offset
            idx = parts.index("offset")  # 找到offset的位置
            offset = int(parts[idx + 1]) # offset必須為數字

        return {
            "limit": limit,
            "offset": offset
        }
    # endregion
    
    # region TOKEN
    # =============================
    #   Parser 專用：Token 操作
    # =============================
    def peek(self):
        """回傳目前 token，不前進"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        """消耗目前 token，往後移"""
        tok = self.peek()
        if tok:
            self.pos += 1
        return tok

    def match(self, token_type):
        """
        如果符合指定 token type，消耗並回傳 True
        否則 False
        """
        tok = self.peek()
        if tok and tok.type == token_type:
            self.advance()
            return True
        return False

    def expect(self, token_type):
        """
        強制要求下一個 token 為指定 type，不然 throw error
        並回傳 token.value
        """
        tok = self.peek()
        if tok and tok.type == token_type:
            self.advance()
            return tok.value
        raise ValueError(f"Expected {token_type}, got {tok}")

    def parse_value_token(self):
        tok = self.peek()

        if tok is None:
            raise ValueError("Unexpected end of input when reading value")

        # STRING: "Taipei"
        if tok.type == "STRING":
            self.advance()
            val = tok.value

            # 嘗試轉成日期（YYYY-MM-DD）
            try:
                date_val = datetime.strptime(val, "%Y-%m-%d").date()
                return date_val
            except:
                pass

            return val

        # NUMBER: 25, 3.14
        if tok.type == "NUMBER":
            self.advance()
            return tok.value

        # LIST: ["a","b"]
        if tok.type == "LIST":
            self.advance()
            # 丟回去用 Python ast 解析即可
            return ast.literal_eval(tok.value)

        raise ValueError(f"Unexpected token in value: {tok}")
    # endregion


# region TEST
# --- quick test ---
if __name__ == "__main__":
    parser = QueryParser()

    # q = 'users / age > 25 AND city = "Taipei" / select name, age'
    q = 'users / NOT (age > 25 AND city = "Taipei") / select name, age / order by age desc / group by city'
    # q = 'users / YEAR(created_at) = 2024 AND MONTH(created_at) > 6 / select name'

    result = parser.parse(q)
    print(result)
# endregion