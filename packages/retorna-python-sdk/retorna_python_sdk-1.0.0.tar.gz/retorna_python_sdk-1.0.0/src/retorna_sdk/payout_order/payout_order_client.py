from ..models.payout_order import CreatePayoutOrderRequest, PayoutOrder
from ..models.payout_order.validation.registry import PLATFORM_VALIDATORS


class PayoutOrderClient:
    """Client for payout-order-related API operations."""

    def __init__(self, signed_http_client):
        self.http = signed_http_client

    def create(
        self, platform_name: str, request: CreatePayoutOrderRequest
    ) -> PayoutOrder:
        """Creates a new payout order."""
        validator = PLATFORM_VALIDATORS.get(platform_name)
        if not validator:
            raise ValueError(f"Unsupported payout type platform: {platform_name}")

        validator.validate(request, platform_name)

        body = request.to_body_dict()

        response = self.http.post(
            "/orders",
            body=body,
        )

        return PayoutOrder.from_dict(response)

    def get_by_id(self, payout_order_id: str) -> PayoutOrder:
        """Retrieves a payout order by its identifier."""
        response = self.http.get(f"/orders/{payout_order_id}")
        return PayoutOrder.from_dict(response)
