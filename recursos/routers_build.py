import os
import re
from pathlib import Path
import importlib
from fastapi import FastAPI


def routers_build(version: str, app: FastAPI):
    dir_path = Path(f"api/{version}/")
    for dir in os.listdir(dir_path):
        # regex to skip __pycache__ and __init__
        if re.search(r'__\w*__', dir):
            continue
        endpoint_path = f'{dir_path}.{dir}/endpoint'.replace('/', '.')
        module = importlib.import_module(f"{endpoint_path}.{dir}_endpoints")
        app.include_router(module.router)
