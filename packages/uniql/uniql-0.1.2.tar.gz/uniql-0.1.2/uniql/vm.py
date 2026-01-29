from .bytecode import OpCode
from datetime import datetime, date
import math

class VM:
    """
    VM 執行器：負責執行 bytecode 並對每一筆 row 返回 True/False
    """
    # 參數意思
    # code：像這樣的 list
    # [
    # (OpCode.LOAD_FIELD, "age"),
    # (OpCode.LOAD_CONST, 18),
    # (OpCode.GE, None),
    # (OpCode.RETURN, None)
    # ]
    # row：一筆資料
    # {"name": "Alice", "age": 20}
    def run(self, code, row):
        stack = [] # stack
        ip = 0  # instruction pointer，指向「現在跑到哪一條指令」

        while ip < len(code): # 一次一條指令
            # 假如
            # (OpCode.LOAD_FIELD, "age")
            # opcode = OpCode.LOAD_FIELD
            # arg = "age"
            # row.get(arg) -> 20
            # push 到 stack -> [20]
            # ip += 1
            # 繼續下一條指令
            opcode, arg = code[ip]

            if opcode == OpCode.LOAD_FIELD:
                stack.append(row.get(arg))
            elif opcode == OpCode.LOAD_CONST:
                stack.append(arg)
            elif opcode == OpCode.EQ: # 等
                # 為什麼先 pop b 再 pop a？
                # 因為 stack 是：[a, b]
                b = stack.pop()
                a = stack.pop()
                stack.append(a == b)
            elif opcode == OpCode.NE: # 不等
                b = stack.pop()
                a = stack.pop()
                stack.append(a != b)
            elif opcode == OpCode.GT: # 大於
                b = stack.pop()
                a = stack.pop()
                stack.append(a > b)
            elif opcode == OpCode.LT: # 小於
                b = stack.pop()
                a = stack.pop()
                stack.append(a < b)
            elif opcode == OpCode.GE: # 大於等
                b = stack.pop()
                a = stack.pop()
                stack.append(a >= b)
            elif opcode == OpCode.LE: # 小於等
                b = stack.pop()
                a = stack.pop()
                stack.append(a <= b)

            # --------------------------
            # 集合操作
            # --------------------------
            elif opcode == OpCode.IN:
                b = stack.pop()  # list 或 set
                a = stack.pop()  # value
                stack.append(a in b)
            elif opcode == OpCode.NOT_IN:
                b = stack.pop()
                a = stack.pop()
                stack.append(a not in b)

            # --------------------------
            # LIKE 操作
            # --------------------------
            elif opcode == OpCode.LIKE:
                pattern = stack.pop()
                value = stack.pop()
                stack.append(self.match_like(value, pattern))

            # --------------------------
            # 邏輯運算
            # --------------------------
            elif opcode == OpCode.AND:
                b = stack.pop()
                a = stack.pop()
                stack.append(a and b)
            elif opcode == OpCode.OR:
                b = stack.pop()
                a = stack.pop()
                stack.append(a or b)
            elif opcode == OpCode.NOT:
                a = stack.pop()
                stack.append(not a)

            # --------------------------
            # 函數運算
            # --------------------------
            elif opcode == OpCode.YEAR:
                a = stack.pop()
                stack.append(self.to_datetime(a).year)
            elif opcode == OpCode.MONTH:
                a = stack.pop()
                stack.append(self.to_datetime(a).month)
            elif opcode == OpCode.DATE:
                a = stack.pop()
                stack.append(self.to_datetime(a).date())
            elif opcode == OpCode.UPPER:
                a = stack.pop()
                stack.append(str(a).upper())
            elif opcode == OpCode.LOWER:
                a = stack.pop()
                stack.append(str(a).lower())
            elif opcode == OpCode.CONCAT:
                # 支援多個參數，先 pop 所有
                n = arg if arg else 2  # 默認 2 個參數，可自行調整
                items = [stack.pop() for _ in range(n)]
                items.reverse()
                stack.append("".join(str(i) for i in items))
            elif opcode == OpCode.ROUND:
                x = stack.pop()
                n = stack.pop() if stack else 0
                stack.append(round(x, n))
            elif opcode == OpCode.CEIL:
                x = stack.pop()
                stack.append(math.ceil(x))
            elif opcode == OpCode.FLOOR:
                x = stack.pop()
                stack.append(math.floor(x))

            # --------------------------
            # RETURN 指令
            # --------------------------
            elif opcode == OpCode.RETURN:
                return stack.pop()
            else:
                raise RuntimeError(f"Unknown opcode: {opcode}")

            ip += 1

        raise RuntimeError("No RETURN instruction")

    def match_like(self, value, pattern):
        if value is None:
            return False

        value = str(value)
        pattern = str(pattern)

        if pattern.startswith("%") and pattern.endswith("%"):
            return pattern[1:-1] in value
        if pattern.startswith("%"):
            return value.endswith(pattern[1:])
        if pattern.endswith("%"):
            return value.startswith(pattern[:-1])
        return value == pattern

    def to_datetime(self, value):
        """把日期/字串轉成 datetime"""
        if isinstance(value, datetime):
            return value
        if isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        raise ValueError(f"Cannot convert to datetime: {value}")
