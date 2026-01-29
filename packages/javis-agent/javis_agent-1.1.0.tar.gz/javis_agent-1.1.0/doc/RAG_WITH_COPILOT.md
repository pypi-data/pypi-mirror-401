# Sử dụng RAG với GitHub Copilot Chat

## Tổng quan

RAG trong MCP server này hoạt động như sau:
1. **MCP Server** (javis): Tìm kiếm code liên quan (retrieval only)
2. **Copilot Chat**: Nhận context và trả lời câu hỏi (generation)

Bạn **KHÔNG CẦN** OpenAI API key cho generation. Copilot đã lo phần này!

## Workflow

```
User: "How does authentication work?"
  ↓
Copilot Chat → MCP Server (javis): rag_query_code
  ↓
MCP Server: Search vector DB → Return code context
  ↓
Copilot Chat: Receive context → Generate answer using GPT-4
  ↓
User: See answer in Copilot Chat window
```

## Setup (Chỉ cần 1 lần)

### 1. Cài dependencies
```bash
pip install -r requirements-rag.txt
```

### 2. Set OpenAI API key (CHỈ CHO EMBEDDINGS)
```bash
export OPENAI_API_KEY="sk-..."
```

**Quan trọng**: API key này CHỈ dùng để tạo embeddings khi index code. Không dùng cho generation!

Cost: ~$0.02 per 1 million tokens (rất rẻ)

### 3. Index codebase
```bash
# Trong Copilot Chat
@javis /rag_index_codebase {"dir": "/path/to/code"}
```

## Sử dụng

### Hỏi câu hỏi
```bash
# Trong Copilot Chat window
@javis /rag_query_code {"question": "How does the login system work?"}
```

**Kết quả:**
1. MCP server tìm code liên quan
2. Return code context về Copilot
3. **Copilot (GPT-4) đọc context và trả lời bạn**
4. Bạn thấy answer ngay trong chat

## Ví dụ đầy đủ

```bash
# 1. Cài đặt
cd /path/to/javis_agent
pip install -r requirements-rag.txt

# 2. Set API key (chỉ cho embeddings)
export OPENAI_API_KEY="sk-..."

# 3. Trong VS Code Copilot Chat:
@javis /rag_index_codebase {"dir": "/workspace/myproject"}

# 4. Hỏi câu hỏi
@javis /rag_query_code {"question": "How is user authentication implemented?"}

# Copilot sẽ nhận code context và trả lời bạn!
```

## Lợi ích

✅ **Không tốn tiền generation** - Copilot đã trả $10-19/tháng
✅ **GPT-4 quality** - Copilot dùng GPT-4, không phải GPT-3.5
✅ **Tích hợp tự nhiên** - Chat trực tiếp trong VS Code
✅ **Bảo mật** - Code context được Copilot xử lý, không ra ngoài
✅ **Embeddings rẻ** - Chỉ $0.02/1M tokens cho việc index

## Troubleshooting

### "OpenAI API key not found" khi index
Bạn vẫn cần API key để tạo embeddings:
```bash
export OPENAI_API_KEY="sk-..."
```

### Context quá dài
Giảm `top_k`:
```bash
@javis /rag_query_code {"question": "...", "top_k": 3}
```

### Kết quả không chính xác
- Re-index code nếu đã thay đổi nhiều
- Tăng `top_k` để có nhiều context hơn
- Hỏi câu hỏi cụ thể hơn

## Chi tiết kỹ thuật

### Phân chia công việc:

| Task | Who handles | Cost |
|------|-------------|------|
| Index code (embeddings) | OpenAI API | ~$0.02/1M tokens |
| Store vectors | FAISS (local) | Free |
| Search vectors | MCP Server | Free |
| Generate answer | **Copilot Chat (GPT-4)** | **Free** (đã trả subscription) |

### Flow chi tiết:

```
[User] "How does login work?"
  ↓
[Copilot Chat] Call MCP tool: rag_query_code
  ↓
[MCP Server javis]
  1. Search FAISS vector DB
  2. Find top 5 relevant code snippets
  3. Format as markdown context
  4. Return to Copilot
  ↓
[Copilot Chat]
  1. Receive code context
  2. Use GPT-4 to analyze
  3. Generate answer
  4. Show to user
  ↓
[User] See answer in chat window
```

## So sánh với approach khác

### ❌ Approach cũ (tốn tiền):
```
MCP Server → OpenAI API (GPT-4) → Answer
Cost: $0.03/1K tokens input + $0.06/1K tokens output
```

### ✅ Approach mới (free generation):
```
MCP Server → Return context → Copilot (GPT-4) → Answer
Cost: $0 (Copilot đã trả phí)
```

Chỉ tốn tiền cho embeddings khi index (~$0.02/1M tokens)
