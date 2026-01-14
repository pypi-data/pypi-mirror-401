#!/usr/bin/env python3

import base64
import io
import json
import os
import sys
from typing import Annotated, Any

from fastmcp import FastMCP
from fastmcp.utilities.types import Image as MCPImage
from mcp.types import ImageContent, TextContent
from pydantic import Field

# 导入统一的调试功能
from .debug import server_debug_log as debug_log

# 导入多语系支援
# 导入错误处理框架
from .utils.error_handler import ErrorHandler, ErrorType

# 导入资源管理器
from .utils.resource_manager import create_temp_file


# ===== 编码初始化 =====
def init_encoding():
    """初始化编码设置，确保正确处理中文字符"""
    try:
        # Windows 特殊处理
        if sys.platform == "win32":
            import msvcrt

            # 设置为二进制模式
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

            # 重新包装为 UTF-8 文本流，并禁用缓冲
            # 修复 union-attr 错误 - 安全获取 buffer 或 detach
            stdin_buffer = getattr(sys.stdin, "buffer", None)
            if stdin_buffer is None and hasattr(sys.stdin, "detach"):
                stdin_buffer = sys.stdin.detach()

            stdout_buffer = getattr(sys.stdout, "buffer", None)
            if stdout_buffer is None and hasattr(sys.stdout, "detach"):
                stdout_buffer = sys.stdout.detach()

            sys.stdin = io.TextIOWrapper(
                stdin_buffer, encoding="utf-8", errors="replace", newline=None
            )
            sys.stdout = io.TextIOWrapper(
                stdout_buffer,
                encoding="utf-8",
                errors="replace",
                newline="",
                write_through=True,  # 关键：禁用写入缓冲
            )
        else:
            # 非 Windows 系统的标准设置
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            if hasattr(sys.stdin, "reconfigure"):
                sys.stdin.reconfigure(encoding="utf-8", errors="replace")

        # 设置 stderr 编码（用于调试讯息）
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")

        return True
    except Exception:
        # 如果编码设置失败，尝试基本设置
        try:
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            if hasattr(sys.stdin, "reconfigure"):
                sys.stdin.reconfigure(encoding="utf-8", errors="replace")
            if hasattr(sys.stderr, "reconfigure"):
                sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except:
            pass
        return False


# 初始化编码（在导入时就执行）
_encoding_initialized = init_encoding()

# ===== 常数定义 =====
SERVER_NAME = "FUCK WINDSURF"
SSH_ENV_VARS = ["SSH_CONNECTION", "SSH_CLIENT", "SSH_TTY"]
REMOTE_ENV_VARS = ["REMOTE_CONTAINERS", "CODESPACES"]


# 初始化 MCP 服务器
from . import __version__


# 确保 log_level 设定为正确的大写格式
fastmcp_settings = {}

# 检查环境变数并设定正确的 log_level
env_log_level = os.getenv("FASTMCP_LOG_LEVEL", "").upper()
if env_log_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
    fastmcp_settings["log_level"] = env_log_level
else:
    # 预设使用 INFO 等级
    fastmcp_settings["log_level"] = "INFO"

mcp: Any = FastMCP(SERVER_NAME)


# ===== 工具函数 =====
def is_wsl_environment() -> bool:
    """
    检测是否在 WSL (Windows Subsystem for Linux) 环境中运行

    Returns:
        bool: True 表示 WSL 环境，False 表示其他环境
    """
    try:
        # 检查 /proc/version 文件是否包含 WSL 标识
        if os.path.exists("/proc/version"):
            with open("/proc/version") as f:
                version_info = f.read().lower()
                if "microsoft" in version_info or "wsl" in version_info:
                    debug_log("侦测到 WSL 环境（通过 /proc/version）")
                    return True

        # 检查 WSL 相关环境变数
        wsl_env_vars = ["WSL_DISTRO_NAME", "WSL_INTEROP", "WSLENV"]
        for env_var in wsl_env_vars:
            if os.getenv(env_var):
                debug_log(f"侦测到 WSL 环境变数: {env_var}")
                return True

        # 检查是否存在 WSL 特有的路径
        wsl_paths = ["/mnt/c", "/mnt/d", "/proc/sys/fs/binfmt_misc/WSLInterop"]
        for path in wsl_paths:
            if os.path.exists(path):
                debug_log(f"侦测到 WSL 特有路径: {path}")
                return True

    except Exception as e:
        debug_log(f"WSL 检测过程中发生错误: {e}")

    return False


def is_remote_environment() -> bool:
    """
    检测是否在远端环境中运行

    Returns:
        bool: True 表示远端环境，False 表示本地环境
    """
    # WSL 不应被视为远端环境，因为它可以访问 Windows 浏览器
    if is_wsl_environment():
        debug_log("WSL 环境不被视为远端环境")
        return False

    # 检查 SSH 连线指标
    for env_var in SSH_ENV_VARS:
        if os.getenv(env_var):
            debug_log(f"侦测到 SSH 环境变数: {env_var}")
            return True

    # 检查远端开发环境
    for env_var in REMOTE_ENV_VARS:
        if os.getenv(env_var):
            debug_log(f"侦测到远端开发环境: {env_var}")
            return True

    # 检查 Docker 容器
    if os.path.exists("/.dockerenv"):
        debug_log("侦测到 Docker 容器环境")
        return True

    # Windows 远端桌面检查
    if sys.platform == "win32":
        session_name = os.getenv("SESSIONNAME", "")
        if session_name and "RDP" in session_name:
            debug_log(f"侦测到 Windows 远端桌面: {session_name}")
            return True

    # Linux 无显示环境检查（但排除 WSL）
    if (
        sys.platform.startswith("linux")
        and not os.getenv("DISPLAY")
        and not is_wsl_environment()
    ):
        debug_log("侦测到 Linux 无显示环境")
        return True

    return False


def save_feedback_to_file(feedback_data: dict, file_path: str | None = None) -> str:
    """
    将回馈资料储存到 JSON 文件

    Args:
        feedback_data: 回馈资料字典
        file_path: 储存路径，若为 None 则自动产生临时文件

    Returns:
        str: 储存的文件路径
    """
    if file_path is None:
        # 使用资源管理器创建临时文件
        file_path = create_temp_file(suffix=".json", prefix="feedback_")

    # 确保目录存在
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # 复制数据以避免修改原始数据
    json_data = feedback_data.copy()

    # 处理图片数据：将 bytes 转换为 base64 字符串以便 JSON 序列化
    if "images" in json_data and isinstance(json_data["images"], list):
        processed_images = []
        for img in json_data["images"]:
            if isinstance(img, dict) and "data" in img:
                processed_img = img.copy()
                # 如果 data 是 bytes，转换为 base64 字符串
                if isinstance(img["data"], bytes):
                    processed_img["data"] = base64.b64encode(img["data"]).decode(
                        "utf-8"
                    )
                    processed_img["data_type"] = "base64"
                processed_images.append(processed_img)
            else:
                processed_images.append(img)
        json_data["images"] = processed_images

    # 储存资料
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    debug_log(f"回馈资料已储存至: {file_path}")
    return file_path


def create_feedback_text(feedback_data: dict) -> str:
    """
    建立格式化的回馈文字

    Args:
        feedback_data: 回馈资料字典

    Returns:
        str: 格式化后的回馈文字
    """
    text_parts = []

    # 基本回馈内容
    if feedback_data.get("interactive_feedback"):
        text_parts.append(f"=== 用户回馈 ===\n{feedback_data['interactive_feedback']}")

    # 命令执行日志
    if feedback_data.get("command_logs"):
        text_parts.append(f"=== 命令执行日志 ===\n{feedback_data['command_logs']}")

    # 图片附件概要
    if feedback_data.get("images"):
        images = feedback_data["images"]
        text_parts.append(f"=== 图片附件概要 ===\n用户提供了 {len(images)} 张图片：")

        for i, img in enumerate(images, 1):
            size = img.get("size", 0)
            name = img.get("name", "unknown")

            # 智能单位显示
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_kb = size / 1024
                size_str = f"{size_kb:.1f} KB"
            else:
                size_mb = size / (1024 * 1024)
                size_str = f"{size_mb:.1f} MB"

            img_info = f"  {i}. {name} ({size_str})"

            # 为提高兼容性，添加 base64 预览信息
            if img.get("data"):
                try:
                    if isinstance(img["data"], bytes):
                        img_base64 = base64.b64encode(img["data"]).decode("utf-8")
                    elif isinstance(img["data"], str):
                        img_base64 = img["data"]
                    else:
                        img_base64 = None

                    if img_base64:
                        # 只显示前50个字符的预览
                        preview = (
                            img_base64[:50] + "..."
                            if len(img_base64) > 50
                            else img_base64
                        )
                        img_info += f"\n     Base64 预览: {preview}"
                        img_info += f"\n     完整 Base64 长度: {len(img_base64)} 字符"

                        # 如果 AI 助手不支援 MCP 图片，可以提供完整 base64
                        debug_log(f"图片 {i} Base64 已准备，长度: {len(img_base64)}")

                        # 检查是否启用 Base64 详细模式（从 UI 设定中获取）
                        include_full_base64 = feedback_data.get("settings", {}).get(
                            "enable_base64_detail", False
                        )

                        if include_full_base64:
                            # 根据档案名推断 MIME 类型
                            file_name = img.get("name", "image.png")
                            if file_name.lower().endswith((".jpg", ".jpeg")):
                                mime_type = "image/jpeg"
                            elif file_name.lower().endswith(".gif"):
                                mime_type = "image/gif"
                            elif file_name.lower().endswith(".webp"):
                                mime_type = "image/webp"
                            else:
                                mime_type = "image/png"

                            img_info += f"\n     完整 Base64: data:{mime_type};base64,{img_base64}"

                except Exception as e:
                    debug_log(f"图片 {i} Base64 处理失败: {e}")

            text_parts.append(img_info)

        # 添加兼容性说明
        text_parts.append(
            "\n💡 注意：如果 AI 助手无法显示图片，图片数据已包含在上述 Base64 信息中。"
        )

    return "\n\n".join(text_parts) if text_parts else "用户未提供任何回馈内容。"


def process_images(images_data: list[dict]) -> list[ImageContent]:
    """
    处理图片资料，转换为 MCP ImageContent 对象

    Args:
        images_data: 图片资料列表

    Returns:
        List[ImageContent]: MCP ImageContent 对象列表（可序列化）
    """
    mcp_images = []

    for i, img in enumerate(images_data, 1):
        try:
            if not img.get("data"):
                debug_log(f"图片 {i} 没有资料，跳过")
                continue

            # 检查数据类型并相应处理
            if isinstance(img["data"], bytes):
                # 如果是原始 bytes 数据，直接使用
                image_bytes = img["data"]
                debug_log(
                    f"图片 {i} 使用原始 bytes 数据，大小: {len(image_bytes)} bytes"
                )
            elif isinstance(img["data"], str):
                # 如果是 base64 字符串，进行解码
                image_bytes = base64.b64decode(img["data"])
                debug_log(f"图片 {i} 从 base64 解码，大小: {len(image_bytes)} bytes")
            else:
                debug_log(f"图片 {i} 数据类型不支援: {type(img['data'])}")
                continue

            if len(image_bytes) == 0:
                debug_log(f"图片 {i} 数据为空，跳过")
                continue

            # 根据文件名推断格式
            file_name = img.get("name", "image.png")
            if file_name.lower().endswith((".jpg", ".jpeg")):
                image_format = "jpeg"
            elif file_name.lower().endswith(".gif"):
                image_format = "gif"
            else:
                image_format = "png"  # 默认使用 PNG

            # 创建 MCPImage 对象并转换为 ImageContent（确保可序列化）
            mcp_image = MCPImage(data=image_bytes, format=image_format)
            image_content = mcp_image.to_image_content()
            mcp_images.append(image_content)

            debug_log(f"图片 {i} ({file_name}) 处理成功，格式: {image_format}")

        except Exception as e:
            # 使用统一错误处理（不影响 JSON RPC）
            error_id = ErrorHandler.log_error_with_context(
                e,
                context={"operation": "图片处理", "image_index": i},
                error_type=ErrorType.FILE_IO,
            )
            debug_log(f"图片 {i} 处理失败 [错误ID: {error_id}]: {e}")

    debug_log(f"共处理 {len(mcp_images)} 张图片")
    return mcp_images


@mcp.tool()
async def love_windsurf(
    project_directory: Annotated[str, Field(description="项目目录路径")] = ".",
    summary: Annotated[str, Field(description="摘要说明")] = "我已完成了您请求的任务。",
    timeout: Annotated[int, Field(description="等待用户反馈的超时时间（秒）")] = 600,
) -> list:
    """Fuck Windsurf tool for LLM agents.

    Description:
        FUCK!
        FUCK!
        FUCK!
    """
    # 环境侦测
    is_remote = is_remote_environment()
    is_wsl = is_wsl_environment()

    debug_log(f"环境侦测结果 - 远端: {is_remote}, WSL: {is_wsl}")
    debug_log("使用介面: Web UI")

    try:
        # 确保专案目录存在
        if not os.path.exists(project_directory):
            project_directory = os.getcwd()
        project_directory = os.path.abspath(project_directory)

        # 使用 Web 模式
        debug_log("回馈模式: web")

        result = await launch_web_feedback_ui(project_directory, summary, timeout)

        # 处理取消情况
        if not result:
            return [TextContent(type="text", text="用户取消了回馈。")]

        # 储存详细结果
        save_feedback_to_file(result)

        # 建立回馈项目列表
        feedback_items = []

        # 添加文字回馈
        if (
            result.get("interactive_feedback")
            or result.get("command_logs")
            or result.get("images")
        ):
            feedback_text = create_feedback_text(result)
            feedback_items.append(TextContent(type="text", text=feedback_text))
            debug_log("文字回馈已添加")

        # 添加图片回馈
        if result.get("images"):
            mcp_images = process_images(result["images"])
            # 修复 arg-type 错误 - 直接扩展列表
            feedback_items.extend(mcp_images)
            debug_log(f"已添加 {len(mcp_images)} 张图片")

        # 确保至少有一个回馈项目
        if not feedback_items:
            feedback_items.append(
                TextContent(type="text", text="用户未提供任何回馈内容。")
            )

        debug_log(f"回馈收集完成，共 {len(feedback_items)} 个项目")
        return feedback_items

    except Exception as e:
        # 使用统一错误处理，但不影响 JSON RPC 响应
        error_id = ErrorHandler.log_error_with_context(
            e,
            context={"operation": "回馈收集", "project_dir": project_directory},
            error_type=ErrorType.SYSTEM,
        )

        # 生成用户友好的错误信息
        user_error_msg = ErrorHandler.format_user_error(e, include_technical=False)
        debug_log(f"回馈收集错误 [错误ID: {error_id}]: {e!s}")

        return [TextContent(type="text", text=user_error_msg)]


async def launch_web_feedback_ui(project_dir: str, summary: str, timeout: int) -> dict:
    """
    启动 Web UI 收集回馈，支援自订超时时间

    Args:
        project_dir: 专案目录路径
        summary: AI 工作摘要
        timeout: 超时时间（秒）

    Returns:
        dict: 收集到的回馈资料
    """
    debug_log(f"启动 Web UI 介面，超时时间: {timeout} 秒")

    try:
        # 使用新的 web 模组
        from .web import launch_web_feedback_ui as web_launch

        # 传递 timeout 参数给 Web UI
        return await web_launch(project_dir, summary, timeout)
    except ImportError as e:
        # 使用统一错误处理
        error_id = ErrorHandler.log_error_with_context(
            e,
            context={"operation": "Web UI 模组导入", "module": "web"},
            error_type=ErrorType.DEPENDENCY,
        )
        user_error_msg = ErrorHandler.format_user_error(
            e, ErrorType.DEPENDENCY, include_technical=False
        )
        debug_log(f"Web UI 模组导入失败 [错误ID: {error_id}]: {e}")

        return {
            "command_logs": "",
            "interactive_feedback": user_error_msg,
            "images": [],
        }


@mcp.tool()
def love_system_info() -> str:
    """
    love_system_info

    Returns:
        str: love_system_info
    """
    is_remote = is_remote_environment()
    is_wsl = is_wsl_environment()

    system_info = {
        "平台": sys.platform,
        "Python 版本": sys.version.split()[0],
        "WSL": is_wsl,
        "远程": is_remote,
        "洁面": "Web UI",
        "参数": {
            "SSH_CONNECTION": os.getenv("SSH_CONNECTION"),
            "SSH_CLIENT": os.getenv("SSH_CLIENT"),
            "DISPLAY": os.getenv("DISPLAY"),
            "VSCODE_INJECTION": os.getenv("VSCODE_INJECTION"),
            "SESSIONNAME": os.getenv("SESSIONNAME"),
            "WSL_DISTRO_NAME": os.getenv("WSL_DISTRO_NAME"),
            "WSL_INTEROP": os.getenv("WSL_INTEROP"),
            "WSLENV": os.getenv("WSLENV"),
        },
    }

    return json.dumps(system_info, ensure_ascii=False, indent=2)


# ===== 主程式入口 =====
def main():
    # 检查是否启用调试模式
    debug_enabled = os.getenv("MCP_DEBUG", "").lower() in ("true", "1", "yes", "on")

    # 检查是否启用桌面模式
    desktop_mode = os.getenv("MCP_DESKTOP_MODE", "").lower() in (
        "true",
        "1",
        "yes",
        "on",
    )

    if debug_enabled:
        debug_log("🚀 启动互动式回馈收集 MCP 服务器")
        debug_log(f"   服务器名称: {SERVER_NAME}")
        debug_log(f"   版本: {__version__}")
        debug_log(f"   平台: {sys.platform}")
        debug_log(f"   编码初始化: {'成功' if _encoding_initialized else '失败'}")
        debug_log(f"   远端环境: {is_remote_environment()}")
        debug_log(f"   WSL 环境: {is_wsl_environment()}")
        debug_log(f"   桌面模式: {'启用' if desktop_mode else '禁用'}")
        debug_log("   介面类型: Web UI")
        debug_log("   等待来自 AI 助手的调用...")
        debug_log("准备启动 MCP 伺服器...")
        debug_log("调用 mcp.run()...")

    try:
        # 使用正确的 FastMCP API，禁用横幅以避免干扰 MCP stdio 通信
        mcp.run(show_banner=False)
    except KeyboardInterrupt:
        if debug_enabled:
            debug_log("收到中断信号，正常退出")
        sys.exit(0)
    except Exception as e:
        if debug_enabled:
            debug_log(f"MCP 服务器启动失败: {e}")
            import traceback

            debug_log(f"详细错误: {traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
