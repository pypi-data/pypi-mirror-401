from .utils import validate_required_fields

REQUIRED_FIELDS_CO = {
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

REQUIRED_PAYMENT_CASH_CO = {"bank_name", "phone_number"}
REQUIRED_PAYMENT_INTERBANK_CO = {"bank_name", "account_number", "account_type"}


class ColombiaValidator:
    def validate(self, req, platform_name: str):
        data = req.to_snake_dict()
        validate_required_fields(data, REQUIRED_FIELDS_CO)

        pi = data["payment_instructions"]

        if platform_name == "CASH_PICKUP_CO":
            validate_required_fields(
                pi, REQUIRED_PAYMENT_CASH_CO, "paymentInstructions"
            )

        elif platform_name == "INTERBANK_TRANSFER_CO":
            validate_required_fields(
                pi, REQUIRED_PAYMENT_INTERBANK_CO, "paymentInstructions"
            )


CO_VALIDATOR = ColombiaValidator()
