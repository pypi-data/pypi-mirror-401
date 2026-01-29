from tinydb import TinyDB, Query
from tinydb.operations import set
from ...parser import QueryParser

class TinyDBTransformer:
    def __init__(self, db_path):
        self.db = TinyDB(db_path)
        self.q = Query()

    def transform_to_query(self, ast):
        """
        將 AST 中的 filter 部分轉成 TinyDB Query
        """
        return self._build_query(ast)

    def _build_query(self, node):
        node_type = node["type"]

        if node_type == "and":
            queries = [self._build_query(child) for child in node["conditions"]]
            result = queries[0]
            for q in queries[1:]:
                result = result & q
            return result

        if node_type == "or":
            queries = [self._build_query(child) for child in node["conditions"]]
            result = queries[0]
            for q in queries[1:]:
                result = result | q
            return result

        if node_type == "not":
            return ~(self._build_query(node["condition"]))

        if node_type == "condition":
            field = node["field"]
            op = node["op"]
            value = node["value"]

            if op == "=":
                return self.q[field] == value
            if op == "!=":
                return self.q[field] != value
            if op == ">":
                return self.q[field] > value
            if op == "<":
                return self.q[field] < value
            if op == ">=":
                return self.q[field] >= value
            if op == "<=":
                return self.q[field] <= value
            if op == "in":
                return self.q[field].one_of(value)
            if op == "not in":
                return ~self.q[field].one_of(value)
            if op == "like":
                # TinyDB 沒有 like, 可以用 test + lambda
                return self.q[field].test(lambda v: self._match_like(v, value))

        raise ValueError(f"Unknown node type: {node_type}")

    def _match_like(self, field_value, pattern):
        if pattern.startswith("%") and pattern.endswith("%"):
            return pattern[1:-1] in field_value
        if pattern.startswith("%"):
            return field_value.endswith(pattern[1:])
        if pattern.endswith("%"):
            return field_value.startswith(pattern[:-1])
        return field_value == pattern

    def execute(self, ast, select=None, order_by=None, limit=None):
        query = self.transform_to_query(ast)
        results = self.db.search(query)

        # TODO: 可以加 project / order_by / limit
        if select:
            results = [
                {f: row[f] for f in select["fields"]}
                for row in results
            ]

        if order_by:
            for order in reversed(order_by):
                field = order["field"]
                reverse = order["direction"].lower() == "desc"
                results.sort(key=lambda r: r.get(field), reverse=reverse)

        if limit:
            offset = limit.get("offset", 0)
            results = results[offset : offset + limit["limit"]]

        return results
