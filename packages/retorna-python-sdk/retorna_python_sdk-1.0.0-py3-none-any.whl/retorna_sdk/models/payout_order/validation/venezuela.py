from re import compile

from .utils import validate_required_fields

REQUIRED_FIELDS_VE = {
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

PAYMENT_REQUIREMENTS_VE = {
    "BANK_TRANSFER": {"required": {"bank_name", "account_number", "account_type"}},
    "P2P_PHONE_TRANSFER": {"required": {"bank_name", "phone_number"}},
    "CASH_PICKUP_USD_VE": {"required": set()},
}

P2P_PHONE_REGEX = compile(r"^\+58\-(424|414|412|426|416)\d{7}$")


class VenezuelaValidator:
    @staticmethod
    def validate(req, platform_name: str):
        data = req.to_dict()
        validate_required_fields(data, REQUIRED_FIELDS_VE)

        pi = data["payment_instructions"]
        required = PAYMENT_REQUIREMENTS_VE[platform_name]["required"]

        validate_required_fields(pi, required, "paymentInstructions")

        if platform_name == "P2P_PHONE_TRANSFER":
            phone = pi.get("phone_number")
            if not P2P_PHONE_REGEX.match(phone):
                raise ValueError(
                    "Invalid phone_number for P2P_PHONE_TRANSFER. "
                    "Expected format: +58-4XXYYYYYYY"
                )


VE_VALIDATOR = VenezuelaValidator()
