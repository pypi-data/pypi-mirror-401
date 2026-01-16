"""
Potion API Client

Main client classes for interacting with the Potion API.
"""

from typing import Optional, Dict, Any
import httpx

from .resources.formulations import FormulationsResource, AsyncFormulationsResource
from .resources.ingredients import IngredientsResource, AsyncIngredientsResource
from .resources.sop import SOPResource, AsyncSOPResource
from .resources.labeling import LabelingResource, AsyncLabelingResource
from .resources.assistant import AssistantResource, AsyncAssistantResource
from .resources.supply_chain import SupplyChainResource, AsyncSupplyChainResource
from .resources.compliance import ComplianceResource, AsyncComplianceResource
from .resources.webhooks import WebhooksResource, AsyncWebhooksResource
from .resources.sandbox import SandboxResource, AsyncSandboxResource


class BaseClient:
    """Base client with shared configuration."""

    DEFAULT_BASE_URL = "https://api.potion.com"
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_MAX_RETRIES = 3

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ):
        if not api_key:
            raise ValueError("API key is required")

        if not api_key.startswith(("pk_live_", "pk_sandbox_")):
            raise ValueError(
                "Invalid API key format. Keys must start with 'pk_live_' or 'pk_sandbox_'"
            )

        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.max_retries = max_retries or self.DEFAULT_MAX_RETRIES

        self._is_sandbox = api_key.startswith("pk_sandbox_")

    @property
    def is_sandbox(self) -> bool:
        """Check if using sandbox mode."""
        return self._is_sandbox

    def _get_headers(self) -> Dict[str, str]:
        """Get default request headers."""
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": f"potion-python/1.0.0",
        }


class Potion(BaseClient):
    """
    Synchronous Potion API client.

    Usage:
        client = Potion(api_key="pk_live_your_key_here")
        formulation = client.formulations.generate(...)
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ):
        super().__init__(api_key, base_url, timeout, max_retries)

        # Initialize HTTP client
        self._client = httpx.Client(
            base_url=self.base_url,
            headers=self._get_headers(),
            timeout=self.timeout,
        )

        # Initialize resource clients
        self.formulations = FormulationsResource(self._client)
        self.ingredients = IngredientsResource(self._client)
        self.sop = SOPResource(self._client)
        self.labeling = LabelingResource(self._client)
        self.assistant = AssistantResource(self._client)
        self.supply_chain = SupplyChainResource(self._client)
        self.compliance = ComplianceResource(self._client)
        self.webhooks = WebhooksResource(self._client)
        self.sandbox = SandboxResource(self._client)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the HTTP client."""
        self._client.close()


class AsyncPotion(BaseClient):
    """
    Asynchronous Potion API client.

    Usage:
        async with AsyncPotion(api_key="pk_live_your_key_here") as client:
            formulation = await client.formulations.generate(...)
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ):
        super().__init__(api_key, base_url, timeout, max_retries)

        # Initialize async HTTP client
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self._get_headers(),
            timeout=self.timeout,
        )

        # Initialize async resource clients
        self.formulations = AsyncFormulationsResource(self._client)
        self.ingredients = AsyncIngredientsResource(self._client)
        self.sop = AsyncSOPResource(self._client)
        self.labeling = AsyncLabelingResource(self._client)
        self.assistant = AsyncAssistantResource(self._client)
        self.supply_chain = AsyncSupplyChainResource(self._client)
        self.compliance = AsyncComplianceResource(self._client)
        self.webhooks = AsyncWebhooksResource(self._client)
        self.sandbox = AsyncSandboxResource(self._client)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the async HTTP client."""
        await self._client.aclose()
