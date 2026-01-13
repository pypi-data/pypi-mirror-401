# -*- coding: utf-8 -*-
"""
pycdp - Chrome DevTools Protocol 客户端
支持独立使用或与 DrissionPage 配合使用
"""
import json
import requests
import websocket


class CDP:
    """独立的 CDP 客户端
    
    Args:
        port: Chrome 调试端口，默认 9222
    """
    
    def __init__(self, port: int = 9222):
        self._port = port
        self._ws = None
        self._id = 0
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
    
    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
    
    @property
    def port(self) -> int:
        return self._port
    
    def _get_ws(self):
        if self._ws is None:
            try:
                pages = requests.get(f'http://127.0.0.1:{self._port}/json', timeout=5).json()
                if not pages:
                    raise Exception('没有可用的页面')
                self._ws = websocket.create_connection(pages[0]['webSocketDebuggerUrl'], timeout=30)
            except Exception as e:
                raise Exception(f'CDP 连接失败: {e}')
        return self._ws
    
    def run(self, js: str, wait: bool = False):
        """执行JS代码"""
        ws = self._get_ws()
        self._id += 1
        ws.send(json.dumps({
            'id': self._id,
            'method': 'Runtime.evaluate',
            'params': {'expression': js, 'returnByValue': True, 'awaitPromise': wait}
        }))
        r = json.loads(ws.recv())
        if 'error' in r:
            raise Exception(r['error'].get('message', str(r['error'])))
        return r.get('result', {}).get('result', {}).get('value')
    
    def request(self, url: str, method: str = 'GET', body: dict = None, headers: dict = None, token_key: str = None, extra: dict = None) -> dict:
        """发送请求（绕过反爬）"""
        h = headers or {}
        if body is not None and 'Content-Type' not in h:
            h['Content-Type'] = 'application/json'
        
        token_js = f'let tk=localStorage.getItem("{token_key}");if(tk)h.Authorization="Bearer "+tk;' if token_key else ''
        extra_js = f'Object.assign(h,{json.dumps(extra)});' if extra else ''
        body_js = f',body:JSON.stringify({json.dumps(body)})' if body is not None else ''
        
        js = f'''(async()=>{{
            try{{
                let h={json.dumps(h)};
                {token_js}
                {extra_js}
                let r=await fetch("{url}",{{method:"{method}",headers:h{body_js},credentials:"include"}});
                let txt=await r.text();
                let d;try{{d=JSON.parse(txt)}}catch{{d=txt}}
                return {{status:r.status,data:d}};
            }}catch(e){{return {{error:e.message}}}}
        }})()'''
        return self.run(js, wait=True)
    
    def get(self, url: str, headers: dict = None, token_key: str = None, extra: dict = None) -> dict:
        """GET 请求"""
        return self.request(url, 'GET', headers=headers, token_key=token_key, extra=extra)
    
    def post(self, url: str, body: dict = None, headers: dict = None, token_key: str = None, extra: dict = None) -> dict:
        """POST 请求"""
        return self.request(url, 'POST', body, headers=headers, token_key=token_key, extra=extra)
    
    def put(self, url: str, body: dict = None, headers: dict = None, token_key: str = None, extra: dict = None) -> dict:
        """PUT 请求"""
        return self.request(url, 'PUT', body, headers=headers, token_key=token_key, extra=extra)
    
    def delete(self, url: str, headers: dict = None, token_key: str = None, extra: dict = None) -> dict:
        """DELETE 请求"""
        return self.request(url, 'DELETE', headers=headers, token_key=token_key, extra=extra)
    
    def storage(self, key: str, value: str = None, storage: str = 'localStorage') -> str:
        """获取或设置存储"""
        if value is None:
            return self.run(f'{storage}.getItem("{key}")')
        return self.run(f'{storage}.setItem("{key}",{json.dumps(value)})')
    
    def cookies(self, name: str = None) -> str:
        """获取 cookies"""
        if name:
            return self.run(f'document.cookie.split("; ").find(c=>c.startsWith("{name}="))?.split("=")[1]')
        return self.run('document.cookie')
    
    def close(self) -> None:
        """关闭连接"""
        if self._ws:
            self._ws.close()
            self._ws = None


# DrissionPage 增强版 - 直接定义类以支持 IDE 类型提示
try:
    from DrissionPage import Chromium as _Chromium, ChromiumOptions
    
    class Chromium(_Chromium):
        """DrissionPage 增强版，集成 CDP 功能
        
        Args:
            addr_or_opts: 地址或配置选项
            cdp: 可选，传入已有的 CDP 实例共享使用
        """
        
        def __new__(cls, addr_or_opts=None, **kwargs):
            kwargs.pop('cdp', None)  # 移除 cdp 参数，避免传递给父类 __new__
            return super().__new__(cls, addr_or_opts, **kwargs)
        
        def __init__(self, addr_or_opts=None, **kwargs):
            cdp = kwargs.pop('cdp', None)  # 提取 cdp 参数，避免传递给父类 __init__
            
            if addr_or_opts is None:
                opts = ChromiumOptions()
                opts.set_argument('--remote-allow-origins=*')
                addr_or_opts = opts
            elif isinstance(addr_or_opts, ChromiumOptions):
                addr_or_opts.set_argument('--remote-allow-origins=*')
            
            super().__init__(addr_or_opts, **kwargs)
            self._port = int(self.address.split(':')[-1]) if self.address else 9222
            
            # 支持传入已有的 CDP 实例，或自动创建
            if cdp is not None:
                self._cdp = cdp
            else:
                self._cdp = CDP(self._port)
        
        @property
        def cdp(self) -> CDP:
            """获取 CDP 实例"""
            return self._cdp
        
        # Tab 代理方法
        def get(self, url: str, **kwargs):
            """访问页面"""
            return self.latest_tab.get(url, **kwargs)
        
        @property
        def wait(self):
            """等待操作"""
            return self.latest_tab.wait
        
        def ele(self, locator: str, timeout: float = None):
            """查找元素"""
            return self.latest_tab.ele(locator, timeout=timeout)
        
        def eles(self, locator: str, timeout: float = None):
            """查找多个元素"""
            return self.latest_tab.eles(locator, timeout=timeout)
        
        @property
        def url(self) -> str:
            """当前页面 URL"""
            return self.latest_tab.url
        
        @property
        def html(self) -> str:
            """页面 HTML"""
            return self.latest_tab.html

except ImportError:
    # DrissionPage 未安装时，Chromium 为 None
    Chromium = None