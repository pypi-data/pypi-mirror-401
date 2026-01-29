from dataclasses import dataclass, field, fields
from typing import Any, Dict


@dataclass
class PaymentInstructions:
    """Represents payment instruction details for payout operations."""

    bank_name: str | None = field(default=None, metadata={"alias": "bankName"})
    account_number: str | None = field(
        default=None, metadata={"alias": "accountNumber"}
    )
    account_type: str | None = field(default=None, metadata={"alias": "accountType"})
    phone_number: str | None = field(default=None, metadata={"alias": "phoneNumber"})
    branch_id: str | None = field(default=None, metadata={"alias": "branchId"})

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PaymentInstructions":
        """Create a Route instance from API response data."""
        kwargs = {}
        for f in fields(PaymentInstructions):
            alias = f.metadata.get("alias", f.name)
            kwargs[f.name] = data.get(alias)
        return PaymentInstructions(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Return a snake_case dictionary representation."""
        result = {}
        for f in fields(self):
            result[f.name] = getattr(self, f.name)
        return result

    def to_body_dict(self) -> Dict[str, Any]:
        """Return a camelCase dictionary suitable for API submission."""
        body = {}
        for f in fields(self):
            alias = f.metadata.get("alias", f.name)
            value = getattr(self, f.name)
            body[alias] = value
        return body
