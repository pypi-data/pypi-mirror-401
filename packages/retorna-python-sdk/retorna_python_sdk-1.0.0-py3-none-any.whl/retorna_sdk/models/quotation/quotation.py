from dataclasses import dataclass, field, fields
from typing import Any, Dict, List

from .pricing_rule import PricingRule


@dataclass
class Quotation:
    """Represents a quotation returned by the API."""

    id: str
    quotation_backend_id: str = field(metadata={"alias": "quotationBackendId"})
    rate_id: int = field(metadata={"alias": "rateId"})
    b2b_client_id: int = field(metadata={"alias": "b2bClientId"})
    value: float
    source_amount: float = field(metadata={"alias": "sourceAmount"})
    target_amount: float = field(metadata={"alias": "targetAmount"})
    convert_amount: float = field(metadata={"alias": "convertAmount"})
    source_currency: str = field(metadata={"alias": "sourceCurrency"})
    target_currency: str = field(metadata={"alias": "targetCurrency"})
    created_time: str = field(metadata={"alias": "createdTime"})
    updated_time: str = field(metadata={"alias": "updatedTime"})
    pricing_rules: List[PricingRule] = field(
        metadata={"alias": "pricingRules"}, default_factory=list
    )

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Quotation":
        """Create a Quotation instance from API response data."""
        kwargs = {}
        for f in fields(Quotation):
            alias = f.metadata.get("alias", f.name)
            if f.name == "pricing_rules":
                kwargs[f.name] = [
                    PricingRule.from_dict(item) for item in data.get(alias, [])
                ]
            else:
                kwargs[f.name] = data.get(alias)
        return Quotation(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Quotation instance into a snake_case dictionary."""
        result = {}
        for f in fields(Quotation):
            value = getattr(self, f.name)
            if isinstance(value, list) and value and isinstance(value[0], PricingRule):
                result[f.name] = [item.to_dict() for item in value]
            else:
                result[f.name] = value
        return result
