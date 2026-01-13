# mp-repl

Playwright 交互式调试工具 - 提升自动化脚本开发效率

## 安装

```bash
pip install mp-repl
playwright install chromium
```

## 快速开始

```bash
# 启动 REPL（自动重连上次的浏览器）
pw-repl

# 连接浏览器
pw> connect 127.0.0.1:9222

# 快捷导航
pw> go github
pw> go kaggle

# 页面操作
pw> btn 'Sign in'
pw> fill '#email' 'test@example.com'
pw> click '#submit'

# 执行 Playwright 代码
pw> page.locator('button').click()
pw> await page.title()

# 变量赋值
pw> mypage = page
pw> title = await page.title()

# 加载并执行脚本
pw> run my_script.py
pw> my_function()
```

## 会话管理

```bash
# 列出会话（自动检测当前平台）
pw> sessions
  [0] github/user1
  [1] github/user2

# 加载会话
pw> session 0
✓ Session loaded: github/user1
✓ Page reloaded

# 保存会话
pw> save myuser
✓ Created: github/myuser
✓ Session saved

# 清理会话
pw> clear           # 当前页面
pw> clear --all     # 所有
```

## 主要功能

- 快捷导航：`go kaggle`, `go github`, `go google`
- 页面操作：`btn`, `click`, `fill`, `txt`, `wait`
- Playwright 执行：`page.xxx`, `browser.xxx`
- 脚本执行：`run`, `funcs`, 支持 debug() 断点
- 多 Tab 管理：`pages`, `page <index>`
- 会话管理：`sessions`, `session`, `save`, `clear`
- 历史记录：`history`, `r <index>`

## 文档

详见 [docs/design.md](docs/design.md)

## License

MIT
