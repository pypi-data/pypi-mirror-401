"""Scan Python files for model classes."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Dict


def scan_file(filepath: str) -> dict:
    """Parse a Python file and return detected framework and model AST nodes."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    tree = ast.parse(path.read_text(encoding="utf-8"))
    framework = detect_framework(tree)
    models = extract_models(tree, framework)

    return {"framework": framework, "models": models}


def detect_framework(ast_tree: ast.AST) -> str:
    """Detect framework based on imports in the AST."""
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = {alias.name for alias in node.names}

            if module == "django.db" and ("models" in names or "Model" in names):
                return "django"
            if module.startswith("django.db.models"):
                return "django"
            if module.startswith("sqlalchemy") and (
                "Column" in names
                or "declarative_base" in names
                or "Mapped" in names
                or "DeclarativeBase" in names
            ):
                return "sqlalchemy"
            if module == "pydantic" and "BaseModel" in names:
                return "pydantic"
            if module == "pydantic.v1" and "BaseModel" in names:
                return "pydantic"

    raise ValueError("Could not detect framework from imports.")


def extract_models(ast_tree: ast.AST, framework: str) -> Dict[str, ast.ClassDef]:
    """Extract model classes based on framework conventions."""
    models: Dict[str, ast.ClassDef] = {}

    for node in ast.walk(ast_tree):
        if not isinstance(node, ast.ClassDef):
            continue

        if _is_model_class(node, framework):
            models[node.name] = node

    return models


def _is_model_class(node: ast.ClassDef, framework: str) -> bool:
    base_names = {""}
    for base in node.bases:
        if isinstance(base, ast.Attribute):
            base_names.add(base.attr)
        elif isinstance(base, ast.Name):
            base_names.add(base.id)
        elif isinstance(base, ast.Subscript):
            if isinstance(base.value, ast.Name):
                base_names.add(base.value.id)

    if framework == "django":
        return "Model" in base_names
    if framework == "sqlalchemy":
        return "Base" in base_names or "DeclarativeBase" in base_names
    if framework == "pydantic":
        return "BaseModel" in base_names

    return False
