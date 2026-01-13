# -*- coding: utf-8 -*-
"""pycdp 包类型存根文件"""
from typing import Any, Dict, Optional


class CDP:
    """独立的 CDP 客户端
    
    Args:
        port: Chrome 调试端口，默认 9222
    """
    
    def __init__(self, port: int = 9222) -> None: ...
    
    @property
    def options(self) -> Any:
        """返回 ChromiumOptions 实例，用于传给 Chromium"""
        ...
    
    @property
    def port(self) -> int: ...
    
    def run(self, js: str, wait: bool = False) -> Any:
        """执行JS代码"""
        ...
    
    def request(self, url: str, method: str = 'GET', body: Optional[Dict] = None, headers: Optional[Dict] = None, token_key: Optional[str] = None, extra: Optional[Dict] = None) -> Dict[str, Any]:
        """发送请求（绕过反爬）"""
        ...
    
    def get(self, url: str, headers: Optional[Dict] = None, token_key: Optional[str] = None, extra: Optional[Dict] = None) -> Dict[str, Any]:
        """GET 请求"""
        ...
    
    def post(self, url: str, body: Optional[Dict] = None, headers: Optional[Dict] = None, token_key: Optional[str] = None, extra: Optional[Dict] = None) -> Dict[str, Any]:
        """POST 请求"""
        ...
    
    def put(self, url: str, body: Optional[Dict] = None, headers: Optional[Dict] = None, token_key: Optional[str] = None, extra: Optional[Dict] = None) -> Dict[str, Any]:
        """PUT 请求"""
        ...
    
    def delete(self, url: str, headers: Optional[Dict] = None, token_key: Optional[str] = None, extra: Optional[Dict] = None) -> Dict[str, Any]:
        """DELETE 请求"""
        ...
    
    def storage(self, key: str, value: Optional[str] = None, storage: str = 'localStorage') -> Optional[str]:
        """获取或设置存储"""
        ...
    
    def cookies(self, name: Optional[str] = None) -> Optional[str]:
        """获取 cookies"""
        ...
    
    def close(self) -> None:
        """关闭连接"""
        ...


class Chromium:
    """DrissionPage 增强版，集成 CDP 功能
    
    Args:
        addr_or_opts: 地址或配置选项
        cdp: 可选，传入已有的 CDP 实例共享使用
    """
    
    def __init__(self, addr_or_opts: Any = None, cdp: Optional[CDP] = None, **kwargs) -> None: ...
    
    @property
    def cdp(self) -> CDP:
        """获取 CDP 实例"""
        ...
    
    def get(self, url: str, **kwargs) -> Any:
        """访问页面"""
        ...
    
    @property
    def wait(self) -> Any:
        """等待操作"""
        ...
    
    def ele(self, locator: str, timeout: Optional[float] = None) -> Any:
        """查找元素"""
        ...
    
    def eles(self, locator: str, timeout: Optional[float] = None) -> Any:
        """查找多个元素"""
        ...
    
    @property
    def url(self) -> str:
        """当前页面 URL"""
        ...
    
    @property
    def html(self) -> str:
        """页面 HTML"""
        ...
    
    @property
    def latest_tab(self) -> Any:
        """最新标签页"""
        ...
    
    def new_tab(self, url: Optional[str] = None, **kwargs) -> Any:
        """新建标签页"""
        ...
    
    def get_tab(self, **kwargs) -> Any:
        """获取标签页"""
        ...


__all__: list[str]