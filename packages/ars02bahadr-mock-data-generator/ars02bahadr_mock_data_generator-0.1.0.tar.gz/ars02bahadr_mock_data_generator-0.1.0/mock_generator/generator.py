"""Mock data generation logic."""

from __future__ import annotations

from typing import Any, Dict, List

from faker import Faker

from mock_generator.field_mappers import get_mapper
from mock_generator.locales.turkish import TurkishProvider


class MockDataGenerator:
    """Generate mock data for analyzed models."""

    def __init__(self, locale: str = "en_US") -> None:
        self.faker = Faker(locale)
        self.generated_data: Dict[str, List[dict]] = {}
        self.unique_pools: Dict[str, Dict[str, set]] = {}
        if locale.startswith("tr"):
            self.faker.add_provider(TurkishProvider)

    def generate_for_model(self, model_info: dict, count: int) -> List[dict]:
        """Generate N mock records for a model."""
        records: List[dict] = []

        mapper = get_mapper(model_info.get("framework", "django"))
        if mapper is None:
            raise ValueError("No field mapper available for the detected framework.")

        one_to_one_used: Dict[str, set] = {}

        for i in range(count):
            record: Dict[str, Any] = {}

            for field_name, field_info in model_info["fields"].items():
                if field_info.get("auto_generated"):
                    record[field_name] = i + 1
                    continue

                if field_info.get("type") in {"ForeignKey", "OneToOneField"}:
                    related_model = field_info.get("related_model") or (
                        model_info["name"] if field_name in {"manager_id", "mentor_id", "supervisor_id"} else None
                    )
                    related_records = self.generated_data.get(related_model, [])
                    if not related_records:
                        if related_model in {model_info["name"], "self", None}:
                            if records:
                                related_records = records
                            else:
                                record[field_name] = None
                                continue
                        else:
                            record[field_name] = None
                            continue
                    if field_info.get("type") == "OneToOneField":
                        used = one_to_one_used.setdefault(field_name, set())
                        available = [r for r in related_records if r.get("id") not in used]
                        if not available:
                            record[field_name] = None
                        else:
                            chosen = self.faker.random_element(available)
                            record[field_name] = chosen.get("id")
                            used.add(record[field_name])
                    else:
                        record[field_name] = self.faker.random_element(related_records).get("id")
                    continue

                if field_info.get("type") == "ManyToManyField":
                    related_model = field_info.get("related_model")
                    related_records = self.generated_data.get(related_model, [])
                    if not related_records:
                        raise ValueError(f"Related model {related_model} has no records generated yet.")
                    else:
                        ids = [r.get("id") for r in related_records if r.get("id") is not None]
                        size = min(len(ids), self.faker.random_int(1, 3))
                        record[field_name] = self.faker.random_elements(ids, length=size, unique=True)
                    continue

                if field_info.get("choices"):
                    choices = [choice[0] for choice in field_info["choices"]]
                    record[field_name] = self.faker.random_element(choices)
                    continue

                faker_config = mapper(field_name, field_info)
                record[field_name] = self.generate_field_value(
                    faker_config,
                    unique=bool(field_info.get("unique")),
                    max_length=field_info.get("max_length"),
                    model_name=model_info["name"],
                    field_name=field_name,
                )

                if field_info.get("max_length") and isinstance(record[field_name], str):
                    max_len = int(field_info["max_length"])
                    if len(record[field_name]) > max_len:
                        record[field_name] = record[field_name][:max_len]

            records.append(record)

        return records

    def generate_field_value(
        self,
        faker_config: Dict[str, Any],
        unique: bool = False,
        max_length: int | None = None,
        model_name: str | None = None,
        field_name: str | None = None,
    ) -> Any:
        """Generate a single field value using Faker."""
        method_name = faker_config["method"]
        params = faker_config.get("params", {})
        if not hasattr(self.faker, method_name) and method_name == "turkish_phone":
            method_name = "phone_number"
        provider = self.faker.unique if unique else self.faker
        pool = None
        if unique and model_name and field_name:
            pool = self.unique_pools.setdefault(model_name, {}).setdefault(field_name, set())

        while True:
            value = getattr(provider, method_name)(**params)
            if max_length and isinstance(value, str) and len(value) > max_length:
                value = value[: max_length]
            if pool is not None:
                if value in pool:
                    continue
                pool.add(value)
            return value

    def generate_all(self, models: Dict[str, dict], counts: Dict[str, int], order: List[str]) -> Dict[str, List[dict]]:
        """Generate mock data for all models in dependency order."""
        for model_name in order:
            count = counts.get(model_name, 10)
            model_info = models[model_name]
            records = self.generate_for_model(model_info, count)
            self.generated_data[model_name] = records

        return self.generated_data
