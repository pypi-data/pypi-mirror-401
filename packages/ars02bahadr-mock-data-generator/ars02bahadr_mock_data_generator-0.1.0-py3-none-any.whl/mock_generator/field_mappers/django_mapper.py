"""Django field to Faker mapping."""

from __future__ import annotations

from typing import Any, Dict


DJANGO_FIELD_MAPPING = {
    "CharField": {
        "faker_method": "text",
        "use_max_length": True,
    },
    "EmailField": {
        "faker_method": "email",
    },
    "IntegerField": {
        "faker_method": "random_int",
        "min": 0,
        "max": 2_147_483_647,
    },
    "BooleanField": {
        "faker_method": "boolean",
    },
    "DateTimeField": {
        "faker_method": "date_time_this_year",
    },
    "TextField": {
        "faker_method": "paragraph",
        "nb_sentences": 5,
    },
    "URLField": {
        "faker_method": "url",
    },
    "UUIDField": {
        "faker_method": "uuid4",
    },
    "DecimalField": {
        "faker_method": "pydecimal",
    },
    "ForeignKey": {
        "faker_method": "random_element",
        "needs_relationship_data": True,
    },
    "PhoneNumberField": {
        "faker_method": "turkish_phone",
    },
}


def map_django_field(field_name: str, field_info: dict) -> Dict[str, Any]:
    """Map Django field info to Faker configuration."""
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
    mapping = DJANGO_FIELD_MAPPING.get(field_type)

    if not mapping:
        return {"method": "pystr", "params": {"min_chars": 5, "max_chars": 12}}

    params: Dict[str, Any] = {}

    if mapping.get("use_max_length") and field_info.get("max_length"):
        params["max_nb_chars"] = int(field_info["max_length"])

    if field_info.get("choices"):
        params["elements"] = [choice[0] for choice in field_info["choices"]]
        return {"method": "random_element", "params": params}

    if "min" in mapping:
        params["min"] = mapping["min"]
    if "max" in mapping:
        params["max"] = mapping["max"]
    if "nb_sentences" in mapping:
        params["nb_sentences"] = mapping["nb_sentences"]
    if field_type == "DecimalField":
        max_digits = field_info.get("max_digits")
        decimal_places = field_info.get("decimal_places")
        if isinstance(max_digits, int):
            params["left_digits"] = max_digits
        if isinstance(decimal_places, int):
            params["right_digits"] = decimal_places

    return {"method": mapping["faker_method"], "params": params}
