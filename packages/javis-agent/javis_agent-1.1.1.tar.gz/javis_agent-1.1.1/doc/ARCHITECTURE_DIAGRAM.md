```mermaid
graph TB
    subgraph "MCP Client (GitHub Copilot)"
        A[User Query]
    end
    
    subgraph "JAVIS MCP Server"
        B[RAG Handler]
        C[Vector Store Factory]
        
        subgraph "Backends (Plugin Architecture)"
            D1[FAISS Backend]
            D2[LEANN Backend]
        end
        
        E[Code Loader]
        F[RAG Service]
    end
    
    subgraph "Storage"
        G1[FAISS Index<br/>~200MB]
        G2[LEANN Index<br/>~6MB<br/>97% savings!]
    end
    
    A -->|rag_index_codebase| B
    A -->|rag_query_code| B
    
    B -->|Create backend| C
    C -->|backend=faiss| D1
    C -->|backend=leann| D2
    
    E -->|Load & Chunk| D1
    E -->|Load & Chunk| D2
    
    D1 -->|Store| G1
    D2 -->|Store| G2
    
    D1 -->|Search| F
    D2 -->|Search| F
    
    F -->|Results| B
    B -->|Context| A
    
    style D2 fill:#90EE90
    style G2 fill:#90EE90
    style C fill:#FFD700
```

## Key Points:

1. **Factory Pattern**: `VectorStoreFactory` creates the right backend
2. **Plugin Architecture**: Easy to add more backends (ChromaDB, Qdrant, etc.)
3. **Backward Compatible**: FAISS still works, LEANN is optional
4. **Storage Savings**: LEANN uses 97% less storage
5. **Same Interface**: Both backends implement same methods

## Data Flow:

### Indexing:
```
User → RAG Handler → Factory → Backend (FAISS/LEANN) → Storage
                              ↑
                        Code Loader
```

### Querying:
```
User → RAG Handler → Backend → RAG Service → Results → User
```

## Environment Variables:

```bash
RAG_BACKEND=leann     # Choose backend (faiss or leann)
RAG_MODE=retrieval_only  # Choose mode (retrieval_only or full_rag)
```
