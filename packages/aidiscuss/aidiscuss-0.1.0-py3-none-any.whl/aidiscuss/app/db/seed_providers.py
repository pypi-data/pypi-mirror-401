"""
Default provider seeding
Seeds 4 built-in providers (OpenAI, Anthropic, Gemini, Groq) with default models.
- Users can add custom models to providers (isDefault=False)
- Users cannot delete/modify default models (isDefault=True)
- Each model has its own pricing and capabilities
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aidiscuss.app.models.provider import Provider


DEFAULT_PROVIDERS = [
    {
        "id": "openai",
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "is_active": True,
        "meta": {
            "models": [
                {
                    "id": "gpt-4o",
                    "name": "GPT-4o",
                    "contextLength": 128000,
                    "supportsTools": True,
                    "costTier": "premium",
                    "isDefault": True,
                    "pricing": {"input": 0.0025, "output": 0.01},
                },
                {
                    "id": "gpt-4o-mini",
                    "name": "GPT-4o Mini",
                    "contextLength": 128000,
                    "supportsTools": True,
                    "costTier": "standard",
                    "isDefault": True,
                    "pricing": {"input": 0.00015, "output": 0.0006},
                },
                {
                    "id": "o1-preview",
                    "name": "O1 Preview",
                    "contextLength": 128000,
                    "supportsTools": False,
                    "costTier": "premium",
                    "isDefault": True,
                    "pricing": {"input": 0.015, "output": 0.06},
                },
                {
                    "id": "o1-mini",
                    "name": "O1 Mini",
                    "contextLength": 128000,
                    "supportsTools": False,
                    "costTier": "standard",
                    "isDefault": True,
                    "pricing": {"input": 0.003, "output": 0.012},
                },
                {
                    "id": "gpt-3.5-turbo",
                    "name": "GPT-3.5 Turbo",
                    "contextLength": 16385,
                    "supportsTools": True,
                    "costTier": "cheap",
                    "isDefault": True,
                    "pricing": {"input": 0.0005, "output": 0.0015},
                },
            ],
            "capabilities": {
                "supportsStreaming": True,
                "supportsTools": True,
                "supportsVision": False,
                "corsOk": False,
            },
        },
    },
    {
        "id": "anthropic",
        "name": "Anthropic",
        "base_url": "https://api.anthropic.com/v1",
        "is_active": True,
        "meta": {
            "models": [
                {
                    "id": "claude-3-5-sonnet-20241022",
                    "name": "Claude 3.5 Sonnet",
                    "contextLength": 200000,
                    "supportsTools": True,
                    "costTier": "premium",
                    "isDefault": True,
                    "pricing": {"input": 0.003, "output": 0.015},
                },
                {
                    "id": "claude-3-5-haiku-20241022",
                    "name": "Claude 3.5 Haiku",
                    "contextLength": 200000,
                    "supportsTools": True,
                    "costTier": "standard",
                    "isDefault": True,
                    "pricing": {"input": 0.0008, "output": 0.004},
                },
                {
                    "id": "claude-3-haiku-20240307",
                    "name": "Claude 3 Haiku",
                    "contextLength": 200000,
                    "supportsTools": True,
                    "costTier": "standard",
                    "isDefault": True,
                    "pricing": {"input": 0.00025, "output": 0.00125},
                },
            ],
            "capabilities": {
                "supportsStreaming": True,
                "supportsTools": True,
                "supportsVision": False,
                "corsOk": False,
            },
        },
    },
    {
        "id": "gemini",
        "name": "Google Gemini",
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "is_active": True,
        "meta": {
            "models": [
                {
                    "id": "gemini-2.0-flash",
                    "name": "Gemini 2.0 Flash",
                    "contextLength": 1000000,
                    "supportsTools": True,
                    "costTier": "standard",
                    "isDefault": True,
                    "pricing": {"input": 0.0, "output": 0.0},
                },
            ],
            "capabilities": {
                "supportsStreaming": True,
                "supportsTools": True,
                "supportsVision": False,
                "corsOk": False,
            },
        },
    },
    {
        "id": "groq",
        "name": "Groq",
        "base_url": "https://api.groq.com/openai/v1",
        "is_active": True,
        "meta": {
            "models": [
                {
                    "id": "llama-3.3-70b-versatile",
                    "name": "Llama 3.3 70B Versatile",
                    "contextLength": 128000,
                    "supportsTools": True,
                    "costTier": "cheap",
                    "isDefault": True,
                    "pricing": {"input": 0.00059, "output": 0.00079},
                },
                {
                    "id": "llama-3.1-70b-versatile",
                    "name": "Llama 3.1 70B Versatile",
                    "contextLength": 128000,
                    "supportsTools": True,
                    "costTier": "cheap",
                    "isDefault": True,
                    "pricing": {"input": 0.00059, "output": 0.00079},
                },
                {
                    "id": "llama-3.1-8b-instant",
                    "name": "Llama 3.1 8B Instant",
                    "contextLength": 128000,
                    "supportsTools": True,
                    "costTier": "free",
                    "isDefault": True,
                    "pricing": {"input": 0.00005, "output": 0.00008},
                },
                {
                    "id": "mixtral-8x7b-32768",
                    "name": "Mixtral 8x7B",
                    "contextLength": 32768,
                    "supportsTools": True,
                    "costTier": "cheap",
                    "isDefault": True,
                    "pricing": {"input": 0.00024, "output": 0.00024},
                },
                {
                    "id": "gemma2-9b-it",
                    "name": "Gemma 2 9B",
                    "contextLength": 8192,
                    "supportsTools": True,
                    "costTier": "free",
                    "isDefault": True,
                    "pricing": {"input": 0.0002, "output": 0.0002},
                },
            ],
            "capabilities": {
                "supportsStreaming": True,
                "supportsTools": True,
                "supportsVision": False,
                "corsOk": False,
            },
        },
    },
]


async def seed_default_providers(db: AsyncSession):
    """
    Seed default providers if they don't exist.
    Idempotent: Safe to call multiple times (no duplicates).
    """
    for provider_data in DEFAULT_PROVIDERS:
        result = await db.execute(
            select(Provider).where(Provider.id == provider_data["id"])
        )
        existing = result.scalar_one_or_none()

        if not existing:
            provider = Provider(
                id=provider_data["id"],
                name=provider_data["name"],
                base_url=provider_data["base_url"],
                is_active=provider_data["is_active"],
                meta=provider_data["meta"],
            )
            db.add(provider)

    await db.commit()
