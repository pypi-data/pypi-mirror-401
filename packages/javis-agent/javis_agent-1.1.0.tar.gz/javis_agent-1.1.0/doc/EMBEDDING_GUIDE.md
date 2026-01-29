# Embedding Backend Guide

## Tổng quan

Javis RAG hỗ trợ 3 backend embedding:

| Backend | Tốc độ | Chi phí | Privacy | CPU/GPU | Đa ngôn ngữ |
|---------|--------|---------|---------|---------|-------------|
| **sentence_transformers** | ⚡⚡⚡ Fast | ✅ Free | 🔒 100% Local | ✅ CPU tối ưu | ✅ Yes |
| **openai** | ⚡⚡⚡⚡ Very Fast | 💰 Paid | ⚠️ Cloud | ☁️ Cloud | ✅ Yes |
| **huggingface** | ⚡ Slow | ✅ Free | 🔒 100% Local | ⚠️ GPU preferred | Depends |

---

## 1. SentenceTransformers (Khuyến nghị cho CPU)

### Ưu điểm
- ⚡ Tốc độ nhanh trên CPU (10-50ms/text)
- 💰 Hoàn toàn miễn phí
- 🔒 100% local, không gửi data ra ngoài
- 🌍 Hỗ trợ đa ngôn ngữ tốt
- 💾 Model nhẹ (~80MB)

### Cấu hình trong mcp.json
```json
"embedding_backend": "sentence_transformers",
"embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
```

### Các model khuyến nghị

#### Đa ngôn ngữ (multilingual)
- `paraphrase-multilingual-MiniLM-L12-v2` (default, tối ưu nhất)
- `paraphrase-multilingual-mpnet-base-v2` (chất lượng cao hơn, chậm hơn)

#### Tiếng Anh (English only)
- `all-MiniLM-L6-v2` (nhẹ nhất, nhanh nhất)
- `all-mpnet-base-v2` (chất lượng cao)

#### Code-specific
- `sentence-transformers/multi-qa-MiniLM-L6-cos-v1` (tối ưu cho Q&A)

### Cài đặt
```bash
pip install sentence-transformers
```

---

## 2. OpenAI Embeddings (Khuyến nghị cho production)

### Ưu điểm
- ⚡⚡⚡⚡ Rất nhanh (cloud infrastructure)
- 🎯 Chất lượng embedding rất tốt
- ☁️ Không tốn tài nguyên máy local

### Nhược điểm
- 💰 Tốn phí (~$0.0001 per 1K tokens)
- ⚠️ Cần internet
- 🔓 Data gửi lên OpenAI (privacy concerns)

### Cấu hình trong mcp.json
```json
"embedding_backend": "openai",
"embedding_model": "text-embedding-3-small",
"openai_api_key": "${input:openai_key}"
```

### Các model khuyến nghị
- `text-embedding-3-small` (tốt nhất về giá/hiệu suất)
- `text-embedding-3-large` (chất lượng cao nhất, đắt hơn)
- `text-embedding-ada-002` (legacy, vẫn tốt)

### Cài đặt
```bash
pip install openai
```

Và thêm `OPENAI_API_KEY` vào `.env`:
```bash
OPENAI_API_KEY=sk-...
```

---

## 3. HuggingFace Embeddings (Không khuyến nghị cho CPU)

### Ưu điểm
- 💰 Miễn phí
- 🔒 100% local
- 🎨 Nhiều model lựa chọn

### Nhược điểm
- ⚠️ Rất chậm trên CPU
- 💾 Model lớn, tốn RAM
- ⚡ Cần GPU để đạt tốc độ tốt

### Cấu hình trong mcp.json
```json
"embedding_backend": "huggingface",
"embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
```

### Cài đặt
```bash
pip install transformers sentence-transformers
```

---

## So sánh hiệu suất trên CPU

### Test case: Embed 1000 dòng code (avg 100 chars/line)

| Backend | Thời gian | RAM | Chi phí |
|---------|-----------|-----|---------|
| sentence_transformers | ~30s | 500MB | $0 |
| openai | ~5s | 50MB | ~$0.01 |
| huggingface | ~5min | 2GB | $0 |

---

## Khuyến nghị theo use case

### 1. Development/Testing (máy local, CPU)
```json
"embedding_backend": "sentence_transformers",
"embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
```
✅ Nhanh, free, local

### 2. Production (server, cần tốc độ cao)
```json
"embedding_backend": "openai",
"embedding_model": "text-embedding-3-small"
```
✅ Rất nhanh, chất lượng cao

### 3. Privacy-critical (không được gửi data ra ngoài)
```json
"embedding_backend": "sentence_transformers",
"embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
```
✅ 100% local, secure

### 4. Multilingual (Việt/Anh/Hàn/...)
```json
"embedding_backend": "sentence_transformers",
"embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
```
✅ Hỗ trợ 50+ ngôn ngữ

---

## Tối ưu hóa

### 1. Batch embedding (nhanh hơn)
Code đã tự động batch khi embed nhiều documents.

### 2. Cache embeddings
Vector store (FAISS) tự động lưu embeddings, chỉ cần embed 1 lần.

### 3. Adaptive chunking
Code tự động điều chỉnh chunk size dựa trên file size.

---

## Troubleshooting

### Lỗi: "ImportError: No module named 'sentence_transformers'"
```bash
pip install sentence-transformers
```

### Lỗi: "OpenAI API key not found"
Thêm vào `.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
```

### Embedding chậm trên CPU
- Dùng `sentence_transformers` thay vì `huggingface`
- Giảm `chunk_size` trong `code_loader.py`
- Cân nhắc dùng OpenAI API

---

## Example: Switch embedding backend

### Từ OpenAI sang SentenceTransformers
```json
// Before
"embedding_backend": "openai",
"embedding_model": "text-embedding-3-small",

// After
"embedding_backend": "sentence_transformers",
"embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",
```

**Lưu ý:** Phải re-index lại codebase (các embedding cũ không tương thích).

---

## Summary

**Khuyến nghị cho bạn (máy CPU):**
```json
"embedding_backend": "sentence_transformers",
"embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",
"vector_backend": "faiss",
"rag_mode": "retrieval_only"
```

✅ Tốc độ tốt trên CPU  
✅ Miễn phí  
✅ 100% local  
✅ Đa ngôn ngữ
