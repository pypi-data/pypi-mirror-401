"""本地代理服务 - 支持动态切换上游代理"""
import asyncio
from typing import Optional, Dict, Tuple

class LocalProxy:
    def __init__(self, port: int = 8888):
        self.port = port
        self.upstream: Optional[str] = None  # 全局上游代理
        self.upstream_id: Optional[str] = None  # 全局代理 ID（来自 s-mgr）
        self.platform_rules: Dict[str, Tuple[str, Optional[str]]] = {}  # {keyword: (proxy_url, proxy_id)}
        self._server = None
        self._running = False
    
    async def start(self):
        """启动代理服务"""
        self._server = await asyncio.start_server(
            self._handle_connection, '127.0.0.1', self.port
        )
        self._running = True
        return self.port
    
    async def stop(self):
        """停止代理服务"""
        if self._server:
            self._server.close()
            await self._server.wait_closed()
        self._running = False
    
    def set_upstream(self, proxy_url: Optional[str], proxy_id: Optional[str] = None):
        """设置全局上游代理"""
        self.upstream = proxy_url
        self.upstream_id = proxy_id
    
    def set_platform_proxy(self, keyword: str, proxy_url: Optional[str], proxy_id: Optional[str] = None):
        """设置平台特定代理"""
        if proxy_url is None:
            self.platform_rules.pop(keyword, None)
        else:
            self.platform_rules[keyword] = (proxy_url, proxy_id)
    
    def get_proxy_for_host(self, host: str) -> Optional[str]:
        """根据 host 获取应使用的代理"""
        host_lower = host.lower()
        # 先匹配平台规则
        for keyword, (proxy_url, _) in self.platform_rules.items():
            if keyword in host_lower:
                return proxy_url
        # 返回全局代理
        return self.upstream
    
    async def _handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """处理客户端连接"""
        try:
            # 读取请求头
            request_line = await reader.readline()
            if not request_line:
                return
            
            request = request_line.decode('utf-8', errors='ignore')
            
            if request.startswith('CONNECT'):
                # HTTPS 隧道
                await self._handle_connect(request, reader, writer)
            else:
                # HTTP 请求
                await self._handle_http(request, reader, writer)
        except asyncio.CancelledError:
            pass
        except GeneratorExit:
            pass
        except Exception as e:
            pass
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass
    
    async def _handle_connect(self, request: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """处理 CONNECT 请求（HTTPS 隧道）"""
        # CONNECT host:port HTTP/1.1
        parts = request.split()
        if len(parts) < 2:
            return
        
        host_port = parts[1]
        if ':' in host_port:
            host, port = host_port.rsplit(':', 1)
            port = int(port)
        else:
            host, port = host_port, 443
        
        # 读取剩余请求头
        while True:
            line = await reader.readline()
            if line == b'\r\n' or line == b'\n' or not line:
                break
        
        proxy = self.get_proxy_for_host(host)
        
        try:
            if proxy:
                # 通过上游代理连接
                remote_reader, remote_writer = await self._connect_via_proxy(proxy, host, port)
            else:
                # 直连
                remote_reader, remote_writer = await asyncio.open_connection(host, port)
            
            # 发送 200 响应
            writer.write(b'HTTP/1.1 200 Connection Established\r\n\r\n')
            await writer.drain()
            
            # 双向转发
            await self._pipe(reader, writer, remote_reader, remote_writer)
        except Exception as e:
            writer.write(f'HTTP/1.1 502 Bad Gateway\r\n\r\n{e}'.encode())
            await writer.drain()
    
    async def _handle_http(self, request: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """处理 HTTP 请求"""
        # 解析 host
        headers = [request]
        host = None
        content_length = 0
        
        while True:
            line = await reader.readline()
            if line == b'\r\n' or line == b'\n' or not line:
                break
            headers.append(line.decode('utf-8', errors='ignore'))
            line_lower = line.decode('utf-8', errors='ignore').lower()
            if line_lower.startswith('host:'):
                host = line_lower.split(':', 1)[1].strip()
            if line_lower.startswith('content-length:'):
                content_length = int(line_lower.split(':', 1)[1].strip())
        
        if not host:
            return
        
        # 读取 body
        body = b''
        if content_length > 0:
            body = await reader.read(content_length)
        
        proxy = self.get_proxy_for_host(host)
        
        try:
            if proxy:
                # 通过上游代理
                remote_reader, remote_writer = await self._connect_via_proxy(proxy, host, 80)
            else:
                # 直连
                port = 80
                if ':' in host:
                    host, port = host.rsplit(':', 1)
                    port = int(port)
                remote_reader, remote_writer = await asyncio.open_connection(host, port)
            
            # 发送请求
            request_data = ''.join(headers).encode() + b'\r\n' + body
            remote_writer.write(request_data)
            await remote_writer.drain()
            
            # 转发响应
            while True:
                data = await remote_reader.read(8192)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
            
            remote_writer.close()
        except Exception as e:
            writer.write(f'HTTP/1.1 502 Bad Gateway\r\n\r\n{e}'.encode())
            await writer.drain()
    
    async def _connect_via_proxy(self, proxy: str, host: str, port: int):
        """通过上游代理建立连接"""
        # 解析代理 URL: socks5://host:port 或 http://host:port
        if proxy.startswith('socks5://'):
            return await self._connect_socks5(proxy[9:], host, port)
        elif proxy.startswith('http://'):
            return await self._connect_http_proxy(proxy[7:], host, port)
        else:
            # 默认当作 http 代理
            return await self._connect_http_proxy(proxy, host, port)
    
    async def _connect_http_proxy(self, proxy_addr: str, host: str, port: int):
        """通过 HTTP 代理连接"""
        if ':' in proxy_addr:
            proxy_host, proxy_port = proxy_addr.rsplit(':', 1)
            proxy_port = int(proxy_port)
        else:
            proxy_host, proxy_port = proxy_addr, 8080
        
        reader, writer = await asyncio.open_connection(proxy_host, proxy_port)
        
        # 发送 CONNECT 请求
        connect_req = f'CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n'
        writer.write(connect_req.encode())
        await writer.drain()
        
        # 读取响应
        response = await reader.readline()
        if b'200' not in response:
            raise Exception(f'Proxy connect failed: {response.decode()}')
        
        # 读取剩余响应头
        while True:
            line = await reader.readline()
            if line == b'\r\n' or not line:
                break
        
        return reader, writer
    
    async def _connect_socks5(self, proxy_addr: str, host: str, port: int):
        """通过 SOCKS5 代理连接"""
        if ':' in proxy_addr:
            proxy_host, proxy_port = proxy_addr.rsplit(':', 1)
            proxy_port = int(proxy_port)
        else:
            proxy_host, proxy_port = proxy_addr, 1080
        
        reader, writer = await asyncio.open_connection(proxy_host, proxy_port)
        
        # SOCKS5 握手
        writer.write(b'\x05\x01\x00')  # 版本5, 1种认证方式, 无认证
        await writer.drain()
        
        response = await reader.read(2)
        if response != b'\x05\x00':
            raise Exception('SOCKS5 handshake failed')
        
        # 连接请求
        host_bytes = host.encode()
        request = b'\x05\x01\x00\x03' + bytes([len(host_bytes)]) + host_bytes + port.to_bytes(2, 'big')
        writer.write(request)
        await writer.drain()
        
        response = await reader.read(10)
        if response[1] != 0:
            raise Exception(f'SOCKS5 connect failed: {response[1]}')
        
        return reader, writer
    
    async def _pipe(self, r1, w1, r2, w2):
        """双向数据转发"""
        async def forward(reader, writer):
            try:
                while True:
                    data = await reader.read(8192)
                    if not data:
                        break
                    writer.write(data)
                    await writer.drain()
            except:
                pass
        
        await asyncio.gather(
            forward(r1, w2),
            forward(r2, w1),
            return_exceptions=True
        )
        
        try:
            w2.close()
        except:
            pass
