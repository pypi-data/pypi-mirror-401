"""
RAG Service - Dual mode support
Mode 1 (default): Retrieval-only - Return context for Copilot to handle
Mode 2 (optional): Full RAG - Use OpenAI API to generate answers
"""
import os
from typing import List, Dict, Any, Optional
from javis.modules.config import setup_logging

logger = setup_logging()

try:
    from langchain_core.documents import Document
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    LANGCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("LangChain not installed. RAG features will be disabled.")
    LANGCHAIN_AVAILABLE = False
    Document = None

try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    ChatOpenAI = None


class RAGService:
    """RAG service with dual mode support"""
    
    def __init__(self, vector_store_manager, mode: str = "retrieval_only", model_name: str = "gpt-3.5-turbo"):
        """
        Initialize RAG service
        
        Args:
            vector_store_manager: VectorStoreManager instance
            mode: "retrieval_only" (default, for Copilot) or "full_rag" (use OpenAI)
            model_name: LLM model name (only used if mode="full_rag")
        """
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain is required. Install with: pip install langchain langchain-community")
        
        self.vector_store_manager = vector_store_manager
        self.mode = mode
        self.llm = None
        
        if mode == "full_rag":
            if not OPENAI_AVAILABLE:
                raise ImportError("langchain-openai required for full_rag mode. Install: pip install langchain-openai")
            self.llm = ChatOpenAI(model_name=model_name, temperature=0)
            logger.info(f"RAGService initialized in FULL_RAG mode with {model_name}")
        else:
            logger.info("RAGService initialized in RETRIEVAL_ONLY mode (Copilot handles generation)")
    
    def search_code(self, question: str, top_k: int = 30) -> List:
        """
        Search for relevant code snippets
        
        Args:
            question: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        logger.info(f"Searching for: {question}")
        
        # Search vector store
        documents = self.vector_store_manager.search(question, k=top_k)
        
        logger.info(f"Found {len(documents)} relevant code snippets")
        return documents
    
    def format_context_for_copilot(self, documents: List, question: str) -> str:
        """
        Format retrieved documents as context for Copilot with citations
        
        Args:
            documents: List of retrieved documents
            question: Original question
            
        Returns:
            Formatted context string for Copilot with citation metadata
        """
        if not documents:
            return "No relevant code found in the indexed codebase."
        
        context_parts = [
            f"# Code Context for: {question}\n",
            f"Found {len(documents)} relevant code snippets:\n"
        ]
        
        for i, doc in enumerate(documents, 1):
            metadata = doc.metadata
            file_path = metadata.get('relative_path', 'unknown')
            file_name = metadata.get('file_name', 'unknown')
            file_type = metadata.get('file_type', '')
            page_number = metadata.get('page_number', None)
            section_title = metadata.get('section_title', None)
            line_range = metadata.get('line_range', None)
            
            # Build citation info (NO chunk_index - not useful for users)
            citation_parts = [f"**Source:** {file_name}"]
            
            # Ưu tiên hiển thị section/heading nếu có
            if section_title:
                citation_parts.append(f"**Section:** {section_title}")
            
            if page_number:
                citation_parts.append(f"**Page:** {page_number}")
            
            if line_range:
                citation_parts.append(f"**Lines:** {line_range}")
            
            # Thêm đoạn text trích dẫn để có thể search trong tài liệu gốc
            # Giới hạn 150 ký tự, loại bỏ newline để dễ đọc
            search_text = doc.page_content[:150].replace('\n', ' ').strip()
            if len(doc.page_content) > 150:
                search_text += "..."
            citation_parts.append(f"**Preview:** {search_text}")
            
            # Format output
            context_parts.append(f"\n## [{i}] {file_name}\n")
            context_parts.append("\n".join(citation_parts))
            context_parts.append(f"\n```{file_type[1:] if file_type else 'text'}\n")
            context_parts.append(doc.page_content)
            context_parts.append("\n```\n")
        
        return "\n".join(context_parts)
    
    def generate_answer(self, question: str, documents: List) -> str:
        """
        Generate answer using LLM (full_rag mode only)
        
        Args:
            question: User question
            documents: Retrieved documents
            
        Returns:
            Generated answer
        """
        if self.mode != "full_rag" or not self.llm:
            raise RuntimeError("generate_answer only available in full_rag mode")
        
        if not documents:
            return "No relevant code found to answer the question."
        
        # Prompt template for code Q&A
        template = """You are an expert code assistant helping developers understand their codebase.
Use the following code snippets to answer the question accurately and concisely.
If you don't know the answer based on the provided code, say so clearly.
Always reference specific files and line numbers when possible.

Question: {question}

Relevant Code Context:
{context}

Answer:
Provide a clear, technical answer with:
1. Direct answer to the question
2. Reference to specific files/functions
3. Code examples if helpful
4. Any important caveats or notes
"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # Format context from documents
        context_parts = []
        for i, doc in enumerate(documents, 1):
            metadata = doc.metadata
            file_info = f"File: {metadata.get('relative_path', 'unknown')}"
            content = doc.page_content[:1000]  # Limit content size
            context_parts.append(f"[{i}] {file_info}\n```\n{content}\n```\n")
        
        context = "\n\n".join(context_parts)
        
        # Create RAG chain
        rag_chain = prompt | self.llm | StrOutputParser()
        
        # Generate response
        try:
            answer = rag_chain.invoke({
                "context": context,
                "question": question
            })
            return answer
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"Error generating answer: {str(e)}"
