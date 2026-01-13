#!/usr/bin/env python3
"""REPL 主循环"""
import asyncio
import time
import shlex
from typing import Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from mp_repl.config import config, CONFIG_DIR, HISTORY_FILE
from mp_repl.connection import ConnectionManager
from mp_repl import __version__

class Repl:
    def __init__(self):
        self.conn_mgr = ConnectionManager()
        self.scripts = {}  # 已加载脚本的命名空间
        self._loaded_files = {}  # 已加载的文件路径 -> 模块名
        self._running = True
        self._output_buffer = []  # 输出记录
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.session = PromptSession(history=FileHistory(str(HISTORY_FILE)))
        self._init_dirs()
    
    def _init_dirs(self):
        """初始化目录"""
        from pathlib import Path
        scripts_dir = Path(config.get("scripts_dir")).expanduser()
        lib_dir = Path(config.get("lib_dir")).expanduser()
        scripts_dir.mkdir(parents=True, exist_ok=True)
        lib_dir.mkdir(parents=True, exist_ok=True)
    
    def _autoload_libs(self):
        """静默加载 lib 目录下的模块"""
        from pathlib import Path
        import sys
        
        lib_dir = Path(config.get("lib_dir")).expanduser()
        if not lib_dir.exists():
            return
        
        # 添加到 sys.path
        lib_str = str(lib_dir)
        if lib_str not in sys.path:
            sys.path.insert(0, lib_str)
        
        # 加载所有 .py 文件
        for f in lib_dir.glob("*.py"):
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location(f.stem, f)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                # 导出函数
                for name in dir(module):
                    if not name.startswith("_"):
                        obj = getattr(module, name)
                        if callable(obj):
                            self.scripts[name] = obj
            except Exception as e:
                print(f"⚠ Failed to load lib/{f.name}: {e}")
        
        # 加载 autoload 配置的额外模块
        for path in config.get("autoload", []):
            try:
                p = Path(path).expanduser()
                if p.exists():
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(p.stem, p)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for name in dir(module):
                        if not name.startswith("_"):
                            obj = getattr(module, name)
                            if callable(obj):
                                self.scripts[name] = obj
            except Exception as e:
                print(f"⚠ Failed to autoload {path}: {e}")
    
    async def run(self):
        print(f"pw-repl v{__version__} - Type 'help' for commands")
        
        # 自动加载 lib
        self._autoload_libs()
        
        # 自动重连上次的连接
        last_url = config.get("last_connection")
        if last_url:
            try:
                await self.conn_mgr.connect(last_url)
                print(f"✓ Reconnected: {last_url}")
                if self.conn_mgr.page:
                    print(f"  Page: {self.conn_mgr.page.url}")
            except:
                print(f"⚠ Failed to reconnect: {last_url}")
        
        while self._running:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: self.session.prompt("pw> ")
                )
                if line.strip():
                    await self.execute(line.strip())
            except EOFError:
                break
            except KeyboardInterrupt:
                print()
                continue
        await self.conn_mgr.close_all()
    
    async def execute(self, line: str):
        start = time.time()
        # 记录命令
        self._output_buffer.append(f"pw> {line}")
        
        import io, sys
        old_stdout = sys.stdout
        sys.stdout = captured = io.StringIO()
        
        try:
            # import 语句
            if line.startswith("import ") or line.startswith("from "):
                exec(line, self.scripts)
                print(f"✓ {line}")
                return
            # await 开头 - 去掉 await 执行
            if line.startswith("await "):
                result = await self._exec_func(line[6:])
                self._ok(result, start)
            # Playwright 直接执行
            elif line.startswith(("page.", "browser.", "context.")):
                result = await self._exec_playwright(line)
                self._ok(result, start)
            # 赋值语句
            elif "=" in line and not line.startswith(("go ", "goto ")) and "==" not in line:
                await self._exec_assign(line)
            # 可能是函数调用（包括模块.函数）
            elif "(" in line and not line.startswith(("go ", "goto ", "click ", "fill ", "btn ", "txt ", "wait ", "run ")):
                result = await self._exec_func(line)
                self._ok(result, start)
            # 内置命令
            else:
                await self._exec_command(line)
        except Exception as e:
            self._err(e)
        finally:
            sys.stdout = old_stdout
            output = captured.getvalue()
            if output:
                print(output, end='')
                self._output_buffer.append(output.rstrip())
    
    async def _exec_playwright(self, code: str):
        ns = {"page": self.conn_mgr.page, "browser": self.conn_mgr.browser, "context": self.conn_mgr.context}
        result = eval(code, ns)
        if asyncio.iscoroutine(result):
            result = await result
        return result
    
    async def _exec_func(self, code: str):
        ns = {"page": self.conn_mgr.page, "browser": self.conn_mgr.browser, "context": self.conn_mgr.context}
        ns.update(self.scripts)
        result = eval(code, ns)
        if asyncio.iscoroutine(result):
            result = await result
        return result
    
    async def _exec_assign(self, code: str):
        ns = {"page": self.conn_mgr.page, "browser": self.conn_mgr.browser, "context": self.conn_mgr.context}
        ns.update(self.scripts)
        exec(code, ns)
        # 提取变量名并保存到 scripts
        var_name = code.split("=")[0].strip()
        if var_name in ns:
            self.scripts[var_name] = ns[var_name]
            print(f"✓ {var_name} = {repr(ns[var_name])[:50]}")
    
    async def _exec_command(self, line: str):
        parts = shlex.split(line)
        cmd, args = parts[0], parts[1:]
        handler = getattr(self, f"cmd_{cmd}", None)
        if handler:
            result = await handler(*args)
            return result
        else:
            print(f"✗ Unknown command: {cmd}")
    
    def _ok(self, result, start):
        elapsed = time.time() - start
        if result is not None:
            print(f"✓ {result} ({elapsed:.2f}s)")
        else:
            print(f"✓ ({elapsed:.2f}s)")
    
    def _err(self, e):
        print(f"✗ {type(e).__name__}: {e}")
    
    # === 连接命令 ===
    async def cmd_connect(self, url: str = None, name: str = None):
        url = url or config.get("cdp_url")
        conn = await self.conn_mgr.connect(url, name)
        config.set("last_connection", url)  # 保存用于下次自动重连
        print(f"✓ Connected: {conn.name} ({conn.url})")
        if conn.page:
            print(f"  Page: {conn.page.url}")
    
    async def cmd_launch(self, port: str = "9222", name: str = None):
        # 确保代理服务启动
        proxy = self._get_proxy()
        if not proxy._running:
            await proxy.start()
            print(f"✓ Proxy started on 127.0.0.1:{proxy.port}")
        
        conn = await self.conn_mgr.launch(int(port), name, proxy.port)
        print(f"✓ Launched: {conn.name} ({conn.url})")
    
    async def cmd_disconnect(self, name: str = None):
        await self.conn_mgr.disconnect(name)
        print("✓ Disconnected")
    
    async def cmd_connections(self):
        conns = self.conn_mgr.list()
        if not conns:
            print("No connections")
            return
        for name, url, active in conns:
            mark = "*" if active else " "
            print(f"  {mark} {name}  {url}")
    
    async def cmd_use(self, name: str):
        if self.conn_mgr.use(name):
            print(f"✓ Switched to: {name}")
        else:
            print(f"✗ Connection not found: {name}")
    
    async def cmd_status(self):
        conn = self.conn_mgr.current
        if conn:
            print(f"Connection: {conn.name} ({conn.url})")
            print(f"Page: {conn.page.url if conn.page else 'none'}")
        else:
            print("Not connected")
    
    # === 导航命令 ===
    async def cmd_url(self):
        if self.conn_mgr.page:
            print(self.conn_mgr.page.url)
    
    async def cmd_go(self, url: str):
        # 快捷平台
        shortcuts = {
            'kaggle': 'https://www.kaggle.com',
            'github': 'https://github.com',
            'google': 'https://www.google.com',
            'gmail': 'https://mail.google.com',
            'bing': 'https://www.bing.com',
            'baidu': 'https://www.baidu.com',
        }
        url = shortcuts.get(url.lower(), url)
        if not url.startswith(("http://", "https://", "file://")):
            url = "https://" + url
        await self.conn_mgr.page.goto(url)
        print(f"✓ {self.conn_mgr.page.url}")
    
    async def cmd_goto(self, url: str):
        await self.cmd_go(url)
    
    async def cmd_back(self):
        await self.conn_mgr.page.go_back()
        print(f"✓ {self.conn_mgr.page.url}")
    
    async def cmd_forward(self):
        await self.conn_mgr.page.go_forward()
        print(f"✓ {self.conn_mgr.page.url}")
    
    async def cmd_reload(self):
        await self.conn_mgr.page.reload()
        print("✓ Reloaded")
    
    # === 页面操作 ===
    async def cmd_click(self, selector: str):
        await self.conn_mgr.page.locator(selector).click()
        print("✓ Clicked")
    
    async def cmd_fill(self, selector: str, value: str):
        await self.conn_mgr.page.locator(selector).fill(value)
        print("✓ Filled")
    
    async def cmd_type(self, text: str):
        await self.conn_mgr.page.keyboard.type(text)
        print("✓ Typed")
    
    async def cmd_press(self, key: str):
        await self.conn_mgr.page.keyboard.press(key)
        print("✓ Pressed")
    
    async def cmd_btn(self, name: str):
        await self.conn_mgr.page.get_by_role("button", name=name).click()
        print("✓ Clicked")
    
    async def cmd_link(self, text: str):
        await self.conn_mgr.page.get_by_role("link", name=text).click()
        print("✓ Clicked")
    
    async def cmd_txt(self, text: str):
        await self.conn_mgr.page.get_by_text(text).click()
        print("✓ Clicked")
    
    async def cmd_input(self, label: str, value: str):
        await self.conn_mgr.page.get_by_label(label).fill(value)
        print("✓ Filled")
    
    async def cmd_wait(self, arg: str):
        if arg.isdigit():
            await asyncio.sleep(int(arg))
        else:
            await self.conn_mgr.page.wait_for_selector(arg)
        print("✓ Done")
    
    async def cmd_hover(self, selector: str):
        await self.conn_mgr.page.locator(selector).hover()
        print("✓ Hovered")
    
    # === 脚本执行 ===
    def _resolve_script_path(self, filepath: str) -> str:
        """解析脚本路径"""
        from pathlib import Path
        p = Path(filepath)
        # 绝对路径或 ./ 开头
        if p.is_absolute() or filepath.startswith("./"):
            return str(p.resolve())
        # 相对于 scripts_dir
        scripts_dir = Path(config.get("scripts_dir")).expanduser()
        full = scripts_dir / filepath
        if full.exists():
            return str(full)
        # 尝试原路径
        if p.exists():
            return str(p.resolve())
        return str(full)  # 返回 scripts_dir 下的路径（可能不存在，让后续报错）
    
    async def cmd_run(self, filepath: str):
        import sys
        import builtins
        from pathlib import Path
        
        # 解析路径
        resolved = self._resolve_script_path(filepath)
        
        # 添加脚本目录到 sys.path（支持相对导入）
        script_dir = str(Path(resolved).parent)
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        
        with open(resolved, 'r') as f:
            code = f.read()
        
        # 保存 self 引用给 debug 使用
        repl_self = self
        
        # debug 函数 - 进入交互模式
        class DebugBreak(Exception):
            pass
        
        def debug():
            builtins.print("🔴 Debug breakpoint - type 'c' to continue, 'q' to quit")
            sys.stdout.flush()
            while True:
                try:
                    line = input("(debug) pw> ")
                    if line.strip() == 'c' or line.strip() == 'continue':
                        break
                    if line.strip() == 'q' or line.strip() == 'quit':
                        raise DebugBreak("User quit")
                    # 执行命令
                    if line.strip():
                        try:
                            if line.startswith(("page.", "browser.", "context.")):
                                result = eval(line, ns)
                                if hasattr(result, '__await__'):
                                    import asyncio
                                    result = asyncio.get_event_loop().run_until_complete(result)
                                builtins.print(f"  {result}")
                            else:
                                result = eval(line, ns)
                                builtins.print(f"  {result}")
                        except SyntaxError:
                            exec(line, ns)
                        except Exception as e:
                            builtins.print(f"  ✗ {e}")
                        sys.stdout.flush()
                except EOFError:
                    break
        
        # 包装 print 确保立即输出
        original_print = builtins.print
        def flushed_print(*args, **kwargs):
            original_print(*args, **kwargs)
            sys.stdout.flush()
        
        ns = {
            "page": self.conn_mgr.page,
            "browser": self.conn_mgr.browser,
            "context": self.conn_mgr.context,
            "debug": debug,
            "print": flushed_print,
            "__builtins__": builtins,
        }
        
        # 检查是否有顶层 await
        if 'await ' in code and not code.strip().startswith('async def'):
            # 包装成 async 函数执行
            lines = code.split('\n')
            # 先处理 import 语句和函数/类定义
            imports = []
            defs = []
            body = []
            in_def = False
            def_indent = 0
            
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('import ') or stripped.startswith('from '):
                    imports.append(stripped)
                elif stripped.startswith('def ') or stripped.startswith('class ') or stripped.startswith('async def '):
                    in_def = True
                    def_indent = len(line) - len(line.lstrip())
                    defs.append(line)
                elif in_def:
                    curr_indent = len(line) - len(line.lstrip()) if line.strip() else def_indent + 1
                    if curr_indent > def_indent or not line.strip():
                        defs.append(line)
                    else:
                        in_def = False
                        body.append(f"    {line}")
                else:
                    body.append(f"    {line}")
            
            # import 和函数定义放在外面
            for imp in imports:
                exec(imp, ns)
            if defs:
                exec('\n'.join(defs), ns)
            
            wrapped = "async def __run__():\n" + '\n'.join(body)
            wrapped += "\n__result__ = __run__()"
            
            exec(wrapped, ns)
            await ns["__result__"]
            
            # 导出函数到 scripts
            for name, obj in ns.items():
                if callable(obj) and not name.startswith('_') and name not in ('debug', 'print'):
                    self.scripts[name] = obj
            
            funcs = [n for n in self.scripts.keys() if not n.startswith('__')]
            print(f"✓ Executed: {resolved}")
            if funcs:
                print(f"  Functions: {', '.join(funcs)}")
            sys.stdout.flush()
        else:
            # 原有逻辑：加载模块并导出函数
            import importlib.util
            spec = importlib.util.spec_from_file_location("script", filepath)
            module = importlib.util.module_from_spec(spec)
            module.page = self.conn_mgr.page
            module.browser = self.conn_mgr.browser
            module.context = self.conn_mgr.context
            module.debug = debug
            spec.loader.exec_module(module)
            for name in dir(module):
                if not name.startswith("_"):
                    obj = getattr(module, name)
                    if callable(obj):
                        self.scripts[name] = obj
            funcs = [n for n in self.scripts.keys()]
            print(f"✓ Loaded: {resolved}")
            if funcs:
                print(f"  Functions: {', '.join(funcs)}")
            sys.stdout.flush()
    
    async def cmd_funcs(self):
        if not self.scripts:
            print("No functions loaded")
            return
        for name, func in self.scripts.items():
            print(f"  {name}")
    
    # === 截图 ===
    async def cmd_shot(self, name: str = None):
        if name is None:
            name = f"screenshot_{int(time.time())}.png"
        elif not name.endswith(('.png', '.jpg', '.jpeg')):
            name = f"{name}.png"
        await self.conn_mgr.page.screenshot(path=name)
        print(f"✓ Saved: {name}")
    
    # === 多 Tab 管理 ===
    async def cmd_pages(self):
        if not self.conn_mgr.page:
            print("Not connected")
            return
        # 用 CDP 获取 targets
        try:
            cdp = await self.conn_mgr.context.new_cdp_session(self.conn_mgr.page)
            result = await cdp.send("Target.getTargets")
            targets = [t for t in result.get("targetInfos", []) if t.get("type") == "page"]
            current_page = self.conn_mgr.page
            for i, t in enumerate(targets):
                # 通过匹配 playwright pages 找到对应的 page 对象
                is_current = False
                for p in self.conn_mgr.context.pages:
                    if p.url == t["url"] and p == current_page:
                        is_current = True
                        break
                mark = "*" if is_current else " "
                url = t["url"][:60] if len(t["url"]) > 60 else t["url"]
                print(f"  {mark} [{i}] {url}")
            self._targets = targets
        except Exception as e:
            # fallback 到 Playwright
            pages = self.conn_mgr.get_pages()
            for i, url, active in pages:
                mark = "*" if active else " "
                print(f"  {mark} [{i}] {url}")
    
    async def cmd_page(self, index: str = None):
        if not self.conn_mgr.page:
            print("Not connected")
            return
        if index is None:
            # 无参数时显示当前 page 信息
            print(f"Current: {self.conn_mgr.page.url}")
            return
        idx = int(index)
        # 只切换内部 page 对象，不激活浏览器 tab
        if hasattr(self, '_targets') and idx < len(self._targets):
            target = self._targets[idx]
            for p in self.conn_mgr.context.pages:
                if p.url == target["url"]:
                    self.conn_mgr.current.page = p
                    print(f"✓ Switched to [{index}] {target['url'][:60]}")
                    return
        # fallback
        if self.conn_mgr.set_page(idx):
            print(f"✓ Switched to [{index}] {self.conn_mgr.page.url[:60]}")
        else:
            print(f"✗ Invalid page index: {index}")
    
    async def cmd_front(self):
        """Bring current page to front"""
        await self.conn_mgr.page.bring_to_front()
        print("✓ Brought to front")
    
    # === 历史 ===
    async def cmd_history(self, pattern: str = None):
        items = list(self.session.history.get_strings())
        
        # 去重，保留最后出现的位置
        seen = {}
        for i, cmd in enumerate(items):
            seen[cmd] = i
        unique = sorted(seen.keys(), key=lambda x: seen[x])
        
        if pattern and not pattern.isdigit():
            unique = [c for c in unique if pattern in c]
            unique = unique[-20:]
        elif pattern and pattern.isdigit():
            unique = unique[-int(pattern):]
        else:
            unique = unique[-20:]
        
        self._history_items = unique
        for i, cmd in enumerate(unique, 1):
            print(f"  {i}. {cmd}")
    
    async def cmd_r(self, index: str):
        """执行历史命令"""
        if not hasattr(self, '_history_items') or not self._history_items:
            await self.cmd_history()
        idx = int(index) - 1
        if 0 <= idx < len(self._history_items):
            cmd = self._history_items[idx]
            print(f"> {cmd}")
            await self.execute(cmd)
        else:
            print(f"✗ Invalid index: {index}")
    
    # === 导出 ===
    async def cmd_export(self, target: str = "gist", count: str = "20"):
        """导出输出到文件或 gist
        
        用法:
            export gist [N]        - 导出到默认 gist
            export gist:name [N]   - 导出到指定名字的 gist
            export /path/file [N]  - 导出到本地文件
        """
        n = int(count)
        content = '\n'.join(self._output_buffer[-n:])
        
        if target.startswith('/') or target.startswith('./'):
            # 本地文件
            with open(target, 'w') as f:
                f.write(content)
            print(f"✓ Exported to {target}")
        elif target.startswith('gist'):
            # gist
            name = 'default'
            if ':' in target:
                name = target.split(':')[1]
            await self._export_gist(name, content)
    
    async def _export_gist(self, name: str, content: str):
        import urllib.request
        import json
        
        token = config.get('gist_token')
        if not token:
            print("✗ 需要设置 gist_token: config gist_token ghp_xxx")
            return
        
        gists = config.get('gists') or {}
        gist_id = gists.get(name)
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json',
        }
        
        data = {
            'files': {'pw-repl.log': {'content': content}},
            'public': False,
        }
        
        if gist_id:
            # 更新
            url = f'https://api.github.com/gists/{gist_id}'
            req = urllib.request.Request(url, json.dumps(data).encode(), headers, method='PATCH')
        else:
            # 创建
            data['description'] = f'pw-repl export: {name}'
            url = 'https://api.github.com/gists'
            req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
                if not gist_id:
                    gists[name] = result['id']
                    config.set('gists', gists)
                print(f"✓ Exported to gist:{name}")
                print(f"  {result['html_url']}")
        except Exception as e:
            print(f"✗ Gist 失败: {e}")
    
    # === 帮助 ===
    async def cmd_help(self, cmd: str = None):
        import sys
        if cmd:
            handler = getattr(self, f"cmd_{cmd}", None)
            if handler and handler.__doc__:
                print(handler.__doc__)
            else:
                print(f"No help for: {cmd}")
            return
        print("""Commands:
  connect [url] [name]  - Connect to CDP
  launch [port] [name]  - Launch browser
  disconnect [name]     - Disconnect
  connections           - List connections
  use <name>            - Switch connection
  status                - Show status

  url                   - Show current URL
  go <url>              - Navigate (auto adds https://)
  back/forward/reload   - Navigation
  pages                 - List all tabs
  page [index]          - Show/switch tab

  click <selector>      - Click element
  fill <sel> <val>      - Fill input
  btn <name>            - Click button by name
  txt <text>            - Click by text
  wait <sec|selector>   - Wait

  run <file>            - Load and execute script
  funcs                 - List loaded functions
  shot [name]           - Screenshot
  history [n|pattern]   - Show history
  r <index>             - Run history command

  sessions [platform]  - List available sessions
  session [index|id]  - Load/show session
  save                - Save session to s-mgr
  cookies [export|import] [file] - Manage cookies
  clear               - Clear session

  config                - Show config
  config <key> <val>    - Set config
  page.xxx              - Execute Playwright code
  help [cmd]            - Show help""")
        sys.stdout.flush()
    
    # === 会话管理 ===
    def _get_smgr(self):
        from mp_repl.smgr import SessionManagerClient, PlaywrightHelper
        url = config.get("smgr_url")
        key = config.get("smgr_key")
        if not url:
            return None, None
        client = SessionManagerClient(url, key)
        helper = PlaywrightHelper(client)
        return client, helper
    
    async def cmd_sessions(self, platform: str = None):
        """列出可用会话"""
        client, _ = self._get_smgr()
        if not client:
            print("✗ smgr_url not configured")
            return
        
        # 自动检测平台：从 s-mgr 获取 domains 匹配当前 URL
        if platform is None and self.conn_mgr.page:
            url = self.conn_mgr.page.url.lower()
            try:
                all_accounts = client.list_accounts()
                for acc in all_accounts:
                    domains = acc.get('domains', [])
                    for domain in domains:
                        if domain.lstrip('.') in url:
                            platform = acc.get('platform')
                            break
                    if platform:
                        break
            except:
                pass
        
        try:
            accounts = client.list_accounts(platform)
            if not accounts:
                print(f"No sessions found" + (f" for {platform}" if platform else ""))
                return
            self._sessions = accounts
            for i, acc in enumerate(accounts):
                print(f"  [{i}] {acc.get('platform', '?')}/{acc.get('username', '?')}")
        except Exception as e:
            print(f"✗ {e}")
    
    async def cmd_session(self, index_or_id: str = None):
        """加载/显示会话"""
        if index_or_id is None:
            if hasattr(self, '_current_session'):
                print(f"Current: {self._current_session}")
            else:
                print("No session loaded")
            return
        
        client, helper = self._get_smgr()
        if not client:
            print("✗ smgr_url not configured")
            return
        
        # 支持索引或 ID
        account_id = None
        account_name = index_or_id
        if index_or_id.isdigit() and hasattr(self, '_sessions'):
            idx = int(index_or_id)
            if idx < len(self._sessions):
                account_id = self._sessions[idx].get('id')
                account_name = f"{self._sessions[idx].get('platform')}/{self._sessions[idx].get('username')}"
        else:
            account_id = index_or_id
        
        if not account_id:
            print(f"✗ Invalid session: {index_or_id}")
            return
        
        try:
            # 使用 SDK 切换会话
            current_id = getattr(self, '_current_account_id', None)
            success = await helper.switch_session(
                self.conn_mgr.context,
                account_id,
                save_current=False,
                current_account_id=current_id
            )
            
            if success:
                self._current_session = account_name
                self._current_account_id = account_id
                print(f"✓ Session loaded: {account_name}")
                await self.conn_mgr.page.reload()
                print(f"✓ Page reloaded")
            else:
                print(f"✗ No session data for: {account_name}")
        except Exception as e:
            print(f"✗ {e}")
    
    async def cmd_save(self, username: str = None):
        """保存当前会话到 s-mgr
        
        用法:
            save              - 保存到当前账号
            save <username>   - 保存到当前平台的指定账号（不存在则创建）
        """
        client, helper = self._get_smgr()
        if not client:
            print("✗ smgr_url not configured")
            return
        
        # 从 s-mgr 获取 domains 匹配当前平台
        current_url = self.conn_mgr.page.url.lower()
        platform = None
        try:
            all_accounts = client.list_accounts()
            for acc in all_accounts:
                domains = acc.get('domains', [])
                for domain in domains:
                    if domain.lstrip('.') in current_url:
                        platform = acc.get('platform')
                        break
                if platform:
                    break
        except:
            pass
        
        # 未知平台，从域名提取并确认
        if not platform:
            detected = current_url.split('/')[2].replace('www.', '').split('.')[0]
            confirm = input(f"检测到新平台: {detected}，确认或输入平台名 (n取消): ").strip()
            if confirm.lower() == 'n':
                print("✗ Cancelled")
                return
            platform = confirm if confirm else detected
        
        account_id = None
        
        if username:
            # 查找或创建账号
            accounts = client.list_accounts(platform)
            for acc in accounts:
                if acc.get('username') == username:
                    account_id = acc['id']
                    break
            
            if not account_id:
                try:
                    domain = self.conn_mgr.page.url.split('/')[2]
                    acc = client.create_account(platform, username, domains=[domain])
                    account_id = acc['id']
                    print(f"✓ Created: {platform}/{username}")
                except Exception as e:
                    print(f"✗ Failed to create account: {e}")
                    return
        else:
            if not hasattr(self, '_current_account_id'):
                print(f"✗ Usage: save <username>")
                return
            account_id = self._current_account_id
        
        try:
            await helper.save_session(self.conn_mgr.page, account_id)
            print(f"✓ Session saved")
        except Exception as e:
            print(f"✗ {e}")
    
    async def cmd_cookies(self, action: str = "show", filepath: str = None):
        """cookies export/import/show"""
        import json
        if action == "export":
            cookies = await self.conn_mgr.context.cookies()
            filepath = filepath or f"cookies_{int(time.time())}.json"
            with open(filepath, 'w') as f:
                json.dump(cookies, f, indent=2)
            print(f"✓ Exported {len(cookies)} cookies to {filepath}")
        elif action == "import":
            if not filepath:
                print("✗ Usage: cookies import <file>")
                return
            with open(filepath) as f:
                cookies = json.load(f)
            await self.conn_mgr.context.add_cookies(cookies)
            print(f"✓ Imported {len(cookies)} cookies")
        else:
            cookies = await self.conn_mgr.context.cookies()
            for c in cookies[:10]:
                print(f"  {c.get('name')}: {str(c.get('value'))[:30]}...")
            if len(cookies) > 10:
                print(f"  ... and {len(cookies) - 10} more")
    
    async def cmd_clear(self, flag: str = None):
        """清理会话数据
        
        用法:
            clear       - 清理当前页面的会话
            clear --all - 清理所有会话
        """
        domain = self.conn_mgr.page.url.split('/')[2]
        
        if flag == '--all':
            confirm = input("清理所有会话数据? (y/n): ").strip().lower()
            if confirm != 'y':
                print("✗ Cancelled")
                return
            await self.conn_mgr.context.clear_cookies()
            await self.conn_mgr.page.evaluate("localStorage.clear()")
            print("✓ Cleared all")
        else:
            confirm = input(f"清理当前页面 ({domain}) 的会话数据? (y/n): ").strip().lower()
            if confirm != 'y':
                print("✗ Cancelled")
                return
            # 只清理当前域名的 cookies
            cookies = await self.conn_mgr.context.cookies()
            for c in cookies:
                if domain in c.get('domain', ''):
                    await self.conn_mgr.context.clear_cookies(name=c['name'], domain=c['domain'])
            await self.conn_mgr.page.evaluate("localStorage.clear()")
            print(f"✓ Cleared ({domain})")
    
    # === 代理 ===
    def _get_proxy(self):
        if not hasattr(self, '_proxy'):
            from mp_repl.proxy import LocalProxy
            self._proxy = LocalProxy()
        return self._proxy
    
    async def cmd_proxy(self, *args):
        """代理管理
        
        用法:
            proxy                    - 显示当前状态
            proxy off                - 直连（关闭代理）
            proxy <url>              - 设置全局代理
            proxy <region>           - 设置区域代理（从 s-mgr 获取）
            proxy <platform> <url>   - 设置平台特定代理
            proxy <platform> off     - 平台直连
            proxy list               - 列出可用代理
        """
        proxy = self._get_proxy()
        
        if len(args) == 0:
            # 显示状态
            status = "running" if proxy._running else "stopped"
            print(f"  Status: {status}")
            print(f"  Port: {proxy.port}")
            print(f"  Upstream: {proxy.upstream or 'direct'}")
            if proxy.platform_rules:
                print(f"  Platform rules:")
                for k, v in proxy.platform_rules.items():
                    print(f"    {k}: {v}")
            return
        
        if args[0] == 'list':
            # 从 s-mgr 获取代理列表
            client, _ = self._get_smgr()
            if not client:
                print("✗ smgr_url not configured")
                return
            try:
                region = args[1].upper() if len(args) > 1 else None
                proxies = client._request('GET', '/proxies')['data']
                if region:
                    proxies = [p for p in proxies if p.get('region', '').upper() == region]
                for i, p in enumerate(proxies):
                    cfg = p.get('config', {})
                    print(f"  [{i}] {p.get('region', '?')}: {cfg.get('protocol', 'http')}://{cfg.get('host')}:{cfg.get('port')}")
            except Exception as e:
                print(f"✗ {e}")
            return
        
        if args[0] == 'off':
            proxy.set_upstream(None)
            print("✓ Direct connection")
            return
        
        if args[0] == 'start':
            if not proxy._running:
                await proxy.start()
                print(f"✓ Proxy started on 127.0.0.1:{proxy.port}")
            else:
                print(f"✓ Proxy already running on 127.0.0.1:{proxy.port}")
            return
        
        if args[0] == 'stop':
            if proxy._running:
                await proxy.stop()
                print("✓ Proxy stopped")
            else:
                print("✓ Proxy not running")
            return
        
        if len(args) == 1:
            # proxy <url> 或 proxy <region> 或 proxy <region:index>
            arg = args[0]
            if '://' in arg:
                # URL
                proxy.set_upstream(arg)
                print(f"✓ Upstream: {arg}")
            else:
                # :index 或 region 或 region:index
                region = arg
                index = None
                if ':' in arg:
                    region, idx_str = arg.rsplit(':', 1)
                    if idx_str.isdigit():
                        index = int(idx_str)
                
                client, _ = self._get_smgr()
                if client:
                    try:
                        proxies = client._request('GET', '/proxies')['data']
                        # :index 表示全局索引，不过滤 region
                        if region:
                            proxies = [p for p in proxies if p.get('region', '').upper() == region.upper()]
                        if proxies:
                            import random
                            p = proxies[index] if index is not None else random.choice(proxies)
                            cfg = p.get('config', {})
                            url = f"{cfg.get('protocol', 'http')}://{cfg.get('host')}:{cfg.get('port')}"
                            proxy.set_upstream(url)
                            label = region if region else 'all'
                            print(f"✓ Upstream: {url} ({label})")
                        else:
                            print(f"✗ No proxy found for region: {region}")
                    except IndexError:
                        print(f"✗ Invalid index: {index}")
                    except Exception as e:
                        print(f"✗ {e}")
                else:
                    print(f"✗ smgr_url not configured")
            return
        
        if len(args) == 2:
            # proxy <platform> <url|off|region[:index]>
            platform, value = args
            if value == 'off':
                proxy.set_platform_proxy(platform, None)
                print(f"✓ {platform}: direct")
            elif '://' in value:
                proxy.set_platform_proxy(platform, value)
                print(f"✓ {platform}: {value}")
            else:
                # region[:index]
                region = value
                index = None
                if ':' in value:
                    region, idx_str = value.rsplit(':', 1)
                    if idx_str.isdigit():
                        index = int(idx_str)
                
                client, _ = self._get_smgr()
                if client:
                    try:
                        proxies = client._request('GET', '/proxies')['data']
                        proxies = [p for p in proxies if p.get('region', '').upper() == region.upper()]
                        if proxies:
                            import random
                            p = proxies[index] if index is not None else random.choice(proxies)
                            cfg = p.get('config', {})
                            url = f"{cfg.get('protocol', 'http')}://{cfg.get('host')}:{cfg.get('port')}"
                            proxy.set_platform_proxy(platform, url)
                            print(f"✓ {platform}: {url} ({region})")
                        else:
                            print(f"✗ No proxy found for region: {region}")
                    except IndexError:
                        print(f"✗ Invalid index: {index}")
                    except Exception as e:
                        print(f"✗ {e}")
                else:
                    print(f"✗ smgr_url not configured")
            return
    
    async def cmd_config(self, key: str = None, value: str = None):
        """查看/设置配置"""
        if key is None:
            for k, v in config.all().items():
                print(f"  {k}: {v}")
        elif value is None:
            v = config.get(key)
            if key == 'gists' and isinstance(v, dict):
                for name, gid in v.items():
                    print(f"  {name}: https://gist.github.com/{gid}")
            else:
                print(f"  {key}: {v}")
        else:
            config.set(key, value)
            print(f"✓ {key} = {value}")
    
    async def cmd_exit(self):
        self._running = False
    
    async def cmd_quit(self):
        self._running = False
