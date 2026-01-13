"""Analyze model class AST nodes to extract fields and relationships."""

from __future__ import annotations

import ast
from typing import Any, Dict, Optional


def analyze_model(model_class: ast.ClassDef, framework: str) -> dict:
    """Analyze a model class AST node for fields and relationships."""
    model_info = {
        "name": model_class.name,
        "framework": framework,
        "fields": {},
        "relationships": {},
    }

    if framework == "django":
        model_info["fields"] = extract_django_fields(model_class)
        model_info["relationships"] = detect_relationships(model_class, framework)
    elif framework == "sqlalchemy":
        model_info["fields"] = extract_sqlalchemy_columns(model_class)
        model_info["relationships"] = detect_relationships(model_class, framework)
    elif framework == "pydantic":
        model_info["fields"] = extract_pydantic_fields(model_class)
        model_info["relationships"] = detect_relationships(model_class, framework)
    else:
        raise ValueError(f"Unsupported framework: {framework}")

    for field_name, rel in model_info["relationships"].items():
        rel_type = rel.get("type", "ForeignKey")
        if rel_type not in {"ForeignKey", "OneToOneField", "ManyToManyField"}:
            continue
        if field_name not in model_info["fields"]:
            model_info["fields"][field_name] = {"required": False}
        model_info["fields"][field_name]["type"] = rel_type
        model_info["fields"][field_name]["related_model"] = rel.get("model")

    return model_info


def extract_django_fields(model_class: ast.ClassDef) -> Dict[str, dict]:
    """Extract Django model fields from a ClassDef node."""
    fields: Dict[str, dict] = {}

    for node in model_class.body:
        if isinstance(node, ast.Assign):
            targets = [t for t in node.targets if isinstance(t, ast.Name)]
            if not targets:
                continue
            field_name = targets[0].id
            call = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            field_name = node.target.id
            call = node.value
        else:
            continue

        if not isinstance(call, ast.Call):
            continue

        field_type = _get_field_type(call)
        if not field_type:
            continue

        field_info = _build_django_field_info(field_name, field_type, call)
        fields[field_name] = field_info

    has_primary_key = any(info.get("primary_key") for info in fields.values())
    if not has_primary_key:
        fields.setdefault(
            "id",
            {
                "type": "AutoField",
                "primary_key": True,
                "auto_generated": True,
                "required": False,
            },
        )

    return fields


def extract_sqlalchemy_columns(model_class: ast.ClassDef) -> Dict[str, dict]:
    """Extract SQLAlchemy columns from a ClassDef node."""
    fields: Dict[str, dict] = {}

    for node in model_class.body:
        if isinstance(node, ast.Assign):
            targets = [t for t in node.targets if isinstance(t, ast.Name)]
            if not targets:
                continue
            field_name = targets[0].id
            call = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            field_name = node.target.id
            call = node.value
        else:
            continue

        if not isinstance(call, ast.Call):
            continue

        field_type = _get_sqlalchemy_column_type(call)
        if not field_type:
            continue

        field_info = _build_sqlalchemy_field_info(field_type, call)
        fields[field_name] = field_info

    return fields


def extract_pydantic_fields(model_class: ast.ClassDef) -> Dict[str, dict]:
    """Extract Pydantic fields from a ClassDef node."""
    fields: Dict[str, dict] = {}

    for node in model_class.body:
        if not isinstance(node, ast.AnnAssign) or not isinstance(node.target, ast.Name):
            continue

        field_name = node.target.id
        field_type = _annotation_type_name(node.annotation)
        if field_type == "EmailStr":
            field_type = "email"
        field_info: Dict[str, Any] = {
            "type": field_type or "str",
            "required": node.value is None,
        }

        default_node = node.value
        if isinstance(default_node, ast.Call) and _name_from_node(default_node.func) == "Field":
            meta = _pydantic_field_metadata(default_node)
            field_info.update(meta)
            default_node = default_node.args[0] if default_node.args else None

        if default_node is not None:
            default_value = _literal_value(default_node)
            field_info["default"] = default_value
            field_info["required"] = False

        if _annotation_is_optional(node.annotation):
            field_info["required"] = False

        literal_choices = _annotation_literal_choices(node.annotation)
        if literal_choices:
            field_info["choices"] = literal_choices

        fields[field_name] = field_info

    return fields


def detect_relationships(model_class: ast.ClassDef, framework: str) -> Dict[str, dict]:
    """Detect relationships such as ForeignKey or ManyToMany fields."""
    relationships: Dict[str, dict] = {}

    if framework == "sqlalchemy":
        for node in model_class.body:
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue

            if isinstance(node, ast.Assign):
                if not node.targets or not isinstance(node.targets[0], ast.Name):
                    continue
                field_name = node.targets[0].id
                call = node.value
            else:
                if not isinstance(node.target, ast.Name):
                    continue
                field_name = node.target.id
                call = node.value

            if not isinstance(call, ast.Call):
                continue

            if _is_sqlalchemy_relationship(call):
                relationships[field_name] = {
                    "type": "OneToMany",
                    "model": _get_sqlalchemy_relationship_model(call),
                }
                continue

            if not _has_sqlalchemy_foreign_key(call):
                continue

            relationships[field_name] = {
                "type": "ForeignKey",
                "model": _get_sqlalchemy_fk_model(call),
            }

        return relationships

    if framework == "pydantic":
        for node in model_class.body:
            if not isinstance(node, ast.AnnAssign) or not isinstance(node.target, ast.Name):
                continue
            field_name = node.target.id
            annotation = node.annotation
            related_model = _pydantic_related_model_name(field_name, annotation, model_class.name)
            if not related_model:
                continue
            relationships[field_name] = {
                "type": "ForeignKey",
                "model": related_model,
            }

        return relationships

    for node in model_class.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue

        if isinstance(node, ast.Assign):
            if not node.targets or not isinstance(node.targets[0], ast.Name):
                continue
            field_name = node.targets[0].id
            call = node.value
        else:
            if not isinstance(node.target, ast.Name):
                continue
            field_name = node.target.id
            call = node.value

        if not isinstance(call, ast.Call):
            continue

        field_type = _get_field_type(call)
        if field_type not in {"ForeignKey", "OneToOneField", "ManyToManyField"}:
            continue

        related_model = _get_related_model_name(call)
        reverse_name = _get_call_keyword_literal(call, "related_name")
        relationships[field_name] = {
            "type": field_type,
            "model": related_model,
            "reverse_name": reverse_name,
        }

    return relationships


def _get_field_type(call: ast.Call) -> Optional[str]:
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    if isinstance(call.func, ast.Name):
        return call.func.id
    return None


def _build_django_field_info(field_name: str, field_type: str, call: ast.Call) -> dict:
    keywords = {kw.arg: _literal_value(kw.value) for kw in call.keywords if kw.arg}

    field_info: Dict[str, Any] = {
        "type": field_type,
        "required": True,
    }

    if "max_length" in keywords:
        field_info["max_length"] = keywords["max_length"]
    if "unique" in keywords:
        field_info["unique"] = keywords["unique"]
    if "null" in keywords:
        field_info["null"] = keywords["null"]
    if "blank" in keywords:
        field_info["blank"] = keywords["blank"]
    if "choices" in keywords:
        field_info["choices"] = keywords["choices"]
    if "default" in keywords:
        field_info["default"] = keywords["default"]
    if "primary_key" in keywords:
        field_info["primary_key"] = keywords["primary_key"]
    if "max_digits" in keywords:
        field_info["max_digits"] = keywords["max_digits"]
    if "decimal_places" in keywords:
        field_info["decimal_places"] = keywords["decimal_places"]
    if "max_digits" in keywords:
        field_info["max_digits"] = keywords["max_digits"]
    if "decimal_places" in keywords:
        field_info["decimal_places"] = keywords["decimal_places"]

    if field_type in {"AutoField", "BigAutoField"}:
        field_info["auto_generated"] = True
        field_info["primary_key"] = True

    if field_type in {"ForeignKey", "OneToOneField", "ManyToManyField"}:
        field_info["related_model"] = _get_related_model_name(call)

    null = field_info.get("null") is True
    blank = field_info.get("blank") is True
    has_default = "default" in field_info
    field_info["required"] = not (null or blank or has_default)

    return field_info


def _get_related_model_name(call: ast.Call) -> Optional[str]:
    if call.args:
        return _name_from_node(call.args[0])

    for kw in call.keywords:
        if kw.arg == "to":
            return _name_from_node(kw.value)

    return None


def _name_from_node(node: ast.AST) -> Optional[str]:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value.split(".")[-1]
    return None


def _get_sqlalchemy_column_type(call: ast.Call) -> Optional[str]:
    if not call.args:
        return None
    first_arg = call.args[0]
    if isinstance(first_arg, ast.Call):
        return _name_from_node(first_arg.func)
    return _name_from_node(first_arg)


def _build_sqlalchemy_field_info(field_type: str, call: ast.Call) -> dict:
    keywords = {kw.arg: _literal_value(kw.value) for kw in call.keywords if kw.arg}

    field_info: Dict[str, Any] = {
        "type": field_type,
        "required": True,
    }

    if "primary_key" in keywords:
        field_info["primary_key"] = keywords["primary_key"]
    if "nullable" in keywords:
        field_info["null"] = keywords["nullable"]
    if "unique" in keywords:
        field_info["unique"] = keywords["unique"]
    if "default" in keywords:
        field_info["default"] = keywords["default"]

    max_length = _get_sqlalchemy_length(call)
    if max_length is not None:
        field_info["max_length"] = max_length
    numeric_meta = _get_sqlalchemy_numeric(call)
    if numeric_meta:
        field_info.update(numeric_meta)

    if _has_sqlalchemy_foreign_key(call):
        field_info["type"] = "ForeignKey"
        field_info["related_model"] = _get_sqlalchemy_fk_model(call)
    else:
        enum_choices = _get_sqlalchemy_enum_choices(call)
        if enum_choices:
            field_info["choices"] = enum_choices

    null = field_info.get("null") is True
    has_default = "default" in field_info
    field_info["required"] = not (null or has_default)

    return field_info


def _get_sqlalchemy_length(call: ast.Call) -> Optional[int]:
    if not call.args:
        return None
    first_arg = call.args[0]
    if isinstance(first_arg, ast.Call) and first_arg.args:
        length_value = _literal_value(first_arg.args[0])
        if isinstance(length_value, int):
            return length_value
    return None


def _get_sqlalchemy_numeric(call: ast.Call) -> Optional[dict]:
    if not call.args:
        return None
    first_arg = call.args[0]
    if isinstance(first_arg, ast.Call) and _name_from_node(first_arg.func) in {"Numeric", "DECIMAL"}:
        max_digits = None
        decimal_places = None
        if first_arg.args:
            max_digits = _literal_value(first_arg.args[0])
            if len(first_arg.args) > 1:
                decimal_places = _literal_value(first_arg.args[1])
        if isinstance(max_digits, int):
            meta = {"max_digits": max_digits}
            if isinstance(decimal_places, int):
                meta["decimal_places"] = decimal_places
            return meta
    return None


def _has_sqlalchemy_foreign_key(call: ast.Call) -> bool:
    for arg in call.args:
        if isinstance(arg, ast.Call):
            if _name_from_node(arg.func) == "ForeignKey":
                return True
    return False


def _get_sqlalchemy_fk_model(call: ast.Call) -> Optional[str]:
    for arg in call.args:
        if isinstance(arg, ast.Call) and _name_from_node(arg.func) == "ForeignKey":
            if arg.args:
                fk_value = _literal_value(arg.args[0])
                if isinstance(fk_value, str):
                    table = fk_value.split(".")[0]
                    if table.endswith("s"):
                        table = table[:-1]
                    table = table.replace("-", "_")
                    camel = "".join(part.title() for part in table.split("_"))
                    return camel or table.title()
    return None


def _is_sqlalchemy_relationship(call: ast.Call) -> bool:
    return _name_from_node(call.func) == "relationship"


def _get_sqlalchemy_relationship_model(call: ast.Call) -> Optional[str]:
    if call.args:
        return _name_from_node(call.args[0])
    for kw in call.keywords:
        if kw.arg == "argument":
            return _name_from_node(kw.value)
    return None


def _get_sqlalchemy_enum_choices(call: ast.Call) -> Optional[list]:
    if not call.args:
        return None
    first_arg = call.args[0]
    if isinstance(first_arg, ast.Call) and _name_from_node(first_arg.func) == "Enum":
        choices = []
        for arg in first_arg.args:
            value = _literal_value(arg)
            if value is not None:
                choices.append(value)
        return choices or None
    return None


def _annotation_type_name(annotation: ast.AST) -> Optional[str]:
    if isinstance(annotation, ast.BinOp) and isinstance(annotation.op, ast.BitOr):
        return _annotation_type_name(annotation.left)
    if isinstance(annotation, ast.Tuple):
        for elt in annotation.elts:
            name = _annotation_type_name(elt)
            if name and name not in {"None", "NoneType"}:
                return name
        return None
    if isinstance(annotation, ast.Subscript):
        inner = _annotation_inner_type(annotation)
        if inner is not None:
            return _annotation_type_name(inner)
    if isinstance(annotation, ast.Name):
        return annotation.id
    if isinstance(annotation, ast.Attribute):
        return annotation.attr
    return None


def _pydantic_related_model_name(field_name: str, annotation: ast.AST, model_name: str) -> Optional[str]:
    if isinstance(annotation, ast.Subscript):
        inner = _annotation_inner_type(annotation)
        if inner is not None:
            return _pydantic_related_model_name(field_name, inner, model_name)

    base_name = _annotation_type_name(annotation)
    scalar_types = {
        "UUID",
        "UUID1",
        "UUID4",
        "HttpUrl",
        "AnyUrl",
        "Url",
        "EmailStr",
        "Decimal",
    }
    if base_name and base_name[0].isupper() and base_name not in scalar_types:
        return base_name
    if field_name.endswith("_id"):
        return field_name[:-3].title()
    if field_name in {"manager_id", "mentor_id", "supervisor_id"}:
        return model_name
    return None


def _get_call_keyword_literal(call: ast.Call, keyword: str) -> Optional[Any]:
    for kw in call.keywords:
        if kw.arg == keyword:
            return _literal_value(kw.value)
    return None


def _pydantic_field_metadata(call: ast.Call) -> Dict[str, Any]:
    meta: Dict[str, Any] = {}
    for kw in call.keywords:
        if kw.arg == "max_length":
            meta["max_length"] = _literal_value(kw.value)
        if kw.arg == "min_length":
            meta["min_length"] = _literal_value(kw.value)
        if kw.arg == "unique":
            meta["unique"] = _literal_value(kw.value)
        if kw.arg == "default":
            meta["default"] = _literal_value(kw.value)
    return meta


def _annotation_is_optional(annotation: ast.AST) -> bool:
    if isinstance(annotation, ast.Subscript):
        if isinstance(annotation.value, ast.Name) and annotation.value.id in {"Optional", "Union"}:
            return True
        if isinstance(annotation.value, ast.Attribute) and annotation.value.attr in {"Optional", "Union"}:
            return True
    if isinstance(annotation, ast.BinOp) and isinstance(annotation.op, ast.BitOr):
        return True
    return False


def _annotation_inner_type(annotation: ast.Subscript) -> Optional[ast.AST]:
    if isinstance(annotation.value, ast.Name) and annotation.value.id in {"Optional", "Union", "List", "list"}:
        return annotation.slice
    if isinstance(annotation.value, ast.Attribute) and annotation.value.attr in {"Optional", "Union", "List", "list"}:
        return annotation.slice
    return None


def _annotation_literal_choices(annotation: ast.AST) -> Optional[list]:
    if isinstance(annotation, ast.Subscript):
        if isinstance(annotation.value, ast.Name) and annotation.value.id == "Literal":
            return _extract_literal_values(annotation.slice)
        if isinstance(annotation.value, ast.Attribute) and annotation.value.attr == "Literal":
            return _extract_literal_values(annotation.slice)
    return None


def _extract_literal_values(node: ast.AST) -> list:
    values = []
    if isinstance(node, ast.Tuple):
        items = node.elts
    else:
        items = [node]
    for item in items:
        value = _literal_value(item)
        if value is not None:
            values.append(value)
    return values


def _literal_value(node: ast.AST) -> Any:
    try:
        return ast.literal_eval(node)
    except (ValueError, SyntaxError):
        return None
