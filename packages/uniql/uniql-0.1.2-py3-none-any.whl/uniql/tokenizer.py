import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Tokenizer:
    """
    將查詢條件字串轉成 token stream
    """

    # 運算子順序必須長的在前（避免 >= 被拆成 > =）
    OPERATORS = ["!=", ">=", "<=", "=", ">", "<"]

    KEYWORDS = {
        "AND": "AND",
        "OR": "OR",
        "NOT": "NOT",
        "in": "IN",
        "not": "NOT",
    }

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.length = len(text)

    # ------------------------------------
    # 基本工具
    # ------------------------------------
    def peek(self):
        """查看目前字元"""
        if self.pos >= self.length:
            return None
        return self.text[self.pos]

    def advance(self):
        """指標往前一格"""
        ch = self.peek()
        self.pos += 1
        return ch

    def match(self, string):
        """判斷接下來的字串是否符合指定內容"""
        end = self.pos + len(string)
        return self.text[self.pos:end] == string

    def skip_whitespace(self):
        while self.peek() and self.peek().isspace():
            self.advance()

    # ------------------------------------
    # 主入口
    # ------------------------------------
    def tokenize(self):
        tokens = []

        while self.pos < self.length:
            self.skip_whitespace()
            ch = self.peek()

            if ch is None:
                break

            # 括號
            if ch == "(":
                tokens.append(Token("LPAREN", "("))
                self.advance()
                continue
            if ch == ")":
                tokens.append(Token("RPAREN", ")"))
                self.advance()
                continue

            # 逗號
            if ch == ",":
                tokens.append(Token("COMMA", ","))
                self.advance()
                continue

            # list 開頭 '['
            if ch == "[":
                list_text = self.read_list()
                tokens.append(Token("LIST", list_text))
                continue

            # 字串
            if ch in ['"', "'"]:
                tokens.append(Token("STRING", self.read_string()))
                continue

            # 數字
            if ch.isdigit():
                tokens.append(Token("NUMBER", self.read_number()))
                continue

            # 運算子（先比對 multi-char）
            op = self.match_operator()
            if op:
                tokens.append(Token("OP", op))
                self.pos += len(op)
                continue

            # 識別字、關鍵字（AND, OR, NOT, in）
            if ch.isalpha() or ch == "_":
                word = self.read_identifier()
                upper = word.upper()

                # special: not in
                if upper == "NOT" and self.match(" in"):
                    self.pos += 3  # skip " in"
                    tokens.append(Token("OP", "not in"))
                    continue

                # keyword
                if upper in ["AND", "OR", "NOT"]:
                    tokens.append(Token(upper, upper))
                    continue

                if upper == "LIKE":
                    tokens.append(Token("OP", "like"))
                    continue

                if word == "in":
                    tokens.append(Token("OP", "in"))
                    continue

                tokens.append(Token("IDENT", word))
                continue

            raise ValueError(f"Unknown character at {self.pos}: {ch}")

        return tokens

    # ------------------------------------
    # Token readers
    # ------------------------------------
    def read_string(self):
        quote = self.advance()  # consume " or '
        result = ""

        while True:
            ch = self.advance()
            if ch is None:
                raise ValueError("Unterminated string literal")

            if ch == quote:
                break
            result += ch

        return result

    def read_number(self):
        start = self.pos
        while self.peek() and (self.peek().isdigit() or self.peek() == "."):
            self.advance()
        num = self.text[start:self.pos]

        # int or float
        return float(num) if "." in num else int(num)

    def read_identifier(self):
        start = self.pos
        while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
            self.advance()
        return self.text[start:self.pos]

    def read_list(self):
        """
        回傳 list 的完整文本，例如：["a", "b"]
        parser 再解析成 Python list
        """
        start = self.pos
        depth = 0

        while True:
            ch = self.advance()
            if ch is None:
                raise ValueError("Unterminated list literal")

            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    break

        return self.text[start:self.pos]

    def match_operator(self):
        """比對 >=、<= 等多字元 operator"""
        for op in self.OPERATORS:
            if self.match(op):
                return op
        return None

if __name__ == "__main__":
    t = Tokenizer('age >= 25 AND (city = "Taipei" OR score < 100)')
    print(t.tokenize())