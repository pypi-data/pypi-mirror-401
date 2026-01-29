# 📚 Hướng dẫn Citation trong RAG

## Tổng quan

Hệ thống RAG đã được nâng cấp để cung cấp **citation (trích dẫn)** chi tiết cho mọi câu trả lời, giúp bạn dễ dàng tra cứu nguồn gốc thông tin.

---

## Các cải tiến

### 1. **Metadata được mở rộng**

Mỗi chunk (đoạn text) trong RAG giờ đây chứa thông tin chi tiết:

```python
{
    'source': '/path/to/file.pdf',           # Đường dẫn file gốc
    'relative_path': 'docs/file.pdf',        # Đường dẫn tương đối
    'file_name': 'file.pdf',                 # Tên file
    'file_type': '.pdf',                     # Loại file
    'file_size': 123456,                     # Kích thước nội dung
    
    # Metadata về vị trí
    'chunk_index': 5,                        # Chunk thứ 6 (index bắt đầu từ 0)
    'total_chunks': 20,                      # Tổng số chunks từ file này
    
    # Metadata về page/slide (chỉ cho PDF/PowerPoint)
    'page_number': 3,                        # Trang 3 (PDF)
    'slide_number': 7,                       # Slide 7 (PowerPoint)
    
    # Metadata về section (markdown/docs)
    'section_title': 'Introduction',         # Tiêu đề section
    
    # Metadata gốc về page/slide
    'page_metadata': [                       # Danh sách metadata của các page/slide
        {
            'page_number': 1,
            'page_text_length': 2500,
            'page_start_pos': 0
        },
        ...
    ]
}
```

---

### 2. **Format output có citation**

Khi truy vấn RAG, kết quả sẽ có dạng:

```markdown
# Code Context for: privacy setting la gi

Found 30 relevant code snippets:

## [1] 8B11Z3DAA6500___E.docx

**Source:** docs/requirements/8B11Z3DAA6500___E.docx
**Section:** Privacy Setting (PPP/GDPR)
**Chunk:** 12
**Preview:** In recent years, the handling of personal information has become strict...

```docx
Privacy Setting (PPP/GDPR)

Background / Purpose

In recent years, the handling of personal information has become strict.
...
```

## [2] SPEC_NA_ECALL_v6.pptm

**Source:** specs/SPEC_NA_ECALL_v6.pptm
**Slide:** 11
**Chunk:** 3
**Preview:** 13.7.1.a. Data communications preparation (SRS)...

```pptm
## Slide 11
13.7.1.a. Data communications preparation (SRS)
TCU shall transition to A-eCall data creation process.
```
```

---

### 3. **Cách sử dụng**

#### a. **Truy vấn RAG như bình thường**

```python
from javis.rag.rag_handler import index_codebase, query_code

# Index tài liệu
index_codebase(dir="/path/to/docs")

# Query với citation
result = query_code(question="privacy setting la gi", top_k=30)
```

#### b. **Kết quả trả về**

Kết quả sẽ bao gồm:
- Tên file nguồn
- Số trang/slide (nếu có)
- Tiêu đề section (nếu phát hiện được)
- Chunk index
- Preview 100 ký tự đầu

#### c. **Tham chiếu chính xác**

Bạn có thể dễ dàng tham chiếu:
- "Theo file `8B11Z3DAA6500___E.docx`, section 'Privacy Setting (PPP/GDPR)', chunk 12..."
- "Dựa vào slide 11 của `SPEC_NA_ECALL_v6.pptm`..."
- "Trích từ trang 3 của `requirements.pdf`..."

---

## So sánh trước và sau

### Trước khi nâng cấp

```markdown
## [1] 8B11Z3DAA6500___E.docx

```docx
Privacy Setting (PPP/GDPR)
In recent years, the handling of personal information...
```
```

❌ Không biết đoạn này ở đâu trong file  
❌ Không biết đây là chunk thứ mấy  
❌ Khó tra cứu lại file gốc

### Sau khi nâng cấp

```markdown
## [1] 8B11Z3DAA6500___E.docx

**Source:** docs/requirements/8B11Z3DAA6500___E.docx
**Section:** Privacy Setting (PPP/GDPR)
**Chunk:** 12
**Preview:** In recent years, the handling of personal information...

```docx
Privacy Setting (PPP/GDPR)
In recent years, the handling of personal information...
```
```

✅ Biết rõ vị trí trong file  
✅ Biết đây là chunk thứ 12  
✅ Dễ dàng tra cứu lại file gốc  
✅ Có preview để xác nhận nhanh

---

## Lợi ích

### 1. **Tăng độ tin cậy**
- Mọi thông tin đều có nguồn gốc rõ ràng
- Dễ dàng kiểm chứng lại

### 2. **Tiết kiệm thời gian**
- Không cần đọc lại toàn bộ file
- Biết chính xác vị trí cần tìm

### 3. **Tuân thủ quy trình**
- Đáp ứng yêu cầu trích dẫn nguồn trong báo cáo kỹ thuật
- Phù hợp với quy trình review code/tài liệu

### 4. **Hỗ trợ debug**
- Nếu RAG trả lời sai, dễ dàng tìm ra nguyên nhân
- Kiểm tra xem chunk nào gây nhiễu

---

## Ví dụ thực tế

### Query: "Data Sharing Setting (DSS) la gi"

**Kết quả:**

```markdown
## [1] 8B11Z3DAA6500___E.docx

**Source:** requirements/8B11Z3DAA6500___E.docx
**Section:** Data Sharing Setting (DSS)
**Chunk:** 5
**Preview:** Data Sharing Setting (DSS) consists of the following two items...

```docx
Configuration

Data Sharing Setting (DSS)

Data Sharing Setting (DSS) consists of the following two items.

(1) Data Sharing Settings for All (DSSA)
(2) Data Sharing Settings for individual Service (DSSS)

DSSA is a batch data input of data upload. When it is turned OFF...
```

## [2] 8B11Z3DAA6500___E.docx

**Source:** requirements/8B11Z3DAA6500___E.docx
**Section:** Service ID and Function ID
**Chunk:** 8
**Preview:** This function uses the following IDs. TSU control Privacy Setting...

```docx
Service ID and Function ID

This function uses the following IDs.

TSU control Privacy Setting by associating these ID with the DSS setting.
...
```
```

**Trả lời:**

"Dựa vào file `8B11Z3DAA6500___E.docx`, section 'Data Sharing Setting (DSS)', chunk 5:

DSS là cơ chế kiểm soát upload dữ liệu, gồm:
- DSSA (Data Sharing Settings for All): Bật/tắt toàn bộ
- DSSS (Data Sharing Settings for individual Service): Bật/tắt từng dịch vụ

Khi DSSA OFF, tất cả dịch vụ bị dừng upload dữ liệu."

---

## Các file được hỗ trợ

- ✅ **PDF**: Có metadata về số trang
- ✅ **PowerPoint (.pptx, .pptm)**: Có metadata về số slide
- ✅ **DOCX**: Có metadata về section title (nếu phát hiện được)
- ✅ **Markdown (.md)**: Có metadata về header (# Header)
- ✅ **Code files**: Có metadata về chunk index
- ✅ **Excel**: Có metadata về sheet name (nếu cần)

---

## Tối ưu hóa

### 1. **Giảm số chunks trả về nếu không cần**

```python
# Chỉ lấy top 10 thay vì 30
result = query_code(question="...", top_k=10)
```

### 2. **Filter theo file type**

```python
# Chỉ index PDF
loader = CodeLoader(extensions=('.pdf',))
```

### 3. **Tăng chunk_size để giảm số chunks**

```python
# Chunk lớn hơn -> ít chunks hơn -> citation ít hơn
loader = CodeLoader(chunk_size=2000, chunk_overlap=400)
```

---

## Troubleshooting

### 1. **Không thấy metadata về page/slide**

- Kiểm tra xem file có phải PDF/PowerPoint không
- Kiểm tra xem PyMuPDF/python-pptx đã được cài chưa

### 2. **Section title không chính xác**

- Hiện tại chỉ phát hiện markdown headers (# Header)
- Nếu file không có header rõ ràng, section_title sẽ không có

### 3. **Preview quá ngắn**

- Preview mặc định là 100 ký tự
- Có thể sửa trong `rag_service.py`:

```python
content_preview = doc.page_content[:200]  # Tăng lên 200
```

---

## Kết luận

Với tính năng citation mới, bạn có thể:
- ✅ Trả lời câu hỏi với bằng chứng rõ ràng
- ✅ Tham chiếu chính xác nguồn gốc thông tin
- ✅ Tiết kiệm thời gian tra cứu lại tài liệu
- ✅ Tăng độ tin cậy cho câu trả lời

Hãy sử dụng và trải nghiệm! 🚀
