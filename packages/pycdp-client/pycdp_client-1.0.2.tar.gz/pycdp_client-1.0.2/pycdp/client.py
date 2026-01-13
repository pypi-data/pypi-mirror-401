# -*- coding: utf-8 -*-
"""
pycdp - Chrome DevTools Protocol 客户端

使用示例:
    from pycdp.client import CDP
    from DrissionPage import Chromium
    
    cdp = CDP(port=9222)
    page = Chromium(cdp).latest_tab
    
    page.get("https://example.com")
    
    result = cdp.request(
        'https://api.example.com/data',
        'POST',
        body={'key': 'value'},
        token_key='ACCESS_TOKEN',
        extra={'userType': 'USER'}
    )
    print(result)
"""
import json
import requests
import websocket
from DrissionPage import ChromiumOptions


class CDP(ChromiumOptions):
    """CDP 客户端，继承 ChromiumOptions 可直接传给 Chromium
    
    Args:
        port: Chrome 调试端口，默认 9222
    """
    
    def __init__(self, port: int = None):
        super().__init__()
        self._port = port or 9222
        self.set_local_port(self._port)
        self.set_argument('--remote-allow-origins=*')
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
    
    @port.setter
    def port(self, value: int):
        """设置端口（会关闭现有连接）"""
        if self._ws:
            self._ws.close()
            self._ws = None
        self._port = value
        self.set_local_port(value)
    
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

