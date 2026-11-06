# hello-workbuddy

第一个通过 **WorkBuddy** 创建的仓库。

## 这个仓库是做什么的

一半是连接验证，一半是可用的 Python 骨架：既能证明「AI 助手 → GitHub」这条链路通畅，也能当你下一个脚本的起点。

建库过程由 WorkBuddy 通过 GitHub MCP 服务 `github-pat` 完成：

| 步骤 | 调用 | 结果 |
|---|---|---|
| 1 | `create_repository` | 创建公开仓库 `Chen-Lixing/hello-workbuddy` |
| 2 | `create_or_update_file` | 写入本 README，形成首个提交 |
| 3 | `push_files` | 一次性提交 `main.py`、`requirements.txt`、`.gitignore` |

## 如何运行

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python main.py                        # 打印问候
python main.py -n 张三                 # 指定问候对象
python main.py -r github/github-mcp-server   # 查询公开仓库并打印摘要
```

最后一个例子会真的访问 GitHub 公开 API，输出仓库的 star、fork、语言等信息；没网或限流时会打印错误并以退出码 1 结束。

## 连接方式

不走 WorkBuddy 官方 OAuth 连接器，改用 Personal Access Token 直连 GitHub 官方 MCP 端点：

```json
{
  "mcpServers": {
    "github-pat": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": { "Authorization": "Bearer <你的 PAT>" }
    }
  }
}
```

几点经验，留给自己以后看：

- 桌面端**不会**展开 `${GITHUB_PAT}` 这类占位符，占位符会被原样发出去，GitHub 返回 400，界面上表现为 `SSE error: Non-200 status code (400)`。必须内联真实 token。
- 这个端点只接受 POST（streamable HTTP），`type` 要写 `http`；配成 `sse` 会固定拿到 405。
- Token 有有效期，到期前用本地脚本换掉即可，不用重新授权。

## 接下来可以做什么

- 接入 `pytest`，给 `greet()` 和 `fetch_repo()` 补单测
- 加 GitHub Actions：push 时自动跑 lint 和测试（需要在 MCP 里开启 Actions 工具集，或直接在网页上添加）
- 把这里的 PAT 连接方式复制到你自己的项目

## 更新日志

- 2026-11-05 创建仓库，写入 README（提交 `40a9020`）
- 2026-11-06 通过 PR 流程追加「更新日志」一节（PR #1，squash 合入 `f63f147`）
- 2026-11-06 加入 Python 骨架：`main.py` + `requirements.txt` + `.gitignore`，README 补「如何运行」
