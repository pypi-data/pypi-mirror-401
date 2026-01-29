"""
LLM Provider Service - creates LangChain chat models from providers
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from aidiscuss.app.models.provider import Provider
from aidiscuss.app.models.agent import Agent


class ProviderService:
    """Service for creating LLM instances from providers"""

    @staticmethod
    def create_chat_model(provider: Provider, agent: Agent) -> BaseChatModel:
        """
        Create a LangChain chat model from provider and agent config

        Args:
            provider: Provider with API key
            agent: Agent configuration

        Returns:
            BaseChatModel instance

        Raises:
            ValueError: If provider type is unsupported or API key is missing
        """
        api_key = provider.get_api_key()
        if not api_key:
            raise ValueError(f"No API key set for provider '{provider.id}'")

        temperature = float(agent.temperature)
        max_tokens = int(agent.max_tokens) if agent.max_tokens else None

        # OpenAI and compatible providers
        if provider.id in ["openai", "openrouter", "together"]:
            return ChatOpenAI(
                api_key=api_key,
                base_url=provider.base_url,
                model=agent.model,
                temperature=temperature,
                max_tokens=max_tokens,
                streaming=True,
            )

        # Anthropic
        elif provider.id == "anthropic":
            return ChatAnthropic(
                api_key=api_key,
                model=agent.model,
                temperature=temperature,
                max_tokens=max_tokens or 1024,
                streaming=True,
            )

        # Google
        elif provider.id == "google":
            return ChatGoogleGenerativeAI(
                google_api_key=api_key,
                model=agent.model,
                temperature=temperature,
                max_output_tokens=max_tokens,
                streaming=True,
            )

        # Groq
        elif provider.id == "groq":
            return ChatGroq(
                api_key=api_key,
                model=agent.model,
                temperature=temperature,
                max_tokens=max_tokens,
                streaming=True,
            )

        else:
            raise ValueError(f"Unsupported provider: {provider.id}")
