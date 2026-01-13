"""
sdenv Python wrapper - 简化版
"""
import subprocess
import sys
import shutil
import os
import time
import asyncio
from typing import Optional, Dict, Any, List, Union
from urllib.parse import urlparse

# 内部缓存
_path = None
_cache: Dict[str, Dict] = {}
_cache_ttl = 300  # 默认缓存时间（秒）


def _find() -> str:
    """查找 sdenv 路径"""
    global _path
    if _path:
        return _path
    
    # Windows npm 全局目录
    if sys.platform == "win32":
        npm = os.path.join(os.environ.get("APPDATA", ""), "npm", "sdenv.cmd")
        if os.path.exists(npm):
            _path = npm
            return _path
    
    # PATH 中查找
    cmd = shutil.which("sdenv")
    if cmd:
        _path = cmd
        return _path
    
    raise RuntimeError("sdenv 未安装，请运行: npm install -g sdenv")


def _run(url: str, timeout: int = 120) -> str:
    """运行 sdenv 并返回输出"""
    cmd = [_find(), url]
    result = subprocess.run(cmd, capture_output=True, timeout=timeout, encoding='utf-8', errors='ignore')
    return result.stdout or ""


def _parse_cookie(output: str) -> Optional[str]:
    """从输出中提取 cookie"""
    for line in output.split("\n"):
        if "cookie" in line.lower() and "=" in line:
            for sep in ["：", ":"]:
                if sep in line:
                    cookie = line.split(sep)[-1].strip()
                    if "=" in cookie:
                        return cookie
    return None


def get_cookie(url: Union[str, List[str]], cache: bool = False, timeout: int = 120) -> Union[Optional[str], Dict[str, Optional[str]]]:
    """
    获取 cookie
    
    参数:
        url: 单个 URL 或 URL 列表
        cache: True=使用缓存, False=不使用缓存（默认）
        timeout: 超时秒数
    """
    if isinstance(url, list):
        return {u: get_cookie(u, cache, timeout) for u in url}
    
    domain = urlparse(url).netloc
    
    # 检查缓存
    if cache and domain in _cache:
        if time.time() < _cache[domain]["exp"]:
            return _cache[domain]["val"]
    
    # 获取 cookie
    output = _run(url, timeout)
    cookie = _parse_cookie(output)
    
    # 存入缓存
    if cookie and cache:
        _cache[domain] = {"val": cookie, "exp": time.time() + _cache_ttl}
    
    return cookie


async def get_cookie_async(urls: List[str], cache: bool = False, timeout: int = 120, as_list: bool = False) -> Union[Dict[str, Optional[str]], List[Optional[str]]]:
    """
    异步并发获取多个 URL 的 cookie
    
    参数:
        urls: URL 列表
        cache: 是否使用缓存
        timeout: 超时秒数
        as_list: True=返回列表（保留重复URL的结果），False=返回字典（默认）
    """
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, lambda u=u: get_cookie(u, cache, timeout)) for u in urls]
    results = await asyncio.gather(*tasks)
    return list(results) if as_list else dict(zip(urls, results))


def clear_cache(domain: str = None):
    """清除 cookie 缓存"""
    if domain:
        _cache.pop(domain, None)
    else:
        _cache.clear()


def check_install() -> Dict[str, Any]:
    """检查 sdenv 安装状态"""
    result = {"node": bool(shutil.which("node")), "sdenv": False, "path": None}
    try:
        result["path"] = _find()
        result["sdenv"] = True
    except:
        pass
    return result