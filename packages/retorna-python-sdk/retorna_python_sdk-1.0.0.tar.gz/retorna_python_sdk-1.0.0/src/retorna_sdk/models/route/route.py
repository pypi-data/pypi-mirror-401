from dataclasses import dataclass, field, fields
from typing import Any, Dict

from .route_amounts import RouteAmounts


@dataclass
class Route:
    """Represents an available route."""

    country: str
    created_time: str = field(metadata={"alias": "createdTime"})
    currency: str
    id: int
    name: str
    payout_type_backend_id: str = field(metadata={"alias": "payoutTypeBackendId"})
    platform_name: str = field(metadata={"alias": "platformName"})
    status: str
    updated_time: str = field(metadata={"alias": "updatedTime"})
    min_amount: float = field(metadata={"alias": "minAmount"})
    max_amount: float = field(metadata={"alias": "maxAmount"})
    daily_limit: float = field(metadata={"alias": "dailyLimit"})
    weekly_limit: float = field(metadata={"alias": "weeklyLimit"})
    monthly_limit: float = field(metadata={"alias": "monthlyLimit"})
    amounts: RouteAmounts

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Route":
        """Create a Route instance from API response data."""
        kwargs = {}
        for f in fields(Route):
            alias = f.metadata.get("alias", f.name)
            if f.name == "amounts":
                kwargs["amounts"] = RouteAmounts.from_dict(data.get("amounts", {}))
            else:
                kwargs[f.name] = data.get(alias)
        return Route(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Route instance into a snake_case dictionary."""
        result = {}
        for f in fields(Route):
            value = getattr(self, f.name)
            if isinstance(value, RouteAmounts):
                result[f.name] = value.to_dict()
            else:
                result[f.name] = value
        return result
