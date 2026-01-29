"""
Vector store manager for RAG system
Manages vector database operations (FAISS for simplicity and no external dependencies)
"""
import os
import pickle
from typing import List, Optional, Dict, Any
from pathlib import Path
from javis.modules.config import setup_logging

logger = setup_logging()

try:
    from langchain_core.documents import Document
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import OpenAIEmbeddings
    from langchain_huggingface import HuggingFaceEmbeddings
    LANGCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("LangChain not installed. RAG features will be disabled.")
    LANGCHAIN_AVAILABLE = False
    Document = None
    FAISS = None
    OpenAIEmbeddings = None
    HuggingFaceEmbeddings = None


class VectorStoreManager:
    """Manage vector database for code retrieval"""

    def __init__(self,
                 storage_dir: str = "/tmp/javis_rag",
                 embeddings_model: str = "text-embedding-3-small",
                 mode: str = "retrieval_only",
                 embeddings_backend: str = "sentence_transformers"):
        """
        Initialize vector store manager

        Args:
            storage_dir: Directory to store vector database
            embeddings_model: Embeddings model name
            mode: "retrieval_only" (default, local) or "full_rag" (OpenAI)
            embeddings_backend: 
                - "openai": OpenAI API (fast, cloud, costs money)
                - "huggingface": HuggingFace models (local, free, slower)
                - "sentence_transformers": SentenceTransformer (local, fast on CPU, multilingual)
        """
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain is required for RAG features. Install with: pip install langchain langchain-openai langchain-community faiss-cpu sentence-transformers")

        self.storage_dir = storage_dir
        self.embeddings_model = embeddings_model
        self.vectorstore = None

        # Chọn backend embedding
        if embeddings_backend == "openai":
            self.embeddings = OpenAIEmbeddings(model=embeddings_model)
            logger.info(f"VectorStoreManager using OpenAIEmbeddings: {embeddings_model}")
        elif embeddings_backend == "sentence_transformers":
            # Dùng SentenceTransformer với model tối ưu cho CPU và đa ngôn ngữ
            # Nếu không chỉ định model, dùng paraphrase-multilingual-MiniLM-L12-v2
            if embeddings_model == "text-embedding-3-small":
                embeddings_model = "paraphrase-multilingual-MiniLM-L12-v2"
            self.embeddings = HuggingFaceEmbeddings(
                model_name=embeddings_model,
                model_kwargs={'device': 'cpu'},  # Force CPU
                encode_kwargs={'normalize_embeddings': True}  # Normalize for better similarity
            )
            logger.info(f"VectorStoreManager using SentenceTransformers: {embeddings_model} (CPU optimized, multilingual)")
        else:
            # Default: HuggingFace with all-MiniLM-L6-v2
            self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            logger.info(f"VectorStoreManager using HuggingFaceEmbeddings: all-MiniLM-L6-v2")

        # Create storage directory
        Path(storage_dir).mkdir(parents=True, exist_ok=True)

        logger.info(f"VectorStoreManager initialized with storage: {storage_dir}, mode: {mode}, embeddings_backend: {embeddings_backend}")
    
    def create_vectorstore(self, documents: List[Document], index_name: str = "default") -> None:
        """
        Create vector store from documents
        
        Args:
            documents: List of documents to index
            index_name: Name of the index
        """
        if not documents:
            logger.warning("No documents to index")
            return
        
        logger.info(f"Creating vector store from {len(documents)} documents...")
        
        try:
            self.vectorstore = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            
            # Save to disk
            index_path = os.path.join(self.storage_dir, f"{index_name}.faiss")
            self.vectorstore.save_local(index_path)
            
            logger.info(f"Vector store created and saved to: {index_path}")
            
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def load_vectorstore(self, index_name: str = "default") -> bool:
        """
        Load vector store from disk
        
        Args:
            index_name: Name of the index to load
            
        Returns:
            True if successful, False otherwise
        """
        index_path = os.path.join(self.storage_dir, f"{index_name}.faiss")
        
        if not os.path.exists(index_path):
            logger.warning(f"Vector store not found: {index_path}")
            return False
        
        try:
            self.vectorstore = FAISS.load_local(
                index_path,
                self.embeddings,
                allow_dangerous_deserialization=True  # Required for FAISS
            )
            logger.info(f"Vector store loaded from: {index_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[Document]:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if not self.vectorstore:
            logger.error("Vector store not initialized. Call create_vectorstore or load_vectorstore first.")
            return []
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} relevant documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []
    
    def search_with_scores(self, query: str, k: int = 5) -> List[tuple]:
        """
        Search with relevance scores
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        if not self.vectorstore:
            logger.error("Vector store not initialized")
            return []
        
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            logger.info(f"Found {len(results)} relevant documents with scores")
            return results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []
    
    def delete_index(self, index_name: str = "default") -> bool:
        """
        Delete vector store index
        
        Args:
            index_name: Name of index to delete
            
        Returns:
            True if successful
        """
        index_path = os.path.join(self.storage_dir, f"{index_name}.faiss")
        
        try:
            if os.path.exists(index_path):
                import shutil
                shutil.rmtree(index_path)
                logger.info(f"Deleted index: {index_path}")
                return True
            else:
                logger.warning(f"Index not found: {index_path}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting index: {e}")
            return False
