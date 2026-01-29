"""
Vector Store Factory
Factory pattern để switch giữa FAISS và LEANN backends
"""
import os
from typing import Union
from javis.modules.config import setup_logging

logger = setup_logging()


class VectorStoreFactory:
    """Factory để tạo vector store theo backend type"""
    
    @staticmethod
    def create_vector_store(
        backend: str = "faiss",
        storage_dir: str = "/tmp/javis_rag",
        embeddings_model: str = "paraphrase-multilingual-MiniLM-L12-v2",
        mode: str = "retrieval_only",
        embeddings_backend: str = "sentence_transformers"
    ):
        """
        Create vector store based on backend type
        
        Args:
            backend: Vector store backend ('faiss' or 'leann')
            storage_dir: Directory to store index
            embeddings_model: Embedding model name
            mode: "retrieval_only" or "full_rag" (chỉ cho FAISS)
            embeddings_backend: 
                - "sentence_transformers" (default, tối ưu CPU, đa ngôn ngữ, local)
                - "openai" (cloud, nhanh, tốn phí)
                - "huggingface" (local, free)
        Returns:
            VectorStoreManager or LeannVectorStore instance
        """
        backend = backend.lower()
        
        if backend == "leann":
            logger.info("Creating LEANN vector store...")
            from javis.rag.leann_store import LeannVectorStore
            
            # LEANN dùng sentence-transformers format
            if embeddings_model == "text-embedding-3-small":
                embeddings_model = "sentence-transformers/all-MiniLM-L6-v2"
            
            return LeannVectorStore(
                storage_dir=storage_dir,
                embeddings_model=embeddings_model,
                backend="hnsw"  # hoặc "diskann"
            )
            
        elif backend == "faiss":
            logger.info(f"Creating FAISS vector store with embeddings_backend={embeddings_backend}...")
            from javis.rag.vector_store import VectorStoreManager
            
            return VectorStoreManager(
                storage_dir=storage_dir,
                embeddings_model=embeddings_model,
                mode=mode,
                embeddings_backend=embeddings_backend
            )
            
        else:
            raise ValueError(
                f"Unknown backend: {backend}. "
                f"Supported backends: 'faiss', 'leann'"
            )
    
    @staticmethod
    def get_available_backends() -> list:
        """Get list of available backends"""
        backends = []
        
        # Check FAISS
        try:
            from langchain_community.vectorstores import FAISS
            backends.append("faiss")
        except ImportError:
            pass
        
        # Check LEANN
        try:
            from leann.api import LeannBuilder
            backends.append("leann")
        except ImportError:
            pass
        
        return backends
    
    @staticmethod
    def get_backend_info(backend: str) -> dict:
        """Get information about a specific backend"""
        info = {
            "faiss": {
                "name": "FAISS",
                "description": "Facebook AI Similarity Search - Traditional vector DB",
                "storage": "High (stores all embeddings)",
                "speed": "Very fast",
                "privacy": "Depends on embedding model",
                "install": "pip install faiss-cpu langchain-community"
            },
            "leann": {
                "name": "LEANN",
                "description": "Lightweight Efficient Approximate Nearest Neighbor",
                "storage": "97% less than FAISS (graph-based recomputation)",
                "speed": "Fast (on-demand embedding computation)",
                "privacy": "100% local (no OpenAI needed)",
                "install": "pip install leann"
            }
        }
        
        embedding_info = {
            "sentence_transformers": {
                "name": "SentenceTransformers",
                "description": "Optimized for CPU, multilingual, local embedding",
                "speed": "Fast on CPU (10-50ms/text)",
                "privacy": "100% local (no API calls)",
                "cost": "Free",
                "recommended_model": "paraphrase-multilingual-MiniLM-L12-v2",
                "install": "pip install sentence-transformers"
            },
            "openai": {
                "name": "OpenAI Embeddings",
                "description": "Cloud-based embedding API",
                "speed": "Very fast (cloud infrastructure)",
                "privacy": "Data sent to OpenAI",
                "cost": "$0.0001 per 1K tokens",
                "recommended_model": "text-embedding-3-small",
                "install": "pip install openai"
            },
            "huggingface": {
                "name": "HuggingFace Embeddings",
                "description": "Open-source models from HuggingFace",
                "speed": "Slow on CPU (depends on model size)",
                "privacy": "100% local",
                "cost": "Free",
                "recommended_model": "sentence-transformers/all-MiniLM-L6-v2",
                "install": "pip install sentence-transformers"
            }
        }
        
        return info.get(backend.lower(), embedding_info.get(backend.lower(), {}))


def get_recommended_backend(codebase_size_mb: int = 0) -> str:
    """
    Recommend backend based on codebase size
    
    Args:
        codebase_size_mb: Size of codebase in MB
        
    Returns:
        Recommended backend name
    """
    # Nếu codebase > 100MB hoặc muốn privacy, recommend LEANN
    if codebase_size_mb > 100:
        return "leann"
    
    # Ngược lại, FAISS cũng OK cho codebase nhỏ
    return "faiss"
