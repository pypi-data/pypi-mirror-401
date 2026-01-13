"""Field mapper selection utilities."""

from __future__ import annotations

from .django_mapper import map_django_field
from .sqlalchemy_mapper import map_sqlalchemy_field
from .pydantic_mapper import map_pydantic_field


def get_mapper(framework: str):
    """Return the mapper function for the selected framework."""
    mappers = {
        "django": map_django_field,
        "sqlalchemy": map_sqlalchemy_field,
        "pydantic": map_pydantic_field,
    }
    return mappers.get(framework)
