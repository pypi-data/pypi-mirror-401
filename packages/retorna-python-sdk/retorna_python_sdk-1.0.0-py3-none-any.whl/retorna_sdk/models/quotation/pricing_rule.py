from dataclasses import dataclass, field, fields
from typing import Any, Dict


@dataclass
class PricingRule:
    """Represents a pricing rule applied within a quotation."""

    currency: str
    backend_id: str = field(metadata={"alias": "backendId"})
    pricing_rule: str = field(metadata={"alias": "pricingRule"})
    pricing_type: str = field(metadata={"alias": "pricingType"})
    applied_value: float = field(metadata={"alias": "appliedValue"})
    pricing_label: str = field(metadata={"alias": "pricingLabel"})
    calculation_method: str = field(metadata={"alias": "calculationMethod"})

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PricingRule":
        """Create a PricingRule instance from API response data."""
        kwargs = {}
        for f in fields(PricingRule):
            alias = f.metadata.get("alias", f.name)
            kwargs[f.name] = data.get(alias)
        return PricingRule(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the PricingRule instance into a snake_case dictionary."""
        result = {}
        for f in fields(PricingRule):
            result[f.name] = getattr(self, f.name)
        return result
