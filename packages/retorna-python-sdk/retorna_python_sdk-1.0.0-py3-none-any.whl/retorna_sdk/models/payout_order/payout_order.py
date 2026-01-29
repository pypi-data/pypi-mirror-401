from dataclasses import dataclass, field, fields
from typing import Any, Dict

from ..quotation import Quotation
from .payment_instructions import PaymentInstructions


@dataclass(frozen=True)
class PayoutOrder:
    """Represents a created payout order."""

    id: int
    entity_backend_id: str = field(metadata={"alias": "entityBackendId"})
    payout_type_backend_id: str = field(metadata={"alias": "payoutTypeBackendId"})
    payout_order_backend_id: str = field(metadata={"alias": "payoutOrderBackendId"})
    external_id: str = field(metadata={"alias": "externalId"})
    currency: str
    status: str
    calculated_percentage_fee: float = field(
        metadata={"alias": "calculatedPercentageFee"}
    )
    calculated_flat_fee: float = field(metadata={"alias": "calculatedFlatFee"})
    applied_floor: float = field(metadata={"alias": "appliedFloor"})
    applied_ceiling: float = field(metadata={"alias": "appliedCeiling"})
    provider_amount: float = field(metadata={"alias": "providerAmount"})
    sum_fee: float = field(metadata={"alias": "sumFee"})
    total_fee: float = field(metadata={"alias": "totalFee"})
    tax_fee: float = field(metadata={"alias": "taxFee"})

    beneficiary_names: str = field(metadata={"alias": "beneficiaryNames"})
    beneficiary_last_names: str = field(metadata={"alias": "beneficiaryLastNames"})
    beneficiary_document_id: str = field(metadata={"alias": "beneficiaryDocumentId"})
    beneficiary_document_type: str = field(
        metadata={"alias": "beneficiaryDocumentType"}
    )
    beneficiary_country: str = field(metadata={"alias": "beneficiaryCountry"})

    payment_instructions: PaymentInstructions = field(
        metadata={"alias": "paymentInstructions"}
    )

    sender_names: str = field(metadata={"alias": "senderNames"})
    sender_last_names: str = field(metadata={"alias": "senderLastNames"})
    sender_document_id: str = field(metadata={"alias": "senderDocumentId"})
    sender_document_type: str = field(metadata={"alias": "senderDocumentType"})
    sender_phone: str = field(metadata={"alias": "senderPhone"})
    sender_country: str = field(metadata={"alias": "senderCountry"})
    sender_email: str = field(metadata={"alias": "senderEmail"})

    created_time: str = field(metadata={"alias": "createdTime"})
    updated_time: str = field(metadata={"alias": "updatedTime"})

    b2b_client_backend_id: str = field(metadata={"alias": "b2bClientBackendId"})
    purpose: str
    rate: float

    quotation: Quotation = field(metadata={"alias": "quotation"})

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PayoutOrder":
        """Create a PayoutOrder instance from API response data."""
        kwargs: Dict[str, Any] = {}
        for f in fields(PayoutOrder):
            alias = f.metadata.get("alias", f.name)

            if f.name == "payment_instructions":
                kwargs[f.name] = PaymentInstructions.from_dict(data.get(alias, {}))
            elif f.name == "quotation":
                kwargs[f.name] = Quotation.from_dict(data.get(alias, {}))
            else:
                kwargs[f.name] = data.get(alias)

        return PayoutOrder(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the PayoutOrder instance into a snake_case dictionary."""
        result: Dict[str, Any] = {}
        for f in fields(PayoutOrder):
            value = getattr(self, f.name)

            if isinstance(value, PaymentInstructions):
                result[f.name] = value.to_dict()
            elif isinstance(value, Quotation):
                result[f.name] = value.to_dict()
            else:
                result[f.name] = value

        return result
