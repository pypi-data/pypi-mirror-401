from .utils import validate_required_fields

REQUIRED_FIELDS_PE = {
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

PAYMENT_REQUIREMENTS_PE = {
    "BANK_TRANSFER_USD_PE": {"required": {"account_number", "account_type"}},
    "BANK_TRANSFER_PEN_PE": {"required": {"account_number", "account_type"}},
    "CASH_PICKUP_PEN_PE": {"required": {"bank_name"}},
    "WALLET_PEN_PE": {"required": {"bank_name", "account_number"}},
}


class PeruValidator:
    def validate(self, req, platform_name: str):
        data = req.to_snake_dict()
        validate_required_fields(data, REQUIRED_FIELDS_PE)

        pi = data["payment_instructions"]
        cfg = PAYMENT_REQUIREMENTS_PE.get(platform_name)

        if cfg:
            validate_required_fields(pi, cfg["required"], "paymentInstructions")


PE_VALIDATOR = PeruValidator()
