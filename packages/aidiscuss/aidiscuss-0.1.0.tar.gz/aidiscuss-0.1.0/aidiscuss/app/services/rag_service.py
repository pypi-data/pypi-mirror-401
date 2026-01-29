"""
RAG Service for document processing and retrieval
Simplified version with user-controlled model loading

Features:
- User controls when to load/unload embedding model via toggle
- Model downloads once and caches locally (~/.cache/huggingface/)
- Progress tracking for model loading
- Simple, predictable behavior
"""

import os
import gc
import logging
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import chromadb
from chromadb.config import Settings
from chromadb.api.types import EmbeddingFunction, Documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from nanoid import generate

from aidiscuss.app.core.config import settings as app_settings

logger = logging.getLogger("aidiscuss.rag")


class SentenceTransformerEmbeddingFunction(EmbeddingFunction):
    """ChromaDB embedding function wrapper for SentenceTransformer
    
    This custom implementation allows us to control model loading/unloading
    for memory management, while remaining compatible with ChromaDB's API.
    """

    def __init__(self, model):
        """Initialize with an already-loaded SentenceTransformer model.
        
        Args:
            model: A loaded SentenceTransformer model instance
        """
        if model is None:
            raise ValueError("Model cannot be None")
        self._model = model

    def __call__(self, input: Documents) -> list:
        """Generate embeddings for the input documents.
        
        Args:
            input: List of text documents to embed
            
        Returns:
            List of embedding vectors as lists of floats
        """
        try:
            embeddings = self._model.encode(input, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise


class RAGService:
    """Service for document processing and vector search using ChromaDB
    
    Features:
    - User-controlled embedding model loading/unloading
    - Persistent vector storage with ChromaDB
    - Namespace-based document organization
    - Automatic model download and caching
    """

    def __init__(self, vector_store_path: Optional[str] = None):
        # Use DATA_DIR/vector_stores by default for unified storage
        if vector_store_path is None:
            vector_store_path = str(app_settings.DATA_DIR / "vector_stores")

        self.vector_store_path = vector_store_path
        os.makedirs(vector_store_path, exist_ok=True)

        # Initialize ChromaDB persistent client (lightweight)
        self.client = chromadb.PersistentClient(
            path=vector_store_path,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            ),
        )

        # Embedding model - not loaded by default
        self._embedding_model: Optional[object] = None
        self.model_name = "all-MiniLM-L6-v2"
        self.embedding_dimension = 384
        self._is_loading = False
        self._load_progress = 0  # 0-100

        # Initialize text splitter (lightweight)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512, chunk_overlap=50, length_function=len
        )

    def is_model_loaded(self) -> bool:
        """Check if embedding model is currently loaded"""
        return self._embedding_model is not None

    def is_loading(self) -> bool:
        """Check if model is currently loading"""
        return self._is_loading

    def get_load_progress(self) -> int:
        """Get current loading progress (0-100)"""
        return self._load_progress
    
    def _get_embedding_function(self) -> SentenceTransformerEmbeddingFunction:
        """Get the embedding function for ChromaDB operations.
        
        Returns:
            Embedding function wrapper
            
        Raises:
            RuntimeError: If embedding model is not loaded
        """
        if self._embedding_model is None:
            raise RuntimeError(
                "Embedding model not loaded. Please load the model first using "
                "the RAG control panel or by calling load_model()."
            )
        return SentenceTransformerEmbeddingFunction(self._embedding_model)
    
    def _get_or_create_collection_safely(self, namespace: str):
        """Safely get or create a collection, handling existing collections.
        
        ChromaDB persists embedding functions with collections. If a collection
        already exists, we must get it without specifying a new embedding function.
        
        Args:
            namespace: Collection name
            
        Returns:
            ChromaDB collection object
        """
        # Check if collection already exists
        try:
            existing_collections = [col.name for col in self.client.list_collections()]
            
            if namespace in existing_collections:
                # Collection exists - get it without embedding function
                # ChromaDB will use the persisted embedding function
                return self.client.get_collection(name=namespace)
            else:
                # Collection doesn't exist - create with our embedding function
                embedding_fn = self._get_embedding_function()
                return self.client.create_collection(
                    name=namespace,
                    metadata={
                        "hnsw:space": "cosine",
                        "model_name": self.model_name,
                        "embedding_dimension": self.embedding_dimension,
                    },
                    embedding_function=embedding_fn,
                )
        except Exception as e:
            logger.error(f"Error managing collection '{namespace}': {e}")
            raise

    def get_status(self) -> Dict[str, any]:
        """Get current RAG service status"""
        return {
            "model_loaded": self.is_model_loaded(),
            "is_loading": self._is_loading,
            "load_progress": self._load_progress,
            "namespaces": self.get_namespaces() if self.is_model_loaded() else [],
        }

    def load_model(self) -> Dict[str, any]:
        """
        Load the embedding model.
        Model is downloaded once and cached in ~/.cache/huggingface/
        Subsequent loads are much faster.

        Returns:
            Status dict with success/error information
        """
        if self._embedding_model is not None:
            logger.info("Embedding model already loaded")
            return {"success": True, "message": "Model already loaded", "cached": True}

        if self._is_loading:
            return {"success": False, "message": "Model is currently loading"}

        try:
            self._is_loading = True
            self._load_progress = 10

            logger.info("Loading embedding model (all-MiniLM-L6-v2)...")
            logger.info("First load will download ~80MB model to cache")

            self._load_progress = 30

            # Import and load model
            from sentence_transformers import SentenceTransformer

            self._load_progress = 50

            # Model downloads to ~/.cache/huggingface/ on first run
            # Subsequent runs load from cache (much faster)
            self._embedding_model = SentenceTransformer(self.model_name)

            self._load_progress = 90

            logger.info("Embedding model loaded successfully")
            self._load_progress = 100

            return {
                "success": True,
                "message": "Model loaded successfully",
                "cached": False,  # TODO: detect if loaded from cache
            }

        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            self._embedding_model = None
            return {"success": False, "message": f"Failed to load model: {str(e)}"}

        finally:
            self._is_loading = False

    def unload_model(self) -> Dict[str, any]:
        """
        Unload the embedding model from memory to free RAM.
        The model remains cached on disk for fast reloading.

        Returns:
            Status dict with success information
        """
        if self._embedding_model is None:
            logger.info("Embedding model not loaded")
            return {"success": True, "message": "Model not loaded"}

        try:
            logger.info("Unloading embedding model from memory...")
            self._embedding_model = None
            self._load_progress = 0

            # Force garbage collection to free memory
            gc.collect()

            logger.info("Embedding model unloaded successfully")
            return {
                "success": True,
                "message": "Model unloaded successfully",
                "note": "Model cached on disk for fast reloading",
            }

        except Exception as e:
            logger.error(f"Error unloading model: {e}")
            return {"success": False, "message": f"Error unloading model: {str(e)}"}

    def process_document(
        self, file_path: str, file_type: str
    ) -> List[Tuple[str, dict]]:
        """
        Process document and extract chunks

        Args:
            file_path: Path to document
            file_type: File extension (.pdf, .txt, .md)

        Returns:
            List of (chunk_text, metadata) tuples
        """
        # Load document
        if file_type == ".pdf":
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path, encoding="utf-8")

        documents = loader.load()

        # Split into chunks
        chunks = self.text_splitter.split_documents(documents)

        # Extract text and metadata
        result = []
        for i, chunk in enumerate(chunks):
            result.append(
                (
                    chunk.page_content,
                    {
                        "chunk_index": i,
                        "source": chunk.metadata.get("source", file_path),
                        "page": chunk.metadata.get("page", None),
                    },
                )
            )

        return result

    def generate_embeddings(self, texts: List[str]):
        """Generate embeddings for texts (requires model to be loaded)"""
        if self._embedding_model is None:
            raise RuntimeError("Embedding model not loaded. Call load_model() first.")

        return self._embedding_model.encode(texts, convert_to_numpy=True)

    def add_documents(
        self,
        namespace: str,
        document_id: str,
        chunks: List[Tuple[str, dict]],
    ) -> int:
        """
        Add document chunks to vector store

        Args:
            namespace: Collection namespace
            document_id: Unique document ID
            chunks: List of (text, metadata) tuples

        Returns:
            Number of chunks added
            
        Raises:
            RuntimeError: If embedding model is not loaded
            ValueError: If chunks list is invalid
        """
        if not chunks:
            return 0

        # Ensure model is loaded (will raise RuntimeError if not)
        self._get_embedding_function()

        try:
            # Get or create collection safely
            collection = self._get_or_create_collection_safely(namespace)

            # Prepare data
            ids = [generate() for _ in chunks]
            texts = [chunk[0] for chunk in chunks]
            
            # Prepare metadata, filtering out None values (ChromaDB doesn't accept None)
            metadatas = []
            for chunk in chunks:
                metadata = {"document_id": document_id}
                # Only add non-None values from chunk metadata
                for key, value in chunk[1].items():
                    if value is not None:
                        metadata[key] = value
                metadatas.append(metadata)

            # Add to collection
            collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas,
            )

            return len(chunks)
            
        except Exception as e:
            logger.error(f"Failed to add documents to namespace '{namespace}': {e}")
            raise

    def search(
        self,
        query: str,
        namespace: str = "default",
        k: int = 5,
        min_score: float = 0.0,
    ) -> List[dict]:
        """
        Search for relevant chunks

        Args:
            query: Search query
            namespace: Collection namespace
            k: Number of results (must be > 0)
            min_score: Minimum similarity score (0-1)

        Returns:
            List of chunk dicts with content, metadata, and score
            
        Raises:
            RuntimeError: If embedding model is not loaded
            ValueError: If k <= 0
        """
        if k <= 0:
            raise ValueError(f"k must be positive, got {k}")
            
        # Ensure model is loaded (will raise RuntimeError if not)
        self._get_embedding_function()

        try:
            # Get existing collection (without embedding function - uses persisted one)
            existing_collections = [col.name for col in self.client.list_collections()]
            if namespace not in existing_collections:
                return []
                
            collection = self.client.get_collection(name=namespace)
        except Exception as e:
            logger.error(f"Error accessing collection '{namespace}': {e}")
            return []

        try:
            # Query collection
            results = collection.query(
                query_texts=[query],
                n_results=k,
            )
        except Exception as e:
            logger.error(f"Error querying collection '{namespace}': {e}")
            return []

        # Check if results are empty
        if not results["ids"] or not results["ids"][0]:
            return []

        # Format results
        formatted = []
        for i in range(len(results["ids"][0])):
            distance = results["distances"][0][i]
            score = 1 / (1 + distance)

            if score >= min_score:
                formatted.append(
                    {
                        "chunk_id": results["ids"][0][i],
                        "document_id": results["metadatas"][0][i].get(
                            "document_id", ""
                        ),
                        "content": results["documents"][0][i],
                        "score": float(score),
                        "metadata": results["metadatas"][0][i],
                    }
                )

        return formatted

    def delete_document(self, namespace: str, document_id: str) -> int:
        """
        Delete document chunks from vector store

        Args:
            namespace: Collection namespace
            document_id: Document ID to delete

        Returns:
            Number of chunks deleted
        """
        try:
            collection = self.client.get_collection(name=namespace)

            result = collection.get(
                where={"document_id": {"$eq": document_id}},
            )
            count = len(result["ids"]) if result["ids"] else 0

            collection.delete(
                where={"document_id": {"$eq": document_id}},
            )

            return count

        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return 0

    def get_namespaces(self) -> List[str]:
        """Get list of available namespaces (collections)"""
        collections = self.client.list_collections()
        return [col.name for col in collections]

    def get_stats(self, namespace: str) -> dict:
        """Get statistics for namespace"""
        try:
            collection = self.client.get_collection(name=namespace)

            total_chunks = collection.count()

            all_data = collection.get()
            unique_docs = set()
            if all_data["metadatas"]:
                unique_docs = {
                    meta.get("document_id")
                    for meta in all_data["metadatas"]
                    if meta.get("document_id")
                }

            return {
                "exists": True,
                "total_chunks": total_chunks,
                "unique_documents": len(unique_docs),
            }

        except Exception:
            return {"exists": False}


# Global instance - model NOT loaded on import (fast startup)
# Vector store will be created in DATA_DIR/vector_stores
rag_service = RAGService()
