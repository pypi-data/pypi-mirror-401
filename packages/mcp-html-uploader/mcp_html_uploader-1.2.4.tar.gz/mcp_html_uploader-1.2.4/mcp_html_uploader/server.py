#!/usr/bin/env python3
"""
MCP 服务器 - 提供 HTML 文件创建和阿里云 OSS 上传功能
"""

import os
import json
import mimetypes
from pathlib import Path
from typing import Any, Optional
from datetime import datetime
import oss2
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

# 初始化 MCP 服务器
app = Server("html-file-server")

# OSS 配置（从配置文件读取）
OSS_CONFIG = None
OSS_BUCKET = None


def load_oss_config() -> Optional[dict]:
    """加载 OSS 配置文件"""
    global OSS_CONFIG, OSS_BUCKET
    
    # 尝试从多个位置读取配置文件
    config_paths = [
        Path.cwd() / "config.json",  # 当前目录
        Path(__file__).parent.parent / "config.json",  # 项目根目录
        Path.home() / ".mcp-html-uploader" / "config.json",  # 用户主目录
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    OSS_CONFIG = config.get('oss', {})
                    
                    # 初始化 OSS Bucket
                    auth = oss2.Auth(
                        OSS_CONFIG['access_key_id'],
                        OSS_CONFIG['access_key_secret']
                    )
                    
                    # 检查是否使用 CNAME（自定义域名）
                    is_cname = OSS_CONFIG.get('is_cname', False)
                    
                    OSS_BUCKET = oss2.Bucket(
                        auth,
                        OSS_CONFIG['endpoint'],
                        OSS_CONFIG['bucket'],
                        is_cname=is_cname
                    )
                    
                    return OSS_CONFIG
            except Exception as e:
                print(f"加载配置文件失败 {config_path}: {e}")
                continue
    
    return None


@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的工具"""
    return [
        Tool(
            name="create_html",
            description="创建 HTML 内容。根据提供的内容生成格式良好的 HTML 代码并返回（不保存文件）。",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "HTML 文件的主体内容（可以是完整的 HTML 代码或仅内容）"
                    }
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="upload_file",
            description="上传文件到阿里云 OSS。支持上传任何类型的文件，返回文件 URL。",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "要上传的文件路径（相对或绝对路径）"
                    },
                    "access_key_id": {
                        "type": "string",
                        "description": "阿里云 AccessKey ID"
                    },
                    "access_key_secret": {
                        "type": "string",
                        "description": "阿里云 AccessKey Secret"
                    },
                    "bucket": {
                        "type": "string",
                        "description": "OSS Bucket 名称"
                    },
                    "endpoint": {
                        "type": "string",
                        "description": "OSS Endpoint 地址"
                    },
                    "oss_path": {
                        "type": "string",
                        "description": "OSS 中的文件路径（可选，不填则自动生成）",
                        "default": ""
                    },
                    "base_path": {
                        "type": "string",
                        "description": "文件存储路径前缀（可选）",
                        "default": ""
                    },
                    "is_cname": {
                        "type": ["boolean", "string"],
                        "description": "是否使用自定义域名（CNAME）。支持布尔值或字符串（true/false, 1/0, yes/no）",
                        "default": False
                    }
                },
                "required": ["file_path", "access_key_id", "access_key_secret", "bucket", "endpoint"]
            }
        ),
        Tool(
            name="create_and_upload_html",
            description="创建 HTML 内容并立即上传到阿里云 OSS，返回文件 URL。内存操作，无需本地文件系统权限。",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "HTML 文件的主体内容（可以是完整的 HTML 代码或仅内容）"
                    },
                    "access_key_id": {
                        "type": "string",
                        "description": "阿里云 AccessKey ID"
                    },
                    "access_key_secret": {
                        "type": "string",
                        "description": "阿里云 AccessKey Secret"
                    },
                    "bucket": {
                        "type": "string",
                        "description": "OSS Bucket 名称"
                    },
                    "endpoint": {
                        "type": "string",
                        "description": "OSS Endpoint 地址"
                    },
                    "oss_path": {
                        "type": "string",
                        "description": "OSS 中的文件路径（可选，不填则自动生成）",
                        "default": ""
                    },
                    "base_path": {
                        "type": "string",
                        "description": "文件存储路径前缀（可选）",
                        "default": ""
                    },
                    "is_cname": {
                        "type": "string",
                        "description": "是否使用自定义域名（CNAME）。支持字符串：true/false, 1/0, yes/no",
                        "default": "false"
                    }
                },
                "required": ["content", "access_key_id", "access_key_secret", "bucket", "endpoint"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """处理工具调用"""
    
    if name == "create_html":
        return await create_html_file(arguments)
    elif name == "upload_file":
        return await upload_file(arguments)
    elif name == "create_and_upload_html":
        return await create_and_upload_html(arguments)
    else:
        return [TextContent(type="text", text=f"错误：未知的工具 '{name}'")]


async def create_html_file(args: dict) -> list[TextContent]:
    """创建 HTML 文件（返回内容，不保存到本地）"""
    try:
        content = args.get("content", "")
        
        # 验证内容
        if not content:
            return [TextContent(type="text", text="错误：必须提供 HTML 内容")]
        
        # 自动生成标题
        title = "文档"
        
        # 判断内容是否已经是完整的 HTML
        content_lower = content.strip().lower()
        if content_lower.startswith('<!doctype') or content_lower.startswith('<html'):
            # 已经是完整的 HTML
            html_content = content
        else:
            # 需要包装成完整的 HTML
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
{content}
</body>
</html>"""
        
        # 返回 HTML 内容（不保存文件，避免文件系统权限问题）
        return [TextContent(
            type="text",
            text=f"成功创建 HTML 内容！\n\n{html_content}\n\n文件大小：{len(html_content)} 字节"
        )]
        
    except Exception as e:
        return [TextContent(type="text", text=f"创建 HTML 文件时出错：{str(e)}")]


async def upload_file(args: dict) -> list[TextContent]:
    """上传文件到阿里云 OSS"""
    try:
        file_path = args.get("file_path", "")
        access_key_id = args.get("access_key_id", "")
        access_key_secret = args.get("access_key_secret", "")
        bucket = args.get("bucket", "")
        endpoint = args.get("endpoint", "")
        oss_path = args.get("oss_path", "")
        base_path = args.get("base_path", "")
        is_cname = args.get("is_cname", False)
        
        # 确保 is_cname 是布尔值（处理字符串传递的情况）
        if isinstance(is_cname, str):
            is_cname = is_cname.lower() in ['true', '1', 'yes']
        
        # 验证必需参数
        if not file_path:
            return [TextContent(type="text", text="错误：必须提供文件路径")]
        if not access_key_id or not access_key_secret:
            return [TextContent(type="text", text="错误：必须提供 AccessKey ID 和 Secret")]
        if not bucket or not endpoint:
            return [TextContent(type="text", text="错误：必须提供 Bucket 和 Endpoint")]
        
        # 转换为 Path 对象
        path = Path(file_path)
        
        # 检查文件是否存在
        if not path.exists():
            return [TextContent(type="text", text=f"错误：文件不存在：{file_path}")]
        
        if not path.is_file():
            return [TextContent(type="text", text=f"错误：路径不是文件：{file_path}")]
        
        # 初始化 OSS 连接
        auth = oss2.Auth(access_key_id, access_key_secret)
        oss_bucket = oss2.Bucket(auth, endpoint, bucket, is_cname=is_cname)
        
        # 确定 OSS 路径
        if not oss_path:
            oss_path = f"{base_path}{path.name}"
        
        # 获取文件信息
        mime_type, _ = mimetypes.guess_type(str(path))
        if mime_type is None:
            mime_type = 'application/octet-stream'
        
        # 上传到 OSS
        result = oss_bucket.put_object_from_file(
            oss_path,
            str(path),
            headers={'Content-Type': mime_type}
        )
        
        # 生成文件 URL
        if result.status == 200:
            # 构建 URL
            if is_cname:
                # CNAME 模式：直接使用 endpoint
                file_url = f"https://{endpoint}/{oss_path}"
            else:
                # 标准模式：bucket.endpoint
                file_url = f"https://{bucket}.{endpoint}/{oss_path}"
            
            return [TextContent(type="text", text=file_url)]
        else:
            return [TextContent(type="text", text=f"上传失败，状态码：{result.status}")]
        
    except oss2.exceptions.OssError as e:
        return [TextContent(type="text", text=f"OSS 错误：{e}")]
    except Exception as e:
        return [TextContent(type="text", text=f"上传文件时出错：{str(e)}")]


async def create_and_upload_html(args: dict) -> list[TextContent]:
    """创建 HTML 文件并上传到阿里云 OSS（内存操作，不保存本地文件）"""
    try:
        content = args.get("content", "")
        access_key_id = args.get("access_key_id", "")
        access_key_secret = args.get("access_key_secret", "")
        bucket = args.get("bucket", "")
        endpoint = args.get("endpoint", "")
        oss_path = args.get("oss_path", "")
        base_path = args.get("base_path", "")
        is_cname = args.get("is_cname", False)
        
        # 确保 is_cname 是布尔值（处理字符串传递的情况）
        if isinstance(is_cname, str):
            is_cname = is_cname.lower() in ['true', '1', 'yes']
        
        # 验证必需参数
        if not content:
            return [TextContent(type="text", text="错误：必须提供 HTML 内容")]
        if not access_key_id or not access_key_secret:
            return [TextContent(type="text", text="错误：必须提供 AccessKey ID 和 Secret")]
        if not bucket or not endpoint:
            return [TextContent(type="text", text="错误：必须提供 Bucket 和 Endpoint")]
        
        # 初始化 OSS 连接
        auth = oss2.Auth(access_key_id, access_key_secret)
        oss_bucket = oss2.Bucket(auth, endpoint, bucket, is_cname=is_cname)
        
        # 生成文件名（使用时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"page_{timestamp}.html"
        
        # 自动生成标题
        title = "文档"
        
        # 判断内容是否已经是完整的 HTML
        content_lower = content.strip().lower()
        
        if content_lower.startswith('<!doctype') or content_lower.startswith('<html'):
            html_content = content
        else:
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
{content}
</body>
</html>"""
        
        # 确定 OSS 路径
        if not oss_path:
            oss_path = f"{base_path}{filename}"
        
        # 直接在内存中准备上传（不保存到文件系统，避免权限问题）
        file_content = html_content.encode('utf-8')
        
        # 上传到 OSS
        result = oss_bucket.put_object(
            oss_path,
            file_content,
            headers={'Content-Type': 'text/html; charset=utf-8'}
        )
        
        # 生成文件 URL
        if result.status == 200:
            # 构建 URL
            if is_cname:
                # CNAME 模式：直接使用 endpoint
                file_url = f"https://{endpoint}/{oss_path}"
            else:
                # 标准模式：bucket.endpoint
                file_url = f"https://{bucket}.{endpoint}/{oss_path}"
            
            return [TextContent(type="text", text=file_url)]
        else:
            return [TextContent(type="text", text=f"上传失败，状态码：{result.status}")]
        
    except oss2.exceptions.OssError as e:
        return [TextContent(type="text", text=f"OSS 错误：{e}")]
    except Exception as e:
        return [TextContent(type="text", text=f"创建并上传 HTML 文件时出错：{str(e)}")]


async def async_main():
    """运行服务器（异步入口）"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def main():
    """主入口函数"""
    import asyncio
    asyncio.run(async_main())


if __name__ == "__main__":
    main()

