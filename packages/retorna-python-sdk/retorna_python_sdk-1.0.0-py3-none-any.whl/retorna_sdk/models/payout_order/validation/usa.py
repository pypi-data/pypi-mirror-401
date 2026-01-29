from .utils import validate_required_fields

REQUIRED_FIELDS_US = {
    "beneficiary_document_id",
    "beneficiary_document_type",
    "beneficiary_last_names",
    "beneficiary_names",
    "sender_names",
    "sender_last_names",
    "sender_document_id",
    "sender_document_type",
    "sender_country",
    "external_id",
    "purpose",
}

REQUIRED_PAYMENT_US = {"account_number", "account_type", "branch_id"}


class USAValidator:
    def validate(self, req, platform_name: str):
        data = req.to_snake_dict()
        validate_required_fields(data, REQUIRED_FIELDS_US)

        pi = data["payment_instructions"]
        validate_required_fields(pi, REQUIRED_PAYMENT_US, "paymentInstructions")


US_VALIDATOR = USAValidator()
