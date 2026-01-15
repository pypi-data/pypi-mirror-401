#!/usr/bin/env python3
"""
通用视频下载 MCP 服务器

该服务器基于 you-get 项目，提供以下功能：
1. 查看视频信息 - 获取视频标题、大小、格式等信息
2. 下载视频 - 下载各种平台的视频内容
3. 支持多平台 - B站、YouTube、抖音、微博等100+平台
"""

import os
import sys
import json
import tempfile
import socket
import asyncio
import io
import traceback
import time
import subprocess
import platform
import urllib.parse
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urlparse
from contextlib import redirect_stdout, redirect_stderr

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context

# 导入 you-get 核心模块
from .you_get import common
from .you_get.common import any_download, print_info, url_to_module
from .you_get.util import log

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

package = "bilibili-video-download-mcp"

# 使用当前目录下的logs目录存放日志文件
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "debug.log"

file_handler = RotatingFileHandler(
    str(log_file), maxBytes=5_000_000, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)
logger.propagate = False

# 创建 MCP 服务器实例
mcp = FastMCP("Bilibili Video Download MCP Server")


def _open_aido_link(ctx: Context, return_message: str) -> None:
    """Silently execute aido://tool?xxx&chatSessionId=xxx across platforms."""
    try:
        if ctx is None:
            logger.debug("Context is None, skipping aido link execution")
            return

        request_context = getattr(ctx, "request_context", None)
        chatSessionId = None
        if request_context and hasattr(request_context, "meta"):
            context_meta = getattr(request_context, "meta", None)
            logger.debug(f"context meta: {context_meta}")
            if context_meta and hasattr(context_meta, "chatSessionId"):
                chatSessionId = getattr(context_meta, "chatSessionId", None)
                logger.debug(
                    f"chatSessionId from request_context.meta: {chatSessionId}"
                )

        if not chatSessionId or chatSessionId == "None":
            logger.warning(
                f"Invalid or missing chatSessionId: {chatSessionId}, skipping aido link execution"
            )
            return

        encoded_message = urllib.parse.quote(return_message, safe="")
        package_name = urllib.parse.quote(package, safe="")
        aido_url = f"aido://tool?path={encoded_message}&chatSessionId={chatSessionId}&package={package_name}"

        system = platform.system().lower()
        if system == "darwin":
            result = subprocess.run(
                ["open", aido_url], check=False, capture_output=True, text=True
            )
            if result.returncode != 0 and result.stderr:
                logger.warning(f"macOS open command failed: {result.stderr}")
        elif system == "windows":
            try:
                os.startfile(aido_url)
            except (OSError, AttributeError) as e:
                logger.debug(f"os.startfile failed, trying start command: {e}")
                result = subprocess.run(
                    f'start "" "{aido_url}"',
                    shell=True,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0 and result.stderr:
                    logger.warning(f"Windows start command failed: {result.stderr}")
        elif system == "linux":
            result = subprocess.run(
                ["xdg-open", aido_url], check=False, capture_output=True, text=True
            )
            if result.returncode != 0 and result.stderr:
                logger.warning(f"Linux xdg-open command failed: {result.stderr}")
        else:
            logger.warning(f"Unsupported operating system: {system}")
            return

        logger.info(f"Executed aido link on {system}: {aido_url}")
    except Exception as e:
        logger.error(f"Failed to execute aido link: {str(e)}", exc_info=True)



class RealtimeLogger:
    """即时日志记录器，同时像 StringIO 一样缓冲输出"""
    def __init__(self, logger, level=logging.INFO, is_stderr=False):
        self.buffer = io.StringIO()
        self.logger = logger
        self.level = level
        self.is_stderr = is_stderr
        self.last_progress_time = 0
        self.progress_interval = 5.0  # 进度日志间隔秒数
    
    def write(self, s: str):
        self.buffer.write(s)
        
        # 过滤空字符串
        if not s:
            return

        # 检查是否是进度条 (you-get 通常使用 \r 刷新进度)
        is_progress = '\r' in s or '%' in s
        
        current_time = time.time()
        
        if is_progress:
            # 限制进度条日志频率
            if current_time - self.last_progress_time >= self.progress_interval:
                # 清洗进度条文本，只保留最后一行或去除非打印字符
                clean_s = s.strip().replace('\r', ' ').strip()
                if clean_s:
                    self.logger.log(self.level, f"[Progress] {clean_s}")
                    self.last_progress_time = current_time
        else:
            # 普通日志，按行处理
            if s.strip():
                self.logger.log(self.level, s.strip())

    def flush(self):
        self.buffer.flush()
        
    def getvalue(self):
        return self.buffer.getvalue()


class VideoDownloadProcessor:
    """视频下载处理器"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="video_download_"))
        # 设置 you-get 的全局参数
        common.dry_run = False
        common.json_output = False
        # 为所有网络请求设置默认超时，避免长时间阻塞导致 MCP 调用超时
        # 视频下载需要更长的超时时间，设置为60秒
        try:
            socket.setdefaulttimeout(60)
        except Exception:
            pass
        
    def __del__(self):
        """清理临时目录"""
        import shutil
        if hasattr(self, 'temp_dir') and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _strip_ansi(self, text: str) -> str:
        """去除ANSI转义序列，确保输出为纯文本"""
        try:
            import re
            ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
            return ansi_escape.sub('', text)
        except Exception:
            return text
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """获取视频信息"""
        try:
            # 仅允许 bilibili 链接
            if not self._is_bilibili_url(url):
                raise Exception("仅支持哔哩哔哩（bilibili.com / b23.tv）视频链接")
            # 设置为信息模式
            original_dry_run = common.dry_run
            common.dry_run = True
            
            # 捕获输出
            output_buffer = io.StringIO()
            error_buffer = io.StringIO()
            
            try:
                with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                    # 获取模块和URL
                    module, processed_url = url_to_module(url)
                    
                    # 调用模块的download函数获取信息
                    module.download(processed_url, info_only=True)
                
                # 恢复原始设置
                common.dry_run = original_dry_run
                
                # 解析输出信息
                output = output_buffer.getvalue()
                info = self._parse_video_info(output)
                
                return {
                    "success": True,
                    "info": info,
                    "raw_output": output
                }
                
            except Exception as e:
                common.dry_run = original_dry_run
                error_output = error_buffer.getvalue()
                raise Exception(f"获取视频信息失败: {str(e)}\n{error_output}")
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_video_info(self, output: str) -> Dict[str, Any]:
        """解析 you-get 输出的视频信息（兼容大小写与 streams 列表）"""
        info: Dict[str, Any] = {}
        output = self._strip_ansi(output)
        lines = [ln.rstrip() for ln in output.splitlines()]

        # 基础键（大小写不敏感）
        for raw in lines:
            line = raw.strip()
            lower = line.lower()
            if lower.startswith('site:'):
                info['site'] = line.split(':', 1)[1].strip()
            elif lower.startswith('title:'):
                info['title'] = line.split(':', 1)[1].strip()
            elif lower.startswith('type:'):
                info['type'] = line.split(':', 1)[1].strip()
            elif lower.startswith('size:') and 'bytes' in lower:
                size_part = line.split(':', 1)[1].strip()
                try:
                    # 示例: "83.8 MiB (87892717 bytes)"
                    before, paren = size_part.split('(', 1)
                    mb_value = before.strip().split(' ')[0]
                    bytes_value = ''.join(ch for ch in paren.split(')')[0] if ch.isdigit())
                    info['size'] = {
                        'mb': float(mb_value),
                        'bytes': int(bytes_value)
                    }
                except Exception:
                    info['size_raw'] = size_part
            elif lower.startswith('real url:') or lower.startswith('real urls:'):
                url_part = line.split(':', 1)[1].strip()
                if url_part.startswith('[') and url_part.endswith(']'):
                    try:
                        info['download_urls'] = json.loads(url_part)
                    except Exception:
                        info['download_urls'] = [url_part]
                else:
                    info['download_urls'] = [url_part]

        # 解析 streams 区块
        streams: list[Dict[str, Any]] = []
        i = 0
        while i < len(lines):
            if lines[i].strip().lower().startswith('streams:'):
                i += 1
                current: Dict[str, Any] = {}
                while i < len(lines):
                    ln = lines[i]
                    s = ln.strip()
                    if s == '' or s.startswith('#'):
                        i += 1
                        continue
                    if s.startswith('- '):
                        # 新条目开始，先推入旧的
                        if current:
                            streams.append(current)
                            current = {}
                        # "- format: dash-flv480-AVC"
                        if ':' in s:
                            key, val = s[2:].split(':', 1)
                            current[key.strip().lower()] = val.strip()
                        i += 1
                        continue
                    # 子项键值，如 "container: mp4"
                    if ':' in s:
                        key, val = s.split(':', 1)
                        current[key.strip().lower()] = val.strip()
                        # 尝试解析 size
                        if key.strip().lower() == 'size':
                            size_text = val.strip()
                            try:
                                if '(' in size_text and ')' in size_text:
                                    before, paren = size_text.split('(', 1)
                                    mb_value = before.strip().split(' ')[0]
                                    bytes_value = ''.join(ch for ch in paren.split(')')[0] if ch.isdigit())
                                    current['size_parsed'] = {
                                        'mb': float(mb_value),
                                        'bytes': int(bytes_value)
                                    }
                            except Exception:
                                pass
                        i += 1
                        continue
                    # 碰到空行或非缩进行，认为 streams 结束
                    if not ln.startswith(' '):
                        break
                    i += 1
                # 结束块时推入最后一个
                if current:
                    streams.append(current)
                # 不回退 i，这样可继续扫描后续内容
            else:
                i += 1

        if streams:
            info['streams'] = streams

        return info

    def _is_bilibili_url(self, url: str) -> bool:
        """判断是否为 B 站链接（含短链）"""
        try:
            parsed = urlparse(url)
            host = (parsed.netloc or '').lower()
            return any(h in host for h in [
                'bilibili.com',
                'b23.tv',
                'live.bilibili.com',
                'www.bilibili.com'
            ])
        except Exception:
            return False
    
    def _is_cookies_required_error(self, error_output: str) -> bool:
        """检测是否为需要 cookies 的错误"""
        keywords = ["login cookies", "cookies.txt", "720p formats or above"]
        return any(kw in error_output.lower() for kw in keywords)
    
    def _get_quality_fallback_order(self) -> list[str]:
        """返回清晰度降级顺序（从高到低）- 仅包含未登录状态下可用的清晰度"""
        return ['480', '360']
    
    def _filter_formats_by_quality(self, available_formats: list[str], quality: str) -> list[str]:
        """根据清晰度过滤格式列表"""
        return [fmt for fmt in available_formats if quality in fmt]

    async def download_video(self, url: str, output_dir: Optional[str] = None, selected_format: Optional[str] = None, cookies_path: Optional[str] = None, merge: Optional[bool] = None, ctx: Context = None) -> Dict[str, Any]:
        """下载视频"""
        execution_start_time = time.time()
        try:
            # 仅允许 bilibili 链接
            if not self._is_bilibili_url(url):
                raise Exception("仅支持哔哩哔哩（bilibili.com / b23.tv）视频链接")
            if output_dir is None:
                # 默认下载到桌面
                output_dir = os.path.expanduser("~/Desktop")
            else:
                # 展开 ~ 与环境变量，标准化为绝对路径
                output_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(output_dir)))
            
            if ctx:
                ctx.info(f"开始下载视频: {url}")
                ctx.info(f"下载目录: {output_dir}")
            
            logger.info(f"Starting download: {url} -> {output_dir}")
            
            # 确保输出目录存在
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 记录下载前的文件列表(检测当前目录和一级子目录)
            files_before = set()
            if output_path.exists():
                # 检测当前目录的文件
                for item in output_path.iterdir():
                    if item.is_file():
                        files_before.add(item)
                    # 检测一级子目录中的文件
                    elif item.is_dir():
                        for subitem in item.iterdir():
                            if subitem.is_file():
                                files_before.add(subitem)
            
            # 设置下载参数
            original_dry_run = common.dry_run
            common.dry_run = False
            
            # 使用实时日志记录器 Capture output with realtime logging
            output_logger = RealtimeLogger(logger, logging.INFO)
            error_logger = RealtimeLogger(logger, logging.ERROR, is_stderr=True)
            
            try:
                with redirect_stdout(output_logger), redirect_stderr(error_logger):
                    # 获取模块和URL
                    if ctx:
                        ctx.info("正在解析视频信息...")
                    module, processed_url = url_to_module(url)
                    
                    # 如果提供 cookies 路径，加载登录 cookies 以支持更高清晰度
                    if cookies_path:
                        try:
                            cp = os.path.expanduser(os.path.expandvars(cookies_path))
                            common.load_cookies(cp)
                            if ctx:
                                ctx.info(f"已加载 cookies: {cp}")
                        except Exception as e:
                            if ctx:
                                ctx.warning(f"加载 cookies 失败: {e}")
                            logger.warning(f"Failed to load cookies: {e}")


                    # 规范化用户传入的 format，去除ANSI转义并裁剪空白
                    if selected_format:
                        selected_format = self._strip_ansi(selected_format).strip()

                    # 获取可用的格式列表（用于降级重试）
                    info_out = io.StringIO()
                    info_err = io.StringIO()
                    with redirect_stdout(info_out), redirect_stderr(info_err):
                        module.download(processed_url, info_only=True)
                    info_parsed = self._parse_video_info(info_out.getvalue())
                    available_formats = []
                    if isinstance(info_parsed, dict) and isinstance(info_parsed.get('streams'), list):
                        for s in info_parsed['streams']:
                            fmt = s.get('format')
                            if fmt:
                                fmt = self._strip_ansi(fmt).strip()
                                available_formats.append(fmt)
                    
                    logger.info(f"Available formats: {available_formats}")
                    
                    # 准备下载尝试列表
                    formats_to_try = []
                    
                    if selected_format:
                        # 用户指定了格式，先尝试用户格式
                        if selected_format in available_formats:
                            formats_to_try.append(selected_format)
                        else:
                            logger.warning(f"User specified format '{selected_format}' not available")
                    
                    # 如果没有 cookies，准备降级格式列表
                    if not cookies_path:
                        quality_order = self._get_quality_fallback_order()
                        for quality in quality_order:
                            matching_formats = self._filter_formats_by_quality(available_formats, quality)
                            if matching_formats:
                                # 选择第一个匹配的格式
                                if matching_formats[0] not in formats_to_try:
                                    formats_to_try.append(matching_formats[0])
                    
                    # 如果列表为空，尝试默认（不指定格式）
                    if not formats_to_try:
                        formats_to_try.append(None)  # None 表示使用默认格式
                    
                    logger.info(f"Formats to try (in order): {formats_to_try}")
                    
                    # 尝试下载，遇到 cookies 错误时降级
                    last_error = None
                    download_successful = False
                    
                    for attempt_format in formats_to_try:
                        try:
                            # 清空之前的输出缓冲
                            output_logger = RealtimeLogger(logger, logging.INFO)
                            error_logger = RealtimeLogger(logger, logging.ERROR, is_stderr=True)
                            
                            if ctx:
                                if attempt_format:
                                    ctx.info(f"尝试下载格式: {attempt_format}")
                                else:
                                    ctx.info("尝试下载默认格式")
                            
                            logger.info(f"Attempting download with format: {attempt_format}")
                            
                            with redirect_stdout(output_logger), redirect_stderr(error_logger):
                                kwargs = {"output_dir": output_dir, "merge": True if merge is None else bool(merge)}
                                if attempt_format:
                                    kwargs["stream_id"] = attempt_format
                                
                                # 执行下载
                                module.download(processed_url, **kwargs)
                            
                            # 检查是否真的下载成功（有新文件）
                            files_after = set()
                            if output_path.exists():
                                for item in output_path.iterdir():
                                    if item.is_file():
                                        files_after.add(item)
                                    elif item.is_dir():
                                        for subitem in item.iterdir():
                                            if subitem.is_file():
                                                files_after.add(subitem)
                            
                            new_files = files_after - files_before
                            
                            if new_files:
                                # 下载成功
                                download_successful = True
                                downloaded_files = [str(f.absolute()) for f in new_files]
                                logger.info(f"Download successful with format: {attempt_format}")
                                break
                            else:
                                # 没有新文件，检查原因
                                err_log = error_logger.getvalue()
                                out_log = output_logger.getvalue()
                                
                                # 检查是否是文件已存在
                                if "already exists" in out_log or "already exists" in err_log:
                                    logger.info(f"File already exists, skipping format {attempt_format}")
                                    if ctx:
                                        ctx.info("文件已存在，跳过下载")
                                    
                                    # 尝试从错误信息中提取文件路径
                                    import re
                                    combined_log = out_log + err_log
                                    # 匹配 "Skipping <path>: file already exists" 格式
                                    match = re.search(r'Skipping\s+(.+?):\s*file already exists', combined_log, re.IGNORECASE)
                                    if match:
                                        existing_file = match.group(1).strip()
                                        # 标准化路径
                                        existing_file = os.path.abspath(existing_file)
                                        downloaded_files = [existing_file]
                                        logger.info(f"Existing file found: {existing_file}")
                                    else:
                                        downloaded_files = []
                                    
                                    download_successful = True
                                    break
                                
                                # 检查是否是 cookies 错误
                                if self._is_cookies_required_error(err_log) or self._is_cookies_required_error(out_log):
                                    logger.warning(f"Format {attempt_format} requires cookies, trying next quality")
                                    if ctx:
                                        ctx.warning(f"格式 {attempt_format} 需要登录，尝试更低清晰度")
                                    continue
                                else:
                                    # 其他原因导致没有文件
                                    last_error = f"No files downloaded. Logs: {out_log[:500]}"
                                    continue
                        
                        except Exception as e:
                            err_msg = str(e)
                            logger.warning(f"Download attempt with format {attempt_format} failed: {err_msg}")
                            
                            # 检查是否是 cookies 错误
                            if self._is_cookies_required_error(err_msg):
                                logger.info(f"Cookies required for {attempt_format}, trying lower quality")
                                if ctx:
                                    ctx.warning(f"格式 {attempt_format} 需要登录，尝试更低清晰度")
                                last_error = err_msg
                                continue
                            else:
                                # 其他错误，继续尝试
                                last_error = err_msg
                                continue
                    
                    if not download_successful:
                        # 所有格式都失败了
                        raise Exception(f"所有格式下载均失败。最后错误: {last_error}")
                
                # 恢复原始设置
                common.dry_run = original_dry_run
                
                # downloaded_files 已在重试循环中设置
                if ctx:
                    ctx.info(f"下载完成！文件保存在: {output_dir}")
                    for file_path in downloaded_files:
                        ctx.info(f"下载文件: {Path(file_path).name}")
                
                # 计算执行时间
                execution_time = time.time() - execution_start_time
                
                logger.info(f"Download finished. Time: {execution_time:.2f}s. Files found: {downloaded_files}")

                return {
                    "success": True,
                    "output_dir": output_dir,
                    "downloaded_files": downloaded_files,
                    "raw_output": output_logger.getvalue(),
                    "execution_time": execution_time
                }
                
            except Exception as e:
                common.dry_run = original_dry_run
                error_output = error_logger.getvalue()
                error_msg = f"下载失败: {str(e)}"
                if error_output:
                    error_msg += f"\n详细错误信息:\n{error_output}"
                raise Exception(error_msg)
            
        except Exception as e:
            if ctx:
                ctx.error(f"下载过程中出现错误: {str(e)}")
            logger.error(f"Error during download process: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }


@mcp.tool()
def get_video_info(url: str) -> str:
    """
    获取B站视频信息（仅支持哔哩哔哩）
    
    参数:
    - url: 视频链接URL
    
    返回:
    - 包含视频信息的JSON字符串（标题、大小、格式、平台等）
    
    仅支持以下域名：
    - bilibili.com
    - b23.tv
    """
    try:
        processor = VideoDownloadProcessor()
        result = processor.get_video_info(url)

        if result["success"]:
            return json.dumps({
                "status": "success",
                "url": url,
                **result["info"],
                "message": "视频信息获取成功"
            }, ensure_ascii=False, indent=2)
        else:
            raise Exception(f"获取视频信息失败: {result['error']}")

    except Exception as e:
        # 抛出异常让 MCP 标记 isError=true
        raise


@mcp.tool()
async def download_video(
    url: str,
    output_dir: Optional[str] = None,
    format: Optional[str] = None,
    cookies_path: Optional[str] = None,
    merge: Optional[bool] = None,
    ctx: Context = None
) -> str:
    """
    下载B站视频（仅支持哔哩哔哩）
    
    参数:
    - url: 视频链接URL
    - output_dir: 输出目录路径（可选，默认为桌面）
    
    返回:
    - 包含下载结果的JSON字符串
    
    仅支持以下域名：
    - bilibili.com
    - b23.tv
    """
    try:
        processor = VideoDownloadProcessor()
        result = await processor.download_video(url, output_dir, selected_format=format, cookies_path=cookies_path, merge=merge, ctx=ctx)

        if result["success"]:
            execution_time = result.get("execution_time", 0)
            downloaded_files = result["downloaded_files"]
            
            # 只有执行时间超过59秒才调用 _open_aido_link
            if execution_time > 59 and downloaded_files:
                # 使用第一个下载的文件路径作为通知路径
                _open_aido_link(ctx, downloaded_files[0])
            
            return json.dumps({
                "status": "success",
                "url": url,
                "output_dir": result["output_dir"],
                "downloaded_files": downloaded_files,
                "file_count": len(downloaded_files),
                "execution_time": f"{execution_time:.2f} seconds",
                "message": "视频下载成功"
            }, ensure_ascii=False, indent=2)
        else:
            raise Exception(result["error"])  # 让 MCP 标记 isError=true

    except Exception as e:
        if ctx:
            ctx.error(f"下载过程中出现错误: {str(e)}")
        # 抛出异常让 MCP 标记 isError=true
        raise


@mcp.resource("video://info/{url}")
def get_video_resource(url: str) -> str:
    """
    获取指定URL视频的详细信息资源
    
    参数:
    - url: 视频URL（需要URL编码）
    
    返回:
    - 视频详细信息
    """
    try:
        from urllib.parse import unquote
        decoded_url = unquote(url)
        processor = VideoDownloadProcessor()
        result = processor.get_video_info(decoded_url)
        
        if result["success"]:
            return json.dumps(result["info"], ensure_ascii=False, indent=2)
        else:
            return f"获取视频信息失败: {result['error']}"
    except Exception as e:
        return f"获取视频资源失败: {str(e)}"


@mcp.prompt()
def video_download_guide() -> str:
    """B站视频下载MCP服务使用指南（仅支持哔哩哔哩）"""
    return """
# B站视频下载MCP服务使用指南

## 功能说明
这个MCP服务器基于you-get项目，只支持从哔哩哔哩（bilibili.com/b23.tv）下载视频内容。

## 支持的平台
- 哔哩哔哩（bilibili.com / b23.tv）

## 工具说明
- `get_video_info`: 获取视频信息（标题、大小、格式等）
- `download_video`: 下载视频文件到指定目录
- `video://info/{url}`: 获取指定URL视频的详细信息资源

## 使用示例

### 获取视频信息（B站）
```
使用 get_video_info 工具，传入视频URL：
- https://www.bilibili.com/video/BV1xx411c7mu
```

### 下载视频（B站）
```
使用 download_video 工具：
- url: 视频链接
- output_dir: 下载目录（可选，默认为桌面）
```

## Claude Desktop 配置示例
```json
{
  "mcpServers": {
    "video-download-mcp": {
      "name": "Video Download MCP",
      "type": "stdio",
  "description": "Bilibili-only video downloader",
      "isActive": true,
      "registryUrl": "",
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/your/video_download_mcp",
        "run",
        "python",
        "-m",
        "bilibili_video_download_mcp"
      ]
    }
  }
}
```

## 注意事项
- 请遵守B站的使用条款和版权规定
- 某些视频可能需要登录或有地理限制
- 下载大文件时请确保网络连接稳定
- 建议定期更新以支持最新的平台变化

## 支持的视频格式
- MP4, FLV, WebM, 3GP, MKV
- MP3, M4A, OGG（音频）
- 自动选择最佳质量或指定格式下载

## 技术特性
- 仅支持B站
- 自动格式检测
- 进度显示
- 断点续传（部分平台）
- 批量下载支持
"""


def main():
    """启动MCP服务器"""
    mcp.run()


if __name__ == "__main__":
    main()