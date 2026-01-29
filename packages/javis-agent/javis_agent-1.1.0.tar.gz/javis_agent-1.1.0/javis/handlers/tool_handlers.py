"""
Tool handlers for MCP server operations
Xử lý các MCP tools (fetch rules, analyze files, etc.)
"""
import os
import glob
from typing import List, Union, Dict
from mcp import types
from mcp.types import TextContent

from javis.modules.rule_fetcher import (
    fetch_custom_rule
)
from javis.modules.file_utils import list_source_files


from javis.modules.config import setup_logging, get_src_dir
from javis.modules.persistent_storage import PersistentTracker
from javis.handlers.requirement_handler import handle_requirement_analysis
from javis.handlers.interface_handler import get_interface
from javis.handlers.rag_handler import (
    handle_rag_index_codebase,
    handle_rag_query_code,
    handle_rag_list_indexes
)

import pprint
from datetime import datetime

logger = setup_logging()

import platform
import json
import sys
import subprocess


def get_lgedv_cache_dir():
    if platform.system().lower().startswith("win"):
        return r"C:\Program Files\MCP Server CodeGuard\tmp\lgedv"
    else:
        return "/tmp/lgedv"

  
class ToolHandler:
    """Handler cho các MCP tools"""

    def __init__(self):
        self.memory_tracker = PersistentTracker(analysis_type="memory_analysis")
        
    async def handle_tool_call(self, name: str, arguments: dict) -> List[Union[
        types.TextContent, types.ImageContent, types.AudioContent, types.EmbeddedResource
    ]]:
        """
        Route và xử lý tool calls
        
        Args:
            name: Tên tool
            arguments: Arguments cho tool
            
        Returns:
            List content response
        """
        logger.info("=== handle_tool_call ENTERED ===")
        logger.info(f"Tool called: {name} with arguments: {arguments}")
        
        try:
            if name == "fetch_custom_rule":
                return await self._handle_fetch_custom_rule(arguments)
            # File operations
            elif name == "list_source_files":
                return await self._handle_list_source_files(arguments)
            elif name == "get_src_context":
                logger.info(f"get_src_context called with arguments: {arguments}")
                return await self._handle_get_src_context(arguments)
            elif name == "analyze_requirement":
                return await self._handle_analyze_requirement(arguments)
            elif name == "get_interface":
                return await self._handle_get_interface(arguments)
            # RAG tools
            elif name == "rag_index_codebase":
                return await handle_rag_index_codebase(arguments)
            elif name == "rag_query_code":
                return await handle_rag_query_code(arguments)
            elif name == "rag_list_indexes":
                return await handle_rag_list_indexes(arguments)
            else:
                logger.error(f"Unknown tool: {name}")
                raise ValueError(f"Unknown tool: {name}")
            
                
        except Exception as e:
            logger.exception(f"Error in tool handler for {name}: {e}")
            raise
    
    
    async def _handle_get_interface(self, arguments: dict):
        """
        Handle get interface tool call
        Nếu không có arguments hoặc không có 'dir', lấy từ module_api trong config
        """
        # Import config function để lấy module_api
        from javis.modules.config import get_module_api
        
        # Kiểm tra và lấy dir_path
        if not arguments or 'dir' not in arguments or not arguments.get('dir'):
            # Lấy từ module_api trong mcp.json
            dir_path = get_module_api()
            logger.info(f"[get_interface] No dir parameter provided, using module_api from config: {dir_path}")
        else:
            # Sử dụng dir từ arguments
            dir_path = arguments.get("dir")
            logger.info(f"[get_interface] Using dir from arguments: {dir_path}")
        
        # Kiểm tra dir_path có hợp lệ không
        if not dir_path:
            error_msg = "❌ Lỗi: Không có thư mục nào được chỉ định và không có module_api trong config"
            logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]
        
        # Gọi hàm get_interface với dir_path
        try:
            result = get_interface(dir_path)
            logger.info(f"[get_interface] Successfully analyzed interface in: {dir_path}")
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        except Exception as e:
            error_msg = f"❌ Lỗi khi phân tích interface: {str(e)}"
            logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]

    
    async def _handle_fetch_custom_rule(self, arguments: dict) -> List[types.TextContent]:
        """Handle fetch_custom_rule tool"""
        url = arguments.get("url")
        result = await fetch_custom_rule(url)
        logger.info(f"fetch_custom_rule completed for url: {url}")
        return result
    
    async def _handle_list_source_files(self, arguments: dict) -> List[types.TextContent]:
        """Handle list_source_files tool"""
        dir_path = get_src_dir()
        files = list_source_files(dir_path)
        logger.info(f"list_source_files found {len(files)} files")
        return [types.TextContent(type="text", text="\n".join(files))]

    
    
    async def _handle_get_src_context(self, arguments: dict) -> List[types.TextContent]:
        """
        Lấy toàn bộ code trong thư mục arguments.get("dir"), bao gồm cả thư mục con.
        Trả về hướng dẫn bằng tiếng Việt nếu prompt_lang=vi, còn lại tiếng Anh.
        """
        import os
        prompt_lang = os.environ.get("prompt_lang", "en")
        if prompt_lang == "vi":
            guide = (
                "Bạn là trợ lý ngữ cảnh mã nguồn. Nhiệm vụ của bạn là đọc và ghi nhớ toàn bộ nội dung, cấu trúc của tất cả các file mã nguồn (C++, Python, ...) trong thư mục chỉ định.\n"
                "Với mỗi file, hãy tóm tắt:\n"
                "- Tên file và đường dẫn tương đối\n"
                "- Liệt kê đầy đủ khai báo class, struct, enum, function (bao gồm tham số, kế thừa nếu có)\n"
                "- Trích xuất các docstring hoặc chú thích đầu class/function\n"
                "- Liệt kê biến toàn cục, hằng số, macro, cấu hình (kèm giá trị nếu có)\n"
                "- Tóm tắt các chú thích quan trọng hoặc tài liệu đầu file\n"
                "- Không thực hiện phân tích tĩnh hoặc kiểm tra rule ở bước này\n"
                "- Lưu ngữ cảnh này để dùng cho các truy vấn tiếp theo\n"
                "Hãy tóm tắt code context bằng tiếng Việt, trình bày rõ ràng từng mục.\n\n"
            )
        else:
            guide = (
                "You are a code context assistant. Your task is to read and remember the full content and structure of all source files (C++, Python, etc.) in the specified directory.\n"
                "For each file, extract and summarize:\n"
                "- File name and relative path\n"
                "- List full declarations of all classes, structs, enums, and functions (including parameters and inheritance)\n"
                "- Extract any docstrings or leading comments for each class/function\n"
                "- List all global variables, constants, macros, and configuration (with values if possible)\n"
                "- Summarize important block comments or documentation at the top of the file\n"
                "- Do not perform static analysis or rule checking in this step\n"
                "- Store this context for use in subsequent analysis or code-related queries\n"
                "Summarize code context in clear English, with each item presented explicitly.\n\n"
            )

        dir_path = arguments.get("dir")
        base_path = get_src_dir()
        logger.info(f"[get_context] Walking directory: {base_path}")

        # Xác định đường dẫn tuyệt đối
        if not dir_path:
            abs_path = base_path
        elif os.path.isabs(dir_path):
            abs_path = dir_path
        else:
            if "/" not in dir_path and "\\" not in dir_path:
                matches = []
                for root, dirs, files in os.walk(base_path):
                    for d in dirs:
                        if d == dir_path:
                            matches.append(os.path.join(root, d))
                if len(matches) == 1:
                    abs_path = matches[0]
                elif len(matches) == 0:
                    logger.error(f"Directory '{dir_path}' not found in {base_path}")
                    raise ValueError(f"Directory '{dir_path}' not found in {base_path}")
                else:
                    logger.error(f"Found multiple directories named '{dir_path}':\n" + "\n".join(matches))
                    raise ValueError(f"Found multiple directories named '{dir_path}':\n" + "\n".join(matches))
            else:
                abs_path = os.path.join(base_path, dir_path)

        # Kiểm tra tồn tại và là thư mục
        if not abs_path or not os.path.exists(abs_path):
            logger.error(f"Directory '{abs_path}' does not exist.")
            raise ValueError(f"Directory '{abs_path}' does not exist.")
        if not os.path.isdir(abs_path):
            logger.error(f"Path '{abs_path}' is not a directory.")
            raise ValueError(f"Path '{abs_path}' is not a directory.")

        logger.info(f"[get_context] Walking directory: {abs_path}")
        code_contents = []
        SRC_EXTENSIONS = ('.cpp', '.h', '.hpp', '.cc', '.cxx', '.py', '.java', '.js', '.jsx', '.ts')
        found_code_file = False
        for root, dirs, files in os.walk(abs_path):
            logger.info(f"[get_context] Current dir: {root}")
            logger.info(f"[get_context] Files in dir: {files}")
            for file in files:
                logger.info(f"[get_context] Checking file: {file}")
                if file.endswith(SRC_EXTENSIONS):
                    found_code_file = True
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, abs_path)
                    logger.info(f"[get_context] Found code file: {file_path} (rel: {rel_path})")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code_contents.append(f"// File: {rel_path}\n" + f.read())
                    except Exception as e:
                        logger.error(f"Error reading file {file_path}: {e}")
                        code_contents.append(f"// File: {rel_path}\n// Error reading file: {e}\n")

        if not found_code_file:
            logger.warning(f"No code files found in directory '{abs_path}'.")
            return [types.TextContent(type="text", text=f"// No code files found in directory '{abs_path}'.")]

        content = "\n\n".join(code_contents)
        return [types.TextContent(type="text", text=guide + content)]
