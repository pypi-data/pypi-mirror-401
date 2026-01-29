"""
API Key validation router
Provides endpoints for testing and validating API keys for various providers
Uses existing LangChain libraries for validation
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

router = APIRouter()


class KeyValidationRequest(BaseModel):
    """Request body for key validation"""
    provider: str
    key: str


class KeyValidationResponse(BaseModel):
    """Response for key validation"""
    success: bool
    error: Optional[str] = None
    details: Optional[dict] = None


async def validate_openai_key(api_key: str, base_url: Optional[str] = None) -> tuple[bool, Optional[str], Optional[dict]]:
    """
    Validate OpenAI-compatible API key using LangChain

    Args:
        api_key: API key to validate
        base_url: Optional base URL for OpenAI-compatible providers

    Returns:
        (success, error_message, details)
    """
    try:
        # Create a minimal chat model instance
        llm = ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model="gpt-3.5-turbo",  # Use cheapest model
            max_tokens=1,
            temperature=0
        )

        # Try to invoke with minimal tokens to test the key
        response = await llm.ainvoke([HumanMessage(content="test")])

        return True, None, {"message": "Key is valid"}

    except Exception as e:
        error_msg = str(e)

        # Parse common error messages
        if "401" in error_msg or "Unauthorized" in error_msg or "Invalid" in error_msg:
            return False, "Invalid API key", None
        elif "429" in error_msg or "rate_limit" in error_msg:
            return False, "Rate limit exceeded", None
        elif "quota" in error_msg.lower():
            return False, "Quota exceeded or billing issue", None
        else:
            return False, f"Connection error: {error_msg}", None


async def validate_anthropic_key(api_key: str) -> tuple[bool, Optional[str], Optional[dict]]:
    """
    Validate Anthropic API key using LangChain

    Returns:
        (success, error_message, details)
    """
    try:
        # Create a minimal chat model instance
        llm = ChatAnthropic(
            api_key=api_key,
            model="claude-3-5-haiku-20241022",  # Use cheapest model
            max_tokens=1,
            temperature=0
        )

        # Try to invoke with minimal tokens to test the key
        response = await llm.ainvoke([HumanMessage(content="test")])

        return True, None, {"message": "Key is valid"}

    except Exception as e:
        error_msg = str(e)

        # Parse common error messages
        if "401" in error_msg or "authentication" in error_msg.lower() or "invalid" in error_msg.lower():
            return False, "Invalid API key", None
        elif "429" in error_msg or "rate_limit" in error_msg:
            return False, "Rate limit exceeded", None
        elif "overloaded" in error_msg.lower():
            return False, "API is overloaded, try again", None
        else:
            return False, f"Connection error: {error_msg}", None


async def validate_google_key(api_key: str) -> tuple[bool, Optional[str], Optional[dict]]:
    """
    Validate Google/Gemini API key using LangChain

    Returns:
        (success, error_message, details)
    """
    try:
        # Create a minimal chat model instance
        llm = ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model="gemini-2.0-flash-exp",
            max_output_tokens=1,
            temperature=0
        )

        # Try to invoke with minimal tokens to test the key
        response = await llm.ainvoke([HumanMessage(content="test")])

        return True, None, {"message": "Key is valid"}

    except Exception as e:
        error_msg = str(e)

        # Parse common error messages
        if "400" in error_msg or "invalid" in error_msg.lower() or "API_KEY" in error_msg:
            return False, "Invalid API key", None
        elif "429" in error_msg or "quota" in error_msg.lower():
            return False, "Rate limit or quota exceeded", None
        else:
            return False, f"Connection error: {error_msg}", None


@router.post("/validate", response_model=KeyValidationResponse)
async def validate_key(request: KeyValidationRequest):
    """
    Validate an API key for a specific provider

    This endpoint uses LangChain libraries to make minimal API calls
    and verify the key is valid and has the necessary permissions.
    """
    provider = request.provider.lower()
    api_key = request.key.strip()

    # Basic format validation first
    if not api_key:
        raise HTTPException(status_code=400, detail="API key cannot be empty")

    # Route to appropriate validator based on provider
    try:
        if provider == "openai":
            success, error, details = await validate_openai_key(api_key)
        elif provider == "anthropic":
            success, error, details = await validate_anthropic_key(api_key)
        elif provider in ["google", "gemini"]:
            success, error, details = await validate_google_key(api_key)
        elif provider == "openrouter":
            success, error, details = await validate_openai_key(
                api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        elif provider == "groq":
            success, error, details = await validate_openai_key(
                api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        elif provider == "together":
            success, error, details = await validate_openai_key(
                api_key,
                base_url="https://api.together.xyz/v1"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported provider: {provider}. Supported: openai, anthropic, google, openrouter, groq, together"
            )

        return KeyValidationResponse(
            success=success,
            error=error,
            details=details
        )

    except HTTPException:
        raise
    except Exception as e:
        # Catch any unexpected errors
        return KeyValidationResponse(
            success=False,
            error=f"Validation failed: {str(e)}",
            details=None
        )


@router.get("/supported-providers")
async def get_supported_providers():
    """
    Get list of providers that support key validation
    """
    return {
        "providers": [
            {
                "id": "openai",
                "name": "OpenAI",
                "key_format": "sk-*",
                "validation_method": "LangChain ChatOpenAI"
            },
            {
                "id": "anthropic",
                "name": "Anthropic",
                "key_format": "sk-ant-*",
                "validation_method": "LangChain ChatAnthropic"
            },
            {
                "id": "google",
                "name": "Google/Gemini",
                "key_format": "AIza*",
                "validation_method": "LangChain ChatGoogleGenerativeAI"
            },
            {
                "id": "openrouter",
                "name": "OpenRouter",
                "key_format": "sk-or-*",
                "validation_method": "LangChain ChatOpenAI (OpenRouter)"
            },
            {
                "id": "groq",
                "name": "Groq",
                "key_format": "gsk_*",
                "validation_method": "LangChain ChatOpenAI (Groq)"
            },
            {
                "id": "together",
                "name": "Together AI",
                "key_format": "*",
                "validation_method": "LangChain ChatOpenAI (Together)"
            }
        ]
    }
