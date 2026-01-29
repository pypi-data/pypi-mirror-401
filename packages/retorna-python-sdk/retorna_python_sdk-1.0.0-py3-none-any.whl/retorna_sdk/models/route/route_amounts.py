from dataclasses import dataclass, field, fields
from typing import Any, Dict


@dataclass
class RouteAmounts:
    """Represents an available transfer amount for a route."""

    daily_amount: float = field(metadata={"alias": "dailyAmount"})
    weekly_amount: float = field(metadata={"alias": "weeklyAmount"})
    monthly_amount: float = field(metadata={"alias": "monthlyAmount"})

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "RouteAmounts":
        """Create a RouteAmounts instance from API response data."""
        kwargs = {}
        for f in fields(RouteAmounts):
            alias = f.metadata.get("alias", f.name)
            kwargs[f.name] = data.get(alias)
        return RouteAmounts(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the RouteAmounts instance into a snake_case dictionary."""
        result = {}
        for f in fields(RouteAmounts):
            result[f.name] = getattr(self, f.name)
        return result
