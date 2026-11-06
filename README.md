# hello-workbuddy

第一个通过 **WorkBuddy** 创建的仓库。

## 这个仓库是做什么的

没有业务代码，它的唯一任务是把「AI 助手 → GitHub」这条链路跑通，并留下证据。

建库过程由 WorkBuddy 通过 GitHub MCP 服务 `github-pat` 完成：

| 步骤 | 调用 | 结果 |
|---|---|---|
| 1 | `create_repository` | 创建公开仓库 `Chen-Lixing/hello-workbuddy` |
| 2 | `create_or_update_file` | 写入本 README，形成首个提交 |

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

## 接下来

拿它当试验田：建分支、提 PR、跑 Actions，怎么折腾都行。

## 更新日志

- 2026-11-05 创建仓库，写入 README（提交 `40a9020`）
- 2026-11-06 通过 PR 流程追加本节（分支 `docs/add-changelog`）
