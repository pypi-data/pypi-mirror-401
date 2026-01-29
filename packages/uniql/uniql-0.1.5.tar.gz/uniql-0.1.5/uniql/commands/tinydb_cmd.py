import typer
import json
from ..parser import QueryParser
from ..engines.tinydb.TinyDBTransformer import TinyDBTransformer

app = typer.Typer(help="TinyDB SimpleQL CLI")

# 指定 TinyDB 資料庫檔案
DB_PATH = "tinydb_data/db.json"

@app.command(name="")
def run(
    query_file: str = typer.Argument(..., help="SimpleQL 查詢檔案"),
    fields: str = typer.Option(None, help="選擇要顯示的欄位，逗號分隔")
):
    """
    用 TinyDB 執行 SimpleQL 查詢
    """
    # 讀取 SimpleQL 查詢
    with open(query_file, "r", encoding="utf-8") as f:
        query_str = f.read()

    # 解析
    parser = QueryParser()
    parsed = parser.parse(query_str)

    # TinyDB 轉換器
    transformer = TinyDBTransformer(DB_PATH)
    
    # 過濾結果
    ast_filter = parsed.get("filter", {})
    
    # SELECT 欄位
    select_fields = None
    if fields:
        select_fields = {"fields": [f.strip() for f in fields.split(",")]}

    results = transformer.execute(ast_filter, select=select_fields)

    # 輸出
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    app()
