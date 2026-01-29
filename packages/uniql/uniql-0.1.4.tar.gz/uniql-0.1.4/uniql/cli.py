import typer
import json
from .parser import QueryParser
from .evaluator import QueryEvaluator
from .engines.mongodb.MongoTransformer import MongoTransformer
import random
from pymongo import MongoClient
from .commands import eval_cmd, mongodb_cmd, tinydb_cmd

app = typer.Typer()
app.add_typer(eval_cmd.app, name="eval")
app.add_typer(mongodb_cmd.app, name="mongodb")
app.add_typer(tinydb_cmd.app, name="tinydb")

if __name__ == "__main__":
    app()
