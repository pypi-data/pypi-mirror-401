"""
Offline Service - Phase 6
Manages local model integration (Ollama) and offline capabilities
"""

import aiohttp
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
import json


class LocalModel(BaseModel):
    """Local model information"""
    name: str
    size: str
    modified_at: datetime
    digest: str
    details: Dict[str, Any] = Field(default_factory=dict)


class OllamaModelInfo(BaseModel):
    """Detailed Ollama model information"""
    name: str
    model: str
    size: int
    digest: str
    modified_at: str
    format: str = "gguf"
    family: str = "llama"
    families: Optional[List[str]] = None
    parameter_size: str = "7B"
    quantization_level: str = "Q4_0"


class ModelPullProgress(BaseModel):
    """Progress information for model pulling"""
    status: str
    digest: Optional[str] = None
    total: Optional[int] = None
    completed: Optional[int] = None


class OfflineService:
    """
    Service for managing offline/local model capabilities

    Features:
    - Ollama integration
    - Local model discovery and management
    - Model pulling and caching
    - Offline-first architecture support
    """

    def __init__(self, ollama_base_url: str = "http://localhost:11434"):
        self.ollama_base_url = ollama_base_url
        self.available_models: List[LocalModel] = []
        self.last_refresh: Optional[datetime] = None

    async def check_ollama_available(self) -> bool:
        """
        Check if Ollama is running and accessible

        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_base_url}/api/tags", timeout=aiohttp.ClientTimeout(total=3)) as response:
                    return response.status == 200
        except Exception as e:
            print(f"Ollama not available: {e}")
            return False

    async def list_local_models(self, force_refresh: bool = False) -> List[LocalModel]:
        """
        List all locally available Ollama models

        Args:
            force_refresh: Force refresh from Ollama API

        Returns:
            List of local models
        """
        # Return cached if recent and not forcing refresh
        if not force_refresh and self.last_refresh:
            age = (datetime.now() - self.last_refresh).seconds
            if age < 60:  # Cache for 60 seconds
                return self.available_models

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_base_url}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        models = []

                        for model_data in data.get("models", []):
                            model = LocalModel(
                                name=model_data["name"],
                                size=self._format_size(model_data.get("size", 0)),
                                modified_at=datetime.fromisoformat(model_data["modified_at"].replace("Z", "+00:00")),
                                digest=model_data["digest"],
                                details=model_data.get("details", {})
                            )
                            models.append(model)

                        self.available_models = models
                        self.last_refresh = datetime.now()
                        return models

        except Exception as e:
            print(f"Error listing Ollama models: {e}")

        return []

    async def get_model_info(self, model_name: str) -> Optional[OllamaModelInfo]:
        """
        Get detailed information about a specific model

        Args:
            model_name: Name of the model

        Returns:
            Model information or None if not found
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_base_url}/api/show",
                    json={"name": model_name}
                ) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Extract model details
                        details = data.get("details", {})
                        modelfile = data.get("modelfile", "")

                        return OllamaModelInfo(
                            name=model_name,
                            model=data.get("model", model_name),
                            size=data.get("size", 0),
                            digest=data.get("digest", ""),
                            modified_at=data.get("modified_at", datetime.now().isoformat()),
                            format=details.get("format", "gguf"),
                            family=details.get("family", "llama"),
                            families=details.get("families"),
                            parameter_size=details.get("parameter_size", "unknown"),
                            quantization_level=details.get("quantization_level", "unknown")
                        )

        except Exception as e:
            print(f"Error getting model info for {model_name}: {e}")

        return None

    async def pull_model(self, model_name: str, progress_callback: Optional[callable] = None) -> bool:
        """
        Pull a model from Ollama registry

        Args:
            model_name: Name of model to pull (e.g., "llama2", "mistral")
            progress_callback: Optional callback for progress updates

        Returns:
            True if successful, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_base_url}/api/pull",
                    json={"name": model_name},
                    timeout=aiohttp.ClientTimeout(total=None)  # No timeout for large downloads
                ) as response:
                    if response.status == 200:
                        # Stream progress updates
                        async for line in response.content:
                            if line:
                                try:
                                    progress_data = json.loads(line)

                                    if progress_callback:
                                        progress = ModelPullProgress(**progress_data)
                                        progress_callback(progress)

                                    # Check if complete
                                    if progress_data.get("status") == "success":
                                        # Refresh model list
                                        await self.list_local_models(force_refresh=True)
                                        return True

                                except json.JSONDecodeError:
                                    continue

        except Exception as e:
            print(f"Error pulling model {model_name}: {e}")
            return False

        return False

    async def delete_model(self, model_name: str) -> bool:
        """
        Delete a local model

        Args:
            model_name: Name of model to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    f"{self.ollama_base_url}/api/delete",
                    json={"name": model_name}
                ) as response:
                    if response.status == 200:
                        # Refresh model list
                        await self.list_local_models(force_refresh=True)
                        return True

        except Exception as e:
            print(f"Error deleting model {model_name}: {e}")

        return False

    async def generate_completion(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Generate completion using local Ollama model

        Args:
            model: Model name
            prompt: User prompt
            system: System prompt (optional)
            temperature: Temperature for generation
            max_tokens: Max tokens to generate
            stream: Whether to stream response

        Returns:
            Generation result
        """
        try:
            options = {
                "temperature": temperature,
            }
            if max_tokens:
                options["num_predict"] = max_tokens

            request_data = {
                "model": model,
                "prompt": prompt,
                "stream": stream,
                "options": options
            }

            if system:
                request_data["system"] = system

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_base_url}/api/generate",
                    json=request_data
                ) as response:
                    if response.status == 200:
                        if stream:
                            # Return streaming response
                            return {"streaming": True, "response": response}
                        else:
                            result = await response.json()
                            return {
                                "response": result.get("response", ""),
                                "model": result.get("model", model),
                                "context": result.get("context", []),
                                "total_duration": result.get("total_duration", 0),
                                "load_duration": result.get("load_duration", 0),
                                "prompt_eval_count": result.get("prompt_eval_count", 0),
                                "eval_count": result.get("eval_count", 0),
                            }

        except Exception as e:
            print(f"Error generating completion: {e}")
            return {"error": str(e)}

        return {"error": "Generation failed"}

    async def generate_completion_stream(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ):
        """
        Generate completion using local Ollama model with streaming

        Args:
            model: Model name
            prompt: User prompt
            system: System prompt (optional)
            temperature: Temperature for generation
            max_tokens: Max tokens to generate

        Yields:
            Streaming chunks with response tokens
        """
        try:
            options = {
                "temperature": temperature,
            }
            if max_tokens:
                options["num_predict"] = max_tokens

            request_data = {
                "model": model,
                "prompt": prompt,
                "stream": True,
                "options": options
            }

            if system:
                request_data["system"] = system

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_base_url}/api/generate",
                    json=request_data
                ) as response:
                    if response.status == 200:
                        # Stream response line by line
                        async for line in response.content:
                            if line:
                                try:
                                    import json
                                    chunk_data = json.loads(line.decode('utf-8'))

                                    # Yield the chunk
                                    yield {
                                        "response": chunk_data.get("response", ""),
                                        "done": chunk_data.get("done", False),
                                        "model": chunk_data.get("model", model),
                                    }

                                    # If done, include final metadata
                                    if chunk_data.get("done"):
                                        yield {
                                            "done": True,
                                            "total_duration": chunk_data.get("total_duration", 0),
                                            "load_duration": chunk_data.get("load_duration", 0),
                                            "prompt_eval_count": chunk_data.get("prompt_eval_count", 0),
                                            "eval_count": chunk_data.get("eval_count", 0),
                                        }
                                        break

                                except json.JSONDecodeError as e:
                                    print(f"Error decoding chunk: {e}")
                                    continue
                    else:
                        yield {"error": f"HTTP {response.status}: Generation failed"}

        except Exception as e:
            print(f"Error in streaming generation: {e}")
            yield {"error": str(e)}

    def get_recommended_models(self) -> List[Dict[str, str]]:
        """
        Get list of recommended models for offline use

        Returns:
            List of recommended models with descriptions
        """
        return [
            {
                "name": "llama3.2",
                "size": "2GB",
                "description": "Latest Llama 3.2 model, great for general use",
                "category": "general"
            },
            {
                "name": "llama3.2:1b",
                "size": "1.3GB",
                "description": "Smaller Llama 3.2, faster responses",
                "category": "general"
            },
            {
                "name": "mistral",
                "size": "4GB",
                "description": "Mistral 7B, excellent quality/performance balance",
                "category": "general"
            },
            {
                "name": "phi3",
                "size": "2.3GB",
                "description": "Microsoft Phi-3, compact and capable",
                "category": "general"
            },
            {
                "name": "codellama",
                "size": "4GB",
                "description": "Code-specialized Llama model",
                "category": "coding"
            },
            {
                "name": "gemma2:2b",
                "size": "1.6GB",
                "description": "Google Gemma 2B, very fast",
                "category": "general"
            },
        ]

    def _format_size(self, size_bytes: int) -> str:
        """Format size in bytes to human-readable string"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}PB"

    async def get_offline_status(self) -> Dict[str, Any]:
        """
        Get comprehensive offline capabilities status

        Returns:
            Status information
        """
        ollama_available = await self.check_ollama_available()
        local_models = await self.list_local_models() if ollama_available else []

        return {
            "ollama_available": ollama_available,
            "ollama_url": self.ollama_base_url,
            "local_models_count": len(local_models),
            "local_models": [
                {
                    "name": m.name,
                    "size": m.size,
                    "modified_at": m.modified_at.isoformat()
                }
                for m in local_models
            ],
            "recommended_models": self.get_recommended_models(),
            "can_run_offline": ollama_available and len(local_models) > 0
        }


# Singleton instance
offline_service = OfflineService()
