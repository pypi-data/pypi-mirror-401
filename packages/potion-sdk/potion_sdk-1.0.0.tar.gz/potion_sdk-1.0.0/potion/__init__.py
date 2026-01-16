"""
Potion Python SDK

Official Python SDK for the Potion API - AI-powered beverage formulation platform.

Basic usage:
    from potion import Potion

    client = Potion(api_key="pk_live_your_key_here")
    formulation = client.formulations.generate(
        prompt="A refreshing citrus energy drink",
        category="nonalc",
        subcategory="csd.energy_drink"
    )
"""

__version__ = "1.0.0"
__author__ = "Potion"
__email__ = "api-support@potion.com"

from .client import Potion, AsyncPotion
from .exceptions import (
    PotionError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    ConflictError,
    ServerError,
)
from .types import (
    Formulation,
    Ingredient,
    SOPDocument,
    LabelingRequirements,
    Copacker,
    Distributor,
    Webhook,
    Conversation,
    ComplianceCheck,
    RequestOptions,
    generate_idempotency_key,
)

__all__ = [
    # Version
    "__version__",
    # Clients
    "Potion",
    "AsyncPotion",
    # Exceptions
    "PotionError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "ServerError",
    # Types
    "Formulation",
    "Ingredient",
    "SOPDocument",
    "LabelingRequirements",
    "Copacker",
    "Distributor",
    "Webhook",
    "Conversation",
    "ComplianceCheck",
    # Request options
    "RequestOptions",
    # Utilities
    "generate_idempotency_key",
]
