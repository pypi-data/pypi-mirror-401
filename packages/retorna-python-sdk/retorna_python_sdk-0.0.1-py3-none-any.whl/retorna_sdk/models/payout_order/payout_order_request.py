from dataclasses import dataclass, field, fields
from typing import Any, Dict

from pydantic_core import SchemaValidator, ValidationError

from .payment_instructions import PaymentInstructions
from .payment_purpose import PaymentPurpose
from .validation import PLATFORM_VALIDATORS

payout_order_schema = SchemaValidator(
    {
        "type": "typed-dict",
        "fields": {
            "pog_quotation_id": {"type": "typed-dict-field", "schema": {"type": "int"}},
            "external_id": {"type": "typed-dict-field", "schema": {"type": "str"}},
            "sender_names": {"type": "typed-dict-field", "schema": {"type": "str"}},
            "sender_last_names": {
                "type": "typed-dict-field",
                "schema": {"type": "str"},
            },
            "sender_email": {"type": "typed-dict-field", "schema": {"type": "str"}},
            "sender_phone": {"type": "typed-dict-field", "schema": {"type": "str"}},
            "sender_document_id": {
                "type": "typed-dict-field",
                "schema": {"type": "str"},
            },
            "sender_document_type": {
                "type": "typed-dict-field",
                "schema": {"type": "str"},
            },
            "sender_country": {
                "type": "typed-dict-field",
                "schema": {"type": "str", "pattern": r"^[A-Za-z]{2}$"},
            },
            "beneficiary_names": {
                "type": "typed-dict-field",
                "schema": {"type": "str"},
            },
            "beneficiary_last_names": {
                "type": "typed-dict-field",
                "schema": {"type": "str"},
            },
            "beneficiary_email": {
                "type": "typed-dict-field",
                "schema": {"type": "str"},
            },
            "beneficiary_phone": {
                "type": "typed-dict-field",
                "schema": {"type": "str"},
            },
            "beneficiary_document_id": {
                "type": "typed-dict-field",
                "schema": {"type": "str"},
            },
            "beneficiary_document_type": {
                "type": "typed-dict-field",
                "schema": {"type": "str"},
            },
            "beneficiary_country": {
                "type": "typed-dict-field",
                "schema": {"type": "str", "pattern": r"^[A-Za-z]{2}$"},
            },
            "purpose": {
                "type": "typed-dict-field",
                "schema": {
                    "type": "literal",
                    "expected": [e.value for e in PaymentPurpose],
                },
            },
            "payment_instructions": {
                "type": "typed-dict-field",
                "schema": {"type": "dict"},
            },
        },
    }
)


@dataclass
class CreatePayoutOrderRequest:
    """Request payload for creating a payout order."""

    pog_quotation_id: int = field(metadata={"alias": "pogQuotationId"})
    external_id: str = field(metadata={"alias": "externalId"})
    sender_names: str = field(metadata={"alias": "senderNames"})
    sender_last_names: str = field(metadata={"alias": "senderLastNames"})
    sender_email: str = field(metadata={"alias": "senderEmail"})
    sender_phone: str = field(metadata={"alias": "senderPhone"})
    sender_document_id: str = field(metadata={"alias": "senderDocumentId"})
    sender_document_type: str = field(metadata={"alias": "senderDocumentType"})
    sender_country: str = field(metadata={"alias": "senderCountry"})
    beneficiary_names: str = field(metadata={"alias": "beneficiaryNames"})
    beneficiary_last_names: str = field(metadata={"alias": "beneficiaryLastNames"})
    beneficiary_email: str = field(metadata={"alias": "beneficiaryEmail"})
    beneficiary_phone: str = field(metadata={"alias": "beneficiaryPhone"})
    beneficiary_document_id: str = field(metadata={"alias": "beneficiaryDocumentId"})
    beneficiary_document_type: str = field(
        metadata={"alias": "beneficiaryDocumentType"}
    )
    beneficiary_country: str = field(metadata={"alias": "beneficiaryCountry"})
    purpose: str
    payment_instructions: PaymentInstructions = field(
        metadata={"alias": "paymentInstructions"}
    )

    def validate(self, platform_name: str) -> None:
        """Validate request fields using schema-level and custom rules."""
        try:
            payout_order_schema.validate_python(self.to_dict())
        except ValidationError as e:
            raise ValueError(f"CreatePayoutOrderRequest type error: {e}")

        validator = PLATFORM_VALIDATORS.get(platform_name)
        if not validator:
            raise ValueError(f"Unsupported payout platform: {platform_name}")

        validator.validate(self, platform_name)

    def to_dict(self) -> Dict[str, Any]:
        """Return a snake_case dictionary representation."""
        out = {}
        for f in fields(self):
            val = getattr(self, f.name)
            if isinstance(val, PaymentInstructions):
                out[f.name] = val.to_dict()
            else:
                out[f.name] = val
        return out

    def to_body_dict(self) -> Dict[str, Any]:
        """Return a camelCase dictionary suitable for API submission."""
        body = {}
        for f in fields(self):
            alias = f.metadata.get("alias", f.name)
            value = getattr(self, f.name)
            if isinstance(value, PaymentInstructions):
                body[alias] = value.to_body_dict()
            else:
                body[alias] = value
        return body
