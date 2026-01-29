"""
RAG Handler for MCP Server
Exposes RAG functionality as MCP tools
"""
import os
from typing import List, Union
from mcp import types
from javis.modules.config import setup_logging, get_src_dir, get_config_value

# Load .env file from javis_agent parent directory
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), '../../.env')
    load_dotenv(env_path)
    logger = setup_logging()
    logger.info(f"Loaded .env from: {env_path}")
except ImportError:
    logger = setup_logging()
    logger.warning("python-dotenv not installed, skipping .env loading")
except Exception as e:
    logger = setup_logging()
    logger.warning(f"Could not load .env: {e}")

# Lazy imports to avoid errors when langchain is not installed
_rag_service = None
_vector_store_manager = None
_code_loader = None
_current_backend = None


def _initialize_rag_components():
    """
    Initialize RAG components lazily using config from mcp.json only
    """
    global _rag_service, _vector_store_manager, _code_loader, _current_backend

    # Always re-init if config changes (for dev hot reload)
    try:
        from javis.rag.code_loader import CodeLoader
        from javis.rag.vector_store_factory import VectorStoreFactory
        from javis.rag.rag_service import RAGService

        _code_loader = CodeLoader()

        backend = get_config_value("vector_backend", "faiss")
        rag_mode = get_config_value("rag_mode", "retrieval_only")
        embeddings_backend = get_config_value("embedding_backend", "sentence_transformers")
        embeddings_model = get_config_value("embedding_model", "paraphrase-multilingual-MiniLM-L12-v2")
        
        # Set OPENAI_API_KEY from config if using OpenAI embeddings
        if embeddings_backend == "openai":
            openai_key = get_config_value("openai_api_key") or os.getenv("OPENAI_API_KEY")
            if openai_key:
                os.environ["OPENAI_API_KEY"] = openai_key
                logger.info("OpenAI API key loaded from config")
            else:
                logger.warning("OpenAI embeddings selected but no API key found in .env or mcp.json")

        logger.info(f"Initializing RAG with backend: {backend}, mode: {rag_mode}, embeddings_backend: {embeddings_backend}, embeddings_model: {embeddings_model}")

        _vector_store_manager = VectorStoreFactory.create_vector_store(
            backend=backend,
            mode=rag_mode,
            embeddings_backend=embeddings_backend,
            embeddings_model=embeddings_model
        )

        if rag_mode == "full_rag":
            logger.info("RAG mode: FULL_RAG (OpenAI generates answers)")
            _rag_service = RAGService(_vector_store_manager, mode="full_rag")
        else:
            logger.info("RAG mode: RETRIEVAL_ONLY (Copilot generates answers)")
            _rag_service = RAGService(_vector_store_manager, mode="retrieval_only")

        _current_backend = backend

        logger.info(f"RAG components initialized successfully with {backend.upper()} backend")
        return True

    except ImportError as e:
        logger.error(f"Failed to initialize RAG: {e}")
        logger.error(
            "Install dependencies:\n"
            "  For FAISS: pip install langchain langchain-community faiss-cpu\n"
            "  For LEANN: pip install leann"
        )
        return False
    except Exception as e:
        logger.error(f"Error initializing RAG: {e}")
        return False


async def handle_rag_index_codebase(arguments: dict) -> List[types.TextContent]:
    """
    Index codebase for RAG
    
    Args:
        arguments: {
            "dir": str (optional) - Directory to index, defaults to src_dir
            "index_name": str (optional) - Name for the index, defaults to "default"
            "backend": str (optional) - "faiss" or "leann", defaults to RAG_BACKEND env
            "mode": str (optional) - "retrieval_only" or "full_rag", defaults to env RAG_MODE
        }
    """
    # Get backend from config first (for error messages)
    backend = get_config_value("vector_backend", "faiss")
    
    if not _initialize_rag_components():
        return [types.TextContent(
            type="text",
            text=(
                "❌ RAG not available. Install dependencies:\n"
                f"  For FAISS: pip install langchain langchain-community faiss-cpu\n"
                f"  For LEANN: pip install leann\n"
                f"Current backend: {backend}"
            )
        )]
    
    try:
        dir_path = arguments.get("dir") or get_src_dir()
        index_name = arguments.get("index_name", "default")
        
        logger.info(f"Indexing codebase: {dir_path}")
        
        # Load and chunk documents
        chunks = _code_loader.load_and_chunk(dir_path)
        
        if not chunks:
            return [types.TextContent(
                type="text",
                text=f"❌ No code files found in: {dir_path}"
            )]
        
        # Create vector store
        _vector_store_manager.create_vectorstore(chunks, index_name=index_name)
        
        # Get backend from global or config
        backend_name = _current_backend or backend or "faiss"
        
        result = (
            f"✅ Successfully indexed codebase!\n\n"
            f"🔧 Backend: {backend_name.upper()}\n"
            f"📁 Directory: {dir_path}\n"
            f"📄 Documents: {len(chunks)} chunks\n"
            f"🏷️  Index name: {index_name}\n\n"
            f"You can now query this codebase using 'rag_query_code' tool."
        )
        
        return [types.TextContent(type="text", text=result)]
        
    except Exception as e:
        import traceback
        logger.error(f"Error indexing codebase: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return [types.TextContent(
            type="text",
            text=f"❌ Error indexing codebase: {str(e)}"
        )]


async def handle_rag_query_code(arguments: dict) -> List[types.TextContent]:
    """
    Query codebase using RAG
    
    Args:
        arguments: {
            "question": str - Question to ask
            "index_name": str (optional) - Index to query, defaults to "default"
            "top_k": int (optional) - Number of results, defaults to 30
            "backend": str (optional) - "faiss" or "leann", auto-detect if not specified
            "mode": str (optional) - "retrieval_only" or "full_rag"
        }
    """
    if not _initialize_rag_components():
        return [types.TextContent(
            type="text",
            text="❌ RAG not available. Install dependencies first."
        )]
    
    try:
        question = arguments.get("question")
        if not question:
            return [types.TextContent(
                type="text",
                text="❌ Please provide a 'question' parameter"
            )]
        
        index_name = arguments.get("index_name", "default")
        top_k = arguments.get("top_k", 30)
        
        # Load vector store if needed
        if not _vector_store_manager.vectorstore:
            success = _vector_store_manager.load_vectorstore(index_name)
            if not success:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Index '{index_name}' not found. Please run 'rag_index_codebase' first."
                )]
        
        # Search for relevant code
        logger.info(f"Searching codebase for: {question}")
        documents = _rag_service.search_code(question, top_k=top_k)
        
        # Check mode and respond accordingly
        if _rag_service.mode == "full_rag":
            # Mode 2: Generate answer using OpenAI
            logger.info("Generating answer using OpenAI (full_rag mode)")
            answer = _rag_service.generate_answer(question, documents)
            
            # Format with sources
            result = f"## 🤖 Answer (Generated by OpenAI)\n\n{answer}\n\n"
            
            if documents:
                result += "## 📚 Sources\n\n"
                for i, doc in enumerate(documents, 1):
                    file_path = doc.metadata.get('relative_path', 'unknown')
                    content_preview = doc.page_content[:200] + "..."
                    result += f"**[{i}] {file_path}**\n```\n{content_preview}\n```\n\n"
        else:
            # Mode 1: Return context for Copilot
            logger.info("Returning context for Copilot (retrieval_only mode)")
            context = _rag_service.format_context_for_copilot(documents, question)
            
            result = (
                f"📚 **Retrieved Code Context** (for Copilot to analyze)\n\n"
                f"{context}\n\n"
                f"---\n"
                f"💡 **Instructions for Copilot:**\n"
                f"Please analyze the above code snippets to answer: \"{question}\"\n"
                f"Provide a clear, technical answer referencing specific files and code."
            )
        
        return [types.TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"Error querying RAG: {e}")
        return [types.TextContent(
            type="text",
            text=f"❌ Error querying codebase: {str(e)}"
        )]


async def handle_rag_list_indexes(arguments: dict) -> List[types.TextContent]:
    """List available RAG indexes"""
    if not _initialize_rag_components():
        return [types.TextContent(
            type="text",
            text="❌ RAG not available."
        )]
    
    try:
        storage_dir = _vector_store_manager.storage_dir
        
        if not os.path.exists(storage_dir):
            return [types.TextContent(
                type="text",
                text=f"📂 No indexes found in: {storage_dir}"
            )]
        
        indexes = [d for d in os.listdir(storage_dir) if d.endswith('.faiss')]
        
        if not indexes:
            return [types.TextContent(
                type="text",
                text=f"📂 No indexes found. Create one with 'rag_index_codebase'."
            )]
        
        result = "## 📚 Available RAG Indexes\n\n"
        for idx in indexes:
            index_name = idx.replace('.faiss', '')
            result += f"- `{index_name}`\n"
        
        return [types.TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"Error listing indexes: {e}")
        return [types.TextContent(
            type="text",
            text=f"❌ Error: {str(e)}"
        )]
