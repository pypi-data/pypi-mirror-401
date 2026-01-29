from ..core import SignedHttpClient
from ..models import CreateQuotationRequest, Quotation


class QuotationClient:
    """Client for quotation-related API operations."""

    def __init__(self, signed_client: SignedHttpClient):
        self._client = signed_client

    def create_quotation(self, request: CreateQuotationRequest) -> Quotation:
        """Creates a new quotation."""
        request.validate()
        response = self._client.post(path="/quotations", body=request.to_body_dict())
        return Quotation.from_dict(response)

    def get_quotation_by_id(self, quotation_id: str) -> Quotation:
        """Retrieve a quotation by its identifier."""
        response = self._client.get(path=f"/quotations/{quotation_id}")
        return Quotation.from_dict(response)
