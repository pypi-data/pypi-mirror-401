from typing import TYPE_CHECKING

from ..account import AccountClient
from ..core import (AuthService, HttpClient, SignatureService,
                    SignedHttpClient, TokenManager, create_sdk_logger,
                    resolve_env_config)
from ..models import CreatePayoutOrderRequest, CreateQuotationRequest
from ..payout_order import PayoutOrderClient
from ..quotation import QuotationClient

if TYPE_CHECKING:
    from ..core import SDKConfig


class RetornaClient:
    """Primary client for interacting with the Retorna API."""

    def __init__(self, config: "SDKConfig"):
        self.config = config
        self.credentials = config.credentials
        self.retry_config = config.retry_config

        self.logger = create_sdk_logger(config=config.logging_config)

        self.env_config = resolve_env_config(
            environment=config.environment,
            base_url_override=config.base_url_override,
            scope_override=config.scope_override,
        )
        self.base_url = self.env_config.base_url
        self.scope = self.env_config.scope
        self.logger.debug(f"[RetornaClient] Base URL: {self.base_url}")

        self.signature_service = SignatureService(
            private_key_pem=self.credentials.private_key
        )

        self.http_client = HttpClient(
            base_url=self.base_url, retry_config=self.retry_config, logger=self.logger
        )

        self.auth_service = AuthService(
            http_client=self.http_client,
            credentials=self.credentials,
            environment=self.env_config,
            logger=self.logger,
        )

        self.token_manager = TokenManager(
            auth_service=self.auth_service, logger=self.logger
        )

        self.signed_client = SignedHttpClient(
            http_client=self.http_client,
            signature_service=self.signature_service,
            token_manager=self.token_manager,
            logger=self.logger,
        )

        self.account_client = AccountClient(self.signed_client)

        self.quotation_client = QuotationClient(self.signed_client)

        self.payout_order_client = PayoutOrderClient(self.signed_client)

    def get_balance(self):
        return self.account_client.get_balance()

    def get_routes(self):
        return self.account_client.get_routes()

    def create_quotation(self, request: CreateQuotationRequest):
        return self.quotation_client.create_quotation(request)

    def get_quotation_by_id(self, quotation_id: str):
        return self.quotation_client.get_quotation_by_id(quotation_id)

    def create_payout_order(
        self, platform_name: str, request: CreatePayoutOrderRequest
    ):
        return self.payout_order_client.create(platform_name, request)

    def get_payout_order_by_id(self, payout_order_id: str):
        return self.payout_order_client.get_by_id(payout_order_id)
