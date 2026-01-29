from dataclasses import dataclass, field, fields
from typing import Any, Dict

from pydantic_core import SchemaValidator, ValidationError

create_quotation_schema = SchemaValidator(
    {
        "type": "typed-dict",
        "fields": {
            "source_currency": {
                "type": "typed-dict-field",
                "schema": {
                    "type": "default",
                    "schema": {"type": "str"},
                    "default": "USDT",
                },
            },
            "target_country": {
                "type": "typed-dict-field",
                "schema": {
                    "type": "str",
                },
            },
            "target_currency": {
                "type": "typed-dict-field",
                "schema": {
                    "type": "str",
                },
            },
            "amount": {
                "type": "typed-dict-field",
                "schema": {
                    "type": "float",
                    "ge": 0,
                },
            },
            "payout_type": {
                "type": "typed-dict-field",
                "schema": {
                    "type": "str",
                },
            },
            "amount_type": {
                "type": "typed-dict-field",
                "schema": {
                    "type": "literal",
                    "expected": ["SOURCE", "TARGET"],
                },
            },
        },
    }
)


@dataclass
class CreateQuotationRequest:
    """Request payload for creating a quotation."""

    source_currency: str = field(metadata={"alias": "sourceCurrency"})
    target_country: str = field(metadata={"alias": "targetCountry"})
    target_currency: str = field(metadata={"alias": "targetCurrency"})
    amount: float
    payout_type: str = field(metadata={"alias": "payoutType"})
    amount_type: str = field(metadata={"alias": "amountType"})

    def validate(self) -> None:
        """Validate request fields using schema-level and custom rules."""
        try:
            create_quotation_schema.validate_python(self.to_dict())
        except ValidationError as e:
            raise ValueError(f"Invalid CreateQuotationRequest: {e}") from e

        if len(self.target_country) != 2:
            raise ValueError("target_country must be a 2-letter code.")

        if self.amount <= 0:
            raise ValueError("amount must be positive.")

    def to_dict(self) -> Dict[str, Any]:
        """Return a snake_case dictionary representation."""
        result = {}
        for f in fields(self):
            result[f.name] = getattr(self, f.name)
        return result

    def to_body_dict(self) -> Dict[str, Any]:
        """Return a camelCase dictionary suitable for API submission."""
        self.validate()
        body = {}
        for f in fields(self):
            alias = f.metadata.get("alias", f.name)
            body[alias] = getattr(self, f.name)
        return body
