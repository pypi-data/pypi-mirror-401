"""Pydantic field to Faker mapping."""

from __future__ import annotations

from typing import Any, Dict


PYDANTIC_FIELD_MAPPING = {
    "str": {
        "faker_method": "text",
    },
    "int": {
        "faker_method": "random_int",
        "min": 0,
        "max": 2_147_483_647,
    },
    "Decimal": {
        "faker_method": "pydecimal",
    },
    "float": {
        "faker_method": "pyfloat",
        "min_value": 0.0,
        "max_value": 10_000.0,
    },
    "bool": {
        "faker_method": "boolean",
    },
    "datetime": {
        "faker_method": "date_time_this_year",
    },
    "date": {
        "faker_method": "date_this_year",
    },
    "email": {
        "faker_method": "email",
    },
    "UUID": {
        "faker_method": "uuid4",
    },
    "HttpUrl": {
        "faker_method": "url",
    },
    "AnyUrl": {
        "faker_method": "url",
    },
    "Url": {
        "faker_method": "url",
    },
    "IBAN": {
        "faker_method": "iban",
    },
    "IBANStr": {
        "faker_method": "iban",
    },
    "phone": {
        "faker_method": "turkish_phone",
    },
    "PhoneNumber": {
        "faker_method": "turkish_phone",
    },
}


def map_pydantic_field(field_name: str, field_info: dict) -> Dict[str, Any]:
    """Map Pydantic field info to Faker configuration."""
    lowered_name = field_name.lower()
    if any(key in lowered_name for key in ["phone", "telefon", "tel", "contact", "number"]):
        return {"method": "turkish_phone", "params": {}}
    if "email" in lowered_name:
        return {"method": "email", "params": {}}
    if lowered_name in {"tckn", "tc_kimlik_no", "tc_kimlik"}:
        return {"method": "tckn", "params": {}}
    if lowered_name in {"city", "sehir"}:
        return {"method": "city", "params": {}}
    if "currency" in lowered_name:
        return {"method": "currency_code", "params": {}}
    if any(key in lowered_name for key in ["division", "department", "unit", "org", "office"]):
        return {"method": "company", "params": {}}
    if "code" in lowered_name:
        return {"method": "bothify", "params": {"text": "???-###"}}
    if "name" in lowered_name:
        return {"method": "name", "params": {}}
    if lowered_name in {"iban"}:
        return {"method": "iban", "params": {}}

    field_type = field_info.get("type")
    mapping = PYDANTIC_FIELD_MAPPING.get(field_type)

    if not mapping:
        return {"method": "pystr", "params": {"min_chars": 5, "max_chars": 12}}

    params: Dict[str, Any] = {}

    if "min" in mapping:
        params["min"] = mapping["min"]
    if "max" in mapping:
        params["max"] = mapping["max"]
    if "min_value" in mapping:
        params["min_value"] = mapping["min_value"]
    if "max_value" in mapping:
        params["max_value"] = mapping["max_value"]
    if field_type == "Decimal":
        max_digits = field_info.get("max_digits")
        decimal_places = field_info.get("decimal_places")
        if isinstance(max_digits, int):
            params["left_digits"] = max_digits
        if isinstance(decimal_places, int):
            params["right_digits"] = decimal_places

    return {"method": mapping["faker_method"], "params": params}
