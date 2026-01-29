"""
LEANN Vector Store Adapter for JAVIS RAG
Provides an alternative to FAISS with 97% storage savings
"""
import os
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from javis.modules.config import setup_logging

logger = setup_logging()

try:
    from langchain_core.documents import Document
    LANGCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("LangChain not installed. RAG features will be disabled.")
    LANGCHAIN_AVAILABLE = False
    Document = None

try:
    from leann.api import LeannBuilder, LeannSearcher
    LEANN_AVAILABLE = True
except ImportError:
    logger.warning("LEANN not installed. Install with: pip install leann")
    LEANN_AVAILABLE = False
    LeannBuilder = None
    LeannSearcher = None


class LeannVectorStore:
    """LEANN-based vector store for code retrieval with 97% storage savings"""

    def __init__(self,
                 storage_dir: str = "/tmp/javis_rag",
                 embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 backend: str = "hnsw"):
        """
        Initialize LEANN vector store

        Args:
            storage_dir: Directory to store LEANN index
            embeddings_model: Embedding model name (sentence-transformers format)
            backend: LEANN backend ('hnsw' or 'diskann')
        """
        if not LEANN_AVAILABLE:
            raise ImportError(
                "LEANN is required. Install with:\n"
                "  uv pip install leann\n"
                "Or:\n"
                "  pip install leann"
            )

        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain is required for Document handling")

        self.storage_dir = storage_dir
        self.embeddings_model = embeddings_model
        self.backend = backend
        self.searcher: Optional[LeannSearcher] = None
        
        # For compatibility with FAISS VectorStoreManager interface
        # This property will be set to self.searcher when index is loaded
        self.vectorstore: Optional[LeannSearcher] = None

        # Create storage directory
        Path(storage_dir).mkdir(parents=True, exist_ok=True)

        logger.info(
            f"LeannVectorStore initialized with storage: {storage_dir}, "
            f"model: {embeddings_model}, backend: {backend}"
        )
    
    def create_vectorstore(self, documents: List[Document], index_name: str = "default") -> None:
        """
        Create LEANN index from documents

        Args:
            documents: List of documents to index
            index_name: Name of the index
        """
        if not documents:
            logger.warning("No documents to index")
            return

        logger.info(f"Creating LEANN index from {len(documents)} documents...")

        try:
            # Build LEANN index path
            index_path = os.path.join(self.storage_dir, f"{index_name}.leann")
            
            # Initialize LEANN builder with correct parameters
            builder = LeannBuilder(
                backend_name=self.backend,
                embedding_model=self.embeddings_model,
                embedding_mode="sentence-transformers"
            )
            
            # Add each document as a text chunk with metadata
            logger.info(f"Adding {len(documents)} chunks to LEANN builder...")
            for i, doc in enumerate(documents, 1):
                builder.add_text(text=doc.page_content, metadata=doc.metadata)
                if i % 100 == 0:
                    logger.info(f"Added {i}/{len(documents)} chunks...")
            
            # Build the index (this may take several minutes for large datasets)
            logger.info(f"Building LEANN index... (this may take 5-15 minutes for {len(documents)} chunks)")
            builder.build_index(index_path=index_path)

            logger.info(f"LEANN index created at: {index_path}")
            logger.info(f"Successfully indexed {len(documents)} documents")

        except Exception as e:
            logger.error(f"Error creating LEANN index: {e}")
            raise
    
    def load_vectorstore(self, index_name: str = "default") -> bool:
        """
        Load LEANN index from disk

        Args:
            index_name: Name of the index to load

        Returns:
            True if successful, False otherwise
        """
        # LEANN creates multiple files: index_name.index, index_name.leann.meta.json, etc.
        # When loading, we need to pass the base path without extension
        # Try both with .leann suffix and with .index
        possible_paths = [
            os.path.join(self.storage_dir, f"{index_name}.leann"),
            os.path.join(self.storage_dir, f"{index_name}.index"),
            os.path.join(self.storage_dir, index_name)
        ]
        
        index_path = None
        for path in possible_paths:
            # Check if metadata file exists (LEANN always creates this)
            meta_path = f"{path}.meta.json"
            if os.path.exists(meta_path):
                index_path = path
                break
        
        if not index_path:
            logger.warning(f"LEANN index not found for: {index_name}")
            logger.warning(f"Tried paths: {possible_paths}")
            return False

        try:
            # LeannSearcher loads embedding model and metadata from the index
            self.searcher = LeannSearcher(index_path=index_path)
            
            # Set vectorstore for compatibility with FAISS interface
            self.vectorstore = self.searcher

            logger.info(f"LEANN index loaded from: {index_path}")
            return True

        except Exception as e:
            logger.error(f"Error loading LEANN index: {e}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[Document]:
        """
        Search for relevant documents using LEANN

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of relevant documents
        """
        if not self.searcher:
            logger.error("LEANN searcher not initialized. Call load_vectorstore first.")
            return []

        try:
            # LEANN search returns SearchResult objects with text and metadata
            results = self.searcher.search(query, top_k=k)
            
            # Convert to LangChain Document format
            documents = []
            for result in results:
                # LEANN SearchResult has: id, score, text, metadata
                metadata = result.metadata.copy() if result.metadata else {}
                metadata['leann_score'] = result.score
                metadata['leann_id'] = result.id
                
                doc = Document(
                    page_content=result.text,
                    metadata=metadata
                )
                documents.append(doc)

            logger.info(f"LEANN found {len(documents)} relevant documents")
            return documents

        except Exception as e:
            logger.error(f"Error searching LEANN index: {e}")
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
        if not self.searcher:
            logger.error("LEANN searcher not initialized")
            return []

        try:
            # LEANN search returns SearchResult objects with text and metadata
            results = self.searcher.search(query, top_k=k)
            
            doc_score_pairs = []
            for result in results:
                # LEANN SearchResult has: id, score, text, metadata
                metadata = result.metadata.copy() if result.metadata else {}
                metadata['leann_id'] = result.id
                
                doc = Document(page_content=result.text, metadata=metadata)
                doc_score_pairs.append((doc, result.score))

            logger.info(f"LEANN found {len(doc_score_pairs)} results with scores")
            return doc_score_pairs

        except Exception as e:
            logger.error(f"Error searching LEANN index: {e}")
            return []
    
    def delete_index(self, index_name: str = "default") -> bool:
        """
        Delete LEANN index

        Args:
            index_name: Name of index to delete

        Returns:
            True if successful
        """
        index_path = os.path.join(self.storage_dir, f"{index_name}.leann")
        metadata_path = os.path.join(self.storage_dir, f"{index_name}.metadata.json")

        try:
            deleted = False
            if os.path.exists(index_path):
                import shutil
                shutil.rmtree(index_path)
                logger.info(f"Deleted LEANN index: {index_path}")
                deleted = True
            
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
                logger.info(f"Deleted metadata: {metadata_path}")
                deleted = True
            
            if not deleted:
                logger.warning(f"Index not found: {index_name}")
                return False
            
            return True

        except Exception as e:
            logger.error(f"Error deleting index: {e}")
            return False
