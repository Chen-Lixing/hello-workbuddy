"""hello-workbuddy —— 可运行的最小 Python 骨架。

用法：
    python main.py                         # 打印问候
    python main.py -n 张三                  # 指定问候对象
    python main.py -r github/github-mcp-server   # 查询公开仓库并打印摘要
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

API = "https://api.github.com"


def greet(name: str = "WorkBuddy") -> str:
    """返回一句问候语。"""
    return f"Hello, {name}!"


def fetch_repo(slug: str, timeout: float = 10.0) -> dict[str, Any]:
    """查询公开仓库的摘要信息。

    依赖 requests，采用延迟导入：不查仓库时无需安装依赖也能跑。
    """
    import requests  # noqa: PLC0415 - 故意延迟导入

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "hello-workbuddy",
    }
    # 可选：设置 GITHUB_TOKEN 环境变量可提升 API 限额（CI 环境自动生效）
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(
        f"{API}/repos/{slug}",
        headers=headers,
        timeout=timeout,
    )
    resp.raise_for_status()
    data = resp.json()
    return {
        "full_name": data["full_name"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "language": data.get("language"),
        "description": data.get("description"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hello-workbuddy",
        description="最小 Python 骨架演示",
    )
    parser.add_argument("-n", "--name", default="WorkBuddy", help="问候对象")
    parser.add_argument("-r", "--repo", metavar="OWNER/NAME", help="查询公开仓库信息")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(greet(args.name))

    if not args.repo:
        return 0

    try:
        info = fetch_repo(args.repo)
    except ImportError:
        print("缺少依赖，请先执行：pip install -r requirements.txt", file=sys.stderr)
        return 2
    except Exception as exc:  # 网络、404、限流等统一处理
        print(f"查询失败：{exc}", file=sys.stderr)
        return 1

    print(json.dumps(info, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
