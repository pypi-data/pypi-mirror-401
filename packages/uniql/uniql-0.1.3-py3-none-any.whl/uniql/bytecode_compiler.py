from .bytecode import OpCode

class BytecodeCompiler:
    def compile(self, ast):
        self.code = [] # 用來存指令
        self.visit(ast) # 從 AST 的「根節點」開始走訪
        self.code.append((OpCode.RETURN, None)) # 最後加上 RETURN 指令
        return self.code

    def visit(self, node):
        if node is None: # 如果 AST 為空節點
            return

        node_type = node.get("type") # 取得節點類型

        if node_type == "condition": # 如果是條件節點
            self.compile_condition(node)
        elif node_type == "and": # 如果是 AND 節點
            # 編譯順序是：left（結果會 push 到 stack）
            # 再編 right（結果也 push），最後 AND
            # stack 變化：
            # [left_result, right_result]
            # → AND
            # → [True / False]
            self.visit(node["conditions"][0]) # 走訪左子樹
            self.visit(node["conditions"][1]) # 走訪右子樹
            self.code.append((OpCode.AND, None))
        # or/not 同理
        elif node_type == "or": #
            self.visit(node["conditions"][0])
            self.visit(node["conditions"][1])
            self.code.append((OpCode.OR, None))
        elif node_type == "not":
            self.visit(node["condition"])
            self.code.append((OpCode.NOT, None))
        # elif node_type == "not":
        #     self.visit(node["value"])
        #     self.code.append((OpCode.NOT, None))
        else: # 其他節點，編譯錯誤
            raise ValueError(f"Unknown AST node: {node_type}")


    # 假設 AST 是：
    # {
    # "type": "condition",
    # "field": "age",
    # "op": ">=",
    # "value": 18
    # }
    # LOAD_FIELD age
    # LOAD_CONST 18
    # GE
    def compile_condition(self, node):
        field = node["field"]
        # ------------------------------
        # 1. 處理函數欄位
        # ------------------------------
        if isinstance(field, dict) and field.get("type") == "function":
            func_name = field["name"]
            args = field["args"]
            # 先把每個參數 push 到 stack
            for arg in args:
                if isinstance(arg, str):
                    self.code.append((OpCode.LOAD_FIELD, arg))
                else:
                    # 如果參數是常數
                    self.code.append((OpCode.LOAD_CONST, arg))
            # 再加入對應的函數指令
            func_map = {
                "YEAR": OpCode.YEAR,
                "MONTH": OpCode.MONTH,
                "DATE": OpCode.DATE,
                "UPPER": OpCode.UPPER,
                "LOWER": OpCode.LOWER,
                "CONCAT": OpCode.CONCAT,
                "ROUND": OpCode.ROUND,
                "CEIL": OpCode.CEIL,
                "FLOOR": OpCode.FLOOR,
            }
            if func_name not in func_map:
                raise ValueError(f"Unsupported function: {func_name}")
            self.code.append((func_map[func_name], None))
        else:
            # 普通欄位直接 push
            self.code.append((OpCode.LOAD_FIELD, field))

        # ------------------------------
        # 2. 載入比較值
        # ------------------------------
        self.code.append((OpCode.LOAD_CONST, node["value"]))

        # ------------------------------
        # 3. 操作符對應
        # ------------------------------
        op_map = {
            "=": OpCode.EQ,
            "!=": OpCode.NE,
            ">": OpCode.GT,
            "<": OpCode.LT,
            ">=": OpCode.GE,
            "<=": OpCode.LE,
            "in": OpCode.IN,
            "not in": OpCode.NOT_IN,
            "like": OpCode.LIKE,
        }

        if node["op"] not in op_map:
            raise ValueError(f"Unsupported operator: {node['op']}")

        self.code.append((op_map[node["op"]], None))
