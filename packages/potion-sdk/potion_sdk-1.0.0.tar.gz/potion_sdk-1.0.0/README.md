# Potion Python SDK

Official Python SDK for the Potion API - AI-powered beverage formulation platform.

## Installation

```bash
pip install potion-sdk
```

## Quick Start

```python
from potion import Potion

# Initialize the client
client = Potion(api_key="pk_live_your_key_here")

# Generate a formulation
formulation = client.formulations.generate(
    prompt="A refreshing citrus energy drink with natural caffeine",
    category="nonalc",
    subcategory="csd.energy_drink",
    constraints=["natural", "under-100-calories"]
)

print(f"Created: {formulation.name}")
print(f"Calories: {formulation.nutrition.calories}")
```

## Features

- **Type hints** - Full type annotations for IDE support
- **Async support** - Both sync and async clients available
- **Automatic retries** - Built-in retry logic with exponential backoff
- **Streaming** - Support for SSE streaming responses
- **Rate limiting** - Automatic rate limit handling

## Usage

### Formulations

```python
# List formulations
formulations = client.formulations.list(limit=20, status="active")

# Get a specific formulation
formulation = client.formulations.get("formulation-uuid")

# Generate with AI
formulation = client.formulations.generate(
    prompt="Low-sugar probiotic kombucha",
    category="nonalc",
    subcategory="functional.kombucha"
)

# Create variations
variations = client.formulations.create_variations(
    formulation_id="formulation-uuid",
    variation_type="flavor",
    count=3
)

# Get substitutions
substitutions = client.formulations.get_substitutions(
    formulation_id="formulation-uuid",
    ingredient_name="Organic Cane Sugar",
    reason="cost"
)
```

### Ingredients

```python
# List ingredients
ingredients = client.ingredients.list(category="sweetener")

# Search ingredients
results = client.ingredients.search("natural caffeine")

# Augment ingredient with AI
augmented = client.ingredients.augment(
    ingredient_name="Guarana Extract",
    physical_state="solid"
)

# Batch augment
batch_results = client.ingredients.augment_batch([
    "Stevia",
    "Monk Fruit Extract",
    "Erythritol"
])

# Check compatibility
compatibility = client.ingredients.check_compatibility(
    ingredient_name="Citric Acid",
    with_ingredients=["Sodium Benzoate", "Potassium Sorbate"]
)
```

### SOP Generation

```python
# Generate SOP for a formulation
sop = client.sop.generate(
    formulation_id="formulation-uuid",
    production_scale="commercial",
    include_haccp=True
)

# Get SOP profiles
profiles = client.sop.list_profiles()

# Retrieve existing SOP
sop = client.sop.get("sop-uuid")
```

### Labeling

```python
# Generate labeling requirements
labeling = client.labeling.generate(
    formulation_id="formulation-uuid",
    container_size_ml=355,
    serving_size_ml=355,
    target_markets=["US", "CA"]
)

# Check claims eligibility
claims = client.labeling.check_claims(
    formulation_id="formulation-uuid",
    claims=["organic", "non_gmo", "low_calorie", "natural"]
)
```

### Assistant

```python
# Chat with the assistant
response = client.assistant.chat(
    message="What's the best natural sweetener for an energy drink?",
    formulation_id="formulation-uuid"  # Optional context
)

# Streaming response
for chunk in client.assistant.chat_stream(
    message="Explain the FDA requirements for caffeine labeling"
):
    print(chunk.content, end="", flush=True)

# List conversations
conversations = client.assistant.list_conversations()

# Get conversation history
conversation = client.assistant.get_conversation("conversation-uuid")
```

### Supply Chain

```python
# Search copackers
copackers = client.supply_chain.search_copackers(
    capabilities=["hot_fill", "aseptic"],
    state="CA",
    certifications=["SQF", "Organic"]
)

# Get AI recommendations
recommendations = client.supply_chain.recommend_copackers(
    formulation_id="formulation-uuid",
    requirements={
        "min_volume": 10000,
        "certifications": ["Organic"]
    }
)

# Search distributors
distributors = client.supply_chain.search_distributors(
    region="West Coast",
    channels=["natural_grocery", "specialty"]
)
```

### Compliance

```python
# Run compliance check
compliance = client.compliance.check(
    formulation_id="formulation-uuid",
    target_states=["CA", "NY", "TX"]
)

# Get DTC shipping rules
dtc_rules = client.compliance.get_dtc_shipping(
    states=["CA", "NY"],
    product_type="non_alcoholic_beverage"
)

# Get regulatory updates
updates = client.compliance.get_updates(
    category="fda",
    since="2024-01-01"
)
```

### Webhooks

```python
# Create webhook
webhook = client.webhooks.create(
    url="https://your-server.com/webhook",
    events=["formulation.created", "formulation.updated"],
    secret="your-webhook-secret"
)

# List webhooks
webhooks = client.webhooks.list()

# Test webhook
result = client.webhooks.test(
    webhook_id="webhook-uuid",
    event_type="formulation.created"
)

# Get delivery history
deliveries = client.webhooks.get_deliveries("webhook-uuid")
```

## Async Usage

```python
from potion import AsyncPotion

async def main():
    client = AsyncPotion(api_key="pk_live_your_key_here")

    # All methods are async
    formulation = await client.formulations.generate(
        prompt="Sparkling elderflower lemonade",
        category="nonalc",
        subcategory="csd.sparkling_water"
    )

    print(formulation.name)

import asyncio
asyncio.run(main())
```

## Idempotency

Prevent duplicate operations on retries using idempotency keys:

```python
from potion import Potion, generate_idempotency_key, RequestOptions

client = Potion(api_key="pk_live_your_key_here")

# Generate a unique idempotency key
idempotency_key = generate_idempotency_key()

# Use the key for mutation operations
formulation = client.formulations.generate(
    prompt="A refreshing citrus energy drink",
    category="nonalc",
    subcategory="csd.energy_drink",
    options=RequestOptions(idempotency_key=idempotency_key)
)

# If you retry with the same key, you'll get the cached response
# This prevents duplicate formulations from being created
```

Idempotency keys:
- Must be 10-255 characters (alphanumeric, hyphens, underscores)
- Are retained for 24 hours
- Only apply to mutation operations (POST, PUT, PATCH, DELETE)

## Error Handling

```python
from potion import Potion
from potion.exceptions import (
    PotionError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError
)

client = Potion(api_key="pk_live_your_key_here")

try:
    formulation = client.formulations.get("invalid-uuid")
except NotFoundError as e:
    print(f"Formulation not found: {e.message}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Details: {e.details}")
except PotionError as e:
    print(f"API error: {e.code} - {e.message}")
```

## Configuration

```python
from potion import Potion

client = Potion(
    api_key="pk_live_your_key_here",

    # Optional configuration
    base_url="https://api.potion.com",  # Custom base URL
    timeout=30.0,                        # Request timeout in seconds
    max_retries=3,                       # Max retry attempts

    # Sandbox mode (use pk_sandbox_* keys)
    # api_key="pk_sandbox_your_key_here"
)
```

## Sandbox Mode

Use sandbox keys for development and testing:

```python
from potion import Potion

# Use sandbox key
client = Potion(api_key="pk_sandbox_your_key_here")

# Check sandbox status
status = client.sandbox.get_status()
print(f"Requests remaining: {status.usage.requests_limit - status.usage.requests_today}")

# Reset sandbox data
client.sandbox.reset()

# Load test scenario
client.sandbox.load_scenario("energy-drink-launch")
```

## Requirements

- Python 3.8+
- httpx >= 0.24.0

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: https://potion.com/documentation
- API Reference: https://potion.com/api/v1/docs
- Email: api-support@potion.com
