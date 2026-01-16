"""
Potion SDK Types

Type definitions for API responses.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import time
import random
import string


# =============================================
# Request Options
# =============================================

@dataclass
class RequestOptions:
    """
    Options for API requests that support idempotency.

    Attributes:
        idempotency_key: Unique key to prevent duplicate operations.
            Must be 10-255 characters, alphanumeric with hyphens and underscores.
            Keys are retained for 24 hours.
    """
    idempotency_key: Optional[str] = None


def generate_idempotency_key() -> str:
    """
    Generate a unique idempotency key.

    Returns:
        A UUID string suitable for use as an idempotency key.

    Example:
        >>> key = generate_idempotency_key()
        >>> formulation = client.formulations.generate(request, options=RequestOptions(idempotency_key=key))
    """
    try:
        return str(uuid.uuid4())
    except Exception:
        # Fallback for environments without uuid
        timestamp = hex(int(time.time() * 1000))[2:]
        random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        return f"{timestamp}-{random_part}"


# =============================================
# Core Types
# =============================================


@dataclass
class NutritionInfo:
    """Nutrition information for a formulation."""
    calories: float = 0
    total_fat_g: float = 0
    sodium_mg: float = 0
    total_carbs_g: float = 0
    sugars_g: float = 0
    protein_g: float = 0
    caffeine_mg: float = 0


@dataclass
class FormulationIngredient:
    """Ingredient in a formulation."""
    id: str
    name: str
    percentage: float


@dataclass
class Formulation:
    """Beverage formulation."""
    id: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    status: str = "draft"
    version: int = 1
    serving_size_ml: Optional[float] = None
    nutrition: Optional[NutritionInfo] = None
    ingredients: List[FormulationIngredient] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Formulation":
        """Create Formulation from API response dict."""
        nutrition = None
        if data.get("nutrition"):
            nutrition = NutritionInfo(**data["nutrition"])

        ingredients = []
        for ing in data.get("ingredients", []):
            ingredients.append(FormulationIngredient(**ing))

        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description"),
            category=data.get("category"),
            status=data.get("status", "draft"),
            version=data.get("version", 1),
            serving_size_ml=data.get("serving_size_ml"),
            nutrition=nutrition,
            ingredients=ingredients,
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


@dataclass
class Ingredient:
    """Ingredient from the database."""
    id: str
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    is_organic: bool = False
    is_natural: bool = False
    allergens: List[str] = field(default_factory=list)
    regulatory: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ingredient":
        return cls(
            id=data["id"],
            name=data["name"],
            category=data.get("category"),
            description=data.get("description"),
            is_organic=data.get("is_organic", False),
            is_natural=data.get("is_natural", False),
            allergens=data.get("allergens", []),
            regulatory=data.get("regulatory"),
        )


@dataclass
class SOPSection:
    """Section in an SOP document."""
    title: str
    content: str


@dataclass
class HACCPPlan:
    """HACCP plan in an SOP."""
    hazard_analysis: List[Dict[str, Any]]
    critical_control_points: int
    monitoring_procedures: str


@dataclass
class SOPDocument:
    """Standard Operating Procedure document."""
    id: str
    formulation_id: str
    title: str
    version: str
    sections: List[SOPSection] = field(default_factory=list)
    haccp_plan: Optional[HACCPPlan] = None
    generated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SOPDocument":
        sections = [SOPSection(**s) for s in data.get("sections", [])]
        haccp = None
        if data.get("haccp_plan"):
            haccp = HACCPPlan(**data["haccp_plan"])

        return cls(
            id=data["id"],
            formulation_id=data["formulation_id"],
            title=data["title"],
            version=data["version"],
            sections=sections,
            haccp_plan=haccp,
            generated_at=data.get("generated_at"),
        )


@dataclass
class LabelingRequirements:
    """Labeling requirements for a formulation."""
    id: str
    formulation_id: str
    label_requirements: Dict[str, Any]
    regulatory_compliance: Dict[str, Any]
    claims_eligibility: Dict[str, Any]
    generated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LabelingRequirements":
        return cls(
            id=data["id"],
            formulation_id=data["formulation_id"],
            label_requirements=data.get("label_requirements", {}),
            regulatory_compliance=data.get("regulatory_compliance", {}),
            claims_eligibility=data.get("claims_eligibility", {}),
            generated_at=data.get("generated_at"),
        )


@dataclass
class Location:
    """Geographic location."""
    city: str
    state: str
    country: str = "USA"


@dataclass
class Copacker:
    """Contract manufacturer/copacker."""
    id: str
    name: str
    location: Location
    capabilities: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    minimum_order: Optional[Dict[str, int]] = None
    lead_time_weeks: Optional[int] = None
    rating: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Copacker":
        location = Location(**data["location"])
        return cls(
            id=data["id"],
            name=data["name"],
            location=location,
            capabilities=data.get("capabilities", []),
            certifications=data.get("certifications", []),
            minimum_order=data.get("minimum_order"),
            lead_time_weeks=data.get("lead_time_weeks"),
            rating=data.get("rating"),
        )


@dataclass
class Distributor:
    """Beverage distributor."""
    id: str
    name: str
    coverage: Dict[str, Any]
    specialties: List[str] = field(default_factory=list)
    requirements: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Distributor":
        return cls(
            id=data["id"],
            name=data["name"],
            coverage=data.get("coverage", {}),
            specialties=data.get("specialties", []),
            requirements=data.get("requirements"),
        )


@dataclass
class Webhook:
    """Webhook configuration."""
    id: str
    url: str
    events: List[str]
    is_active: bool = True
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Webhook":
        return cls(
            id=data["id"],
            url=data["url"],
            events=data.get("events", []),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
        )


@dataclass
class Message:
    """Chat message."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None


@dataclass
class Conversation:
    """Assistant conversation."""
    id: str
    title: Optional[str] = None
    messages: List[Message] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conversation":
        messages = [Message(**m) for m in data.get("messages", [])]
        return cls(
            id=data["id"],
            title=data.get("title"),
            messages=messages,
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


@dataclass
class ComplianceCheck:
    """Compliance check results."""
    formulation_id: str
    overall_status: str
    checked_at: str
    regulations: Dict[str, Any]
    recommendations: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ComplianceCheck":
        return cls(
            formulation_id=data["formulation_id"],
            overall_status=data["overall_status"],
            checked_at=data["checked_at"],
            regulations=data.get("regulations", {}),
            recommendations=data.get("recommendations", []),
        )


@dataclass
class SandboxStatus:
    """Sandbox environment status."""
    environment: str
    organization: Dict[str, Any]
    usage: Dict[str, int]
    sample_data: Dict[str, int]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SandboxStatus":
        return cls(
            environment=data["environment"],
            organization=data.get("organization", {}),
            usage=data.get("usage", {}),
            sample_data=data.get("sample_data", {}),
        )
