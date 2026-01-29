"""
Prompt handlers for MCP server operations
Xử lý các MCP prompts cho phân tích code
"""
import os
from typing import Dict
from mcp import types
from javis.prompts.prompt_templates import PromptTemplates

from javis.modules.config import get_src_dir, setup_logging

logger = setup_logging()

class PromptHandler:
    """Handler cho các MCP prompts"""
    
    def __init__(self):
        self.templates = PromptTemplates()
    
   

    async def handle_prompt(self, name: str, arguments: Dict[str, str] = None) -> types.GetPromptResult:
        """
        Route và xử lý prompt calls
        
        Args:
            name: Tên prompt
            arguments: Arguments cho prompt
            
        Returns:
            GetPromptResult
        """
        logger.info(f"Prompt called: {name} with arguments: {arguments}")
        
        try:            
            if name == "get_code_context":
                return await self._handle_code_context()  
            elif name == "check_design":
                return await self._handle_design_check(arguments)
            elif name == "check_single_requirement":
                return await self._handle_single_requirement(arguments)
            else:
                raise ValueError(f"Unknown prompt: {name}")
                
        except Exception as e:
            logger.exception(f"Error in prompt handler for {name}: {e}")
            raise
    
    async def _handle_single_requirement(self, arguments: Dict[str, str] = None) -> types.GetPromptResult:
        """
        Build prompt to verify single user-provided requirement implementation.
        Expects: arguments = {"requirement_text": "..."}
        """
        prompt_lang = os.environ.get("prompt_lang", "en")
        requirement_text = ""
        if arguments and isinstance(arguments, dict):
            requirement_text = arguments.get("requirement_text", "")

        if prompt_lang == "vi":
            prompt = PromptTemplates.get_single_requirement_verification_prompt_vi(requirement_text)
        else:
            prompt = PromptTemplates.get_single_requirement_verification_prompt(requirement_text)

        messages = [
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt),
            )
        ]
        return types.GetPromptResult(
            messages=messages,
            description="Prompt to verify implementation of a single requirement.",
        )
    
        
    async def _handle_design_check(self, arguments=None) -> types.GetPromptResult:
        import os
        from javis.modules.config import get_src_dir, get_req_dir, get_api_base_dirs, get_module_api, get_framework_dir, get_report_dir
        
        prompt_lang = os.environ.get("prompt_lang", "en")
        
        # Lấy tham số feature từ arguments dict
        feature = None
        if arguments and isinstance(arguments, dict) and "feature" in arguments:
            feature = arguments["feature"]
        
        logger.info(f"[check_design] Feature argument: {feature}")
        
        if prompt_lang == "vi":
            # Prompt tiếng Việt đầy đủ
            prompt = (
                "Bạn là chuyên gia phân tích thiết kế hệ thống nhúng ô tô.\n"
                "Nhiệm vụ của bạn: Đánh giá sơ đồ trình tự (sequence diagram) trong thiết kế đính kèm (file hình ảnh) về mức độ đáp ứng yêu cầu"
            )
            
            # Thêm feature nếu có
            if feature:
                prompt += f" cho feature {feature}"
            
            prompt += ", xác thực API, và độ robust.\n"
            
            # Tiếp tục với phần còn lại
            prompt += (
                "\n\n**QUY TRÌNH PHÂN TÍCH:**\n"
                f"1. Phân tích kỹ yêu cầu về feature"
            )
            
            if feature:
                prompt += f" {feature}"
            
            prompt += (
                " trong tài liệu requirement (file markdown đính kèm).\n"
                "2. Trích xuất đầy đủ các thành phần, API call, và luồng tương tác từ sequence diagram.\n"
                "3. Đối chiếu từng API call với ngữ cảnh ứng dụng, interface để xác thực tính hợp lệ.\n"
                "4. So sánh từng bước thiết kế với yêu cầu, kiểm tra điểm thiếu/phủ sóng hoặc chưa rõ ràng. Đặc biệt, cần phân tích kỹ các trường hợp lỗi (error case), timeout, và các tình huống bất thường có thể xảy ra trong thực tế.\n"
                "5. Đánh giá chi tiết khả năng xử lý lỗi, chiến lược recovery, logic fallback, và quản lý trạng thái của hệ thống. Nêu rõ các nhánh xử lý lỗi, cơ chế phục hồi, và đảm bảo hệ thống không rơi vào trạng thái bất định.\n"
                "6. Đề xuất cải tiến robust design, bổ sung các bước xử lý lỗi còn thiếu, và xây dựng sơ đồ PlantUML sequence cải tiến với nhánh error/recovery rõ ràng nếu cần.\n\n"
                "## 🔍 Phân tích thiết kế hiện tại\n"
                "### Đánh giá luồng trình tự\n"
                "- Thành phần: [liệt kê]\n"
                "- Luồng thông điệp: [phân tích]\n"
                "- Chuyển trạng thái: [phân tích]\n\n"
                "### Kết quả xác thực API\n"
                "**✅ API hợp lệ:**\n"
                "- `ClassName::method()` - Tìm thấy trong [ngữ cảnh]\n"
                "**❌ API thiếu:**\n"
                "- `UnknownClass::method()` - Không tìm thấy, cần bổ sung\n"
                "**⚠️ API mơ hồ:**\n"
                "- `CommonName::method()` - Tìm thấy ở nhiều ngữ cảnh, cần làm rõ\n\n"
                "### Đáp ứng yêu cầu\n"
                "| Mã yêu cầu | Mô tả | Trạng thái | Ghi chú |\n"
                "|-----------|-------|------------|--------|\n"
                "| REQ-001 | [nội dung] | ✅/❌/⚠️ | [ghi chú] |\n\n"
                "## ❌ Vấn đề nghiêm trọng\n"
                "- Thiếu phủ sóng yêu cầu\n"
                "- API không hợp lệ hoặc thiếu\n"
                "- Thiếu robust (xử lý lỗi, timeout, fallback, trạng thái)\n"
                "## 🚀 Giải pháp thiết kế nâng cao\n"
                "### Chiến lược tích hợp API\n"
                "- Dùng API có sẵn ở mọi ngữ cảnh nếu có thể\n"
                "- Sửa API hiện có nếu cần\n"
                "- Chỉ đề xuất API mới khi thực sự cần thiết, phải giải thích rõ\n\n"
                "### Kế hoạch đáp ứng yêu cầu\n"
                "- Với mỗi yêu cầu thiếu, nêu rõ thay đổi thiết kế cần thực hiện\n\n"
                "### Đề xuất improved design\n"
                "Vui lòng trình bày improved design cho thiết kế hiện tại bằng sequence diagram chuẩn PlantUML.\n"
                "```plantuml\n"
                "@startuml\n"
                "title Enhanced Design\n"
                "' Add enhanced design here\n"
                "' Include error handling and robustness\n"
                "@enduml\n"
                "```\n"
            )
            
            if feature:
                prompt += f" - {feature}"
            
            prompt += (
                "\n\n"
                "' Add enhanced design here\n"
                "' Include error handling and robustness\n"
                "@enduml\n"
                "```\n"
            )
        else:            
            prompt = self.templates.get_design_verification_prompt(feature)

        messages = [
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt),
            )
        ]
        result = types.GetPromptResult(
            messages=messages,
            description="A prompt for design verification and improvement.",
        )
        logger.info("Design verification prompt completed")
        return result
     
    async def _handle_code_context(self) -> types.GetPromptResult:
        """Handle code context prompt (load and summarize all files in src_dir)"""
        import os
        prompt_lang = os.environ.get("prompt_lang", "en")
        if prompt_lang == "vi":
            prompt = (
                "Bạn là trợ lý ngữ cảnh mã nguồn. Nhiệm vụ của bạn là đọc và ghi nhớ toàn bộ nội dung, cấu trúc của tất cả các file mã nguồn (C++, Python, ...) trong thư mục dự án hiện tại.\n"
                "Nếu nội dung file chưa được tải, hãy gọi tool 'get_src_context' từ MCP server để lấy tất cả file mã nguồn trong thư mục SRC_DIR.\n"
                "Với mỗi file, hãy tóm tắt:\n"
                "- Tên file và đường dẫn tương đối\n"
                "- Tất cả class, struct, enum, function (C++, Python, ...)\n"
                "- Quan hệ kế thừa, sử dụng, thành phần\n"
                "- Biến toàn cục, hằng số, macro, cấu hình\n"
                "- Các chú thích hoặc tài liệu quan trọng\n"
                "Không thực hiện phân tích tĩnh hoặc kiểm tra rule ở bước này.\n"
                "Lưu ngữ cảnh này để dùng cho các truy vấn tiếp theo.\n\n"
                "**ĐỊNH DẠNG KẾT QUẢ:**\n"
                "Với mỗi file:\n"
                "### [Tên file]\n"
                "```[ngôn ngữ]\n[Tóm tắt cấu trúc, định nghĩa, điểm chính]\n```\n"
                "Lặp lại cho tất cả file.\n"
                "Xác nhận khi đã nạp đủ ngữ cảnh."
            )
        else:
            prompt = self.templates.get_context_prompt()
        messages = [
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt),
            )
        ]
        result = types.GetPromptResult(
            messages=messages,
            description="A prompt for loading and summarizing code context for all C++ files.",
        )
        logger.info("Code context prompt completed")
        return result