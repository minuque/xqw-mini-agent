# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

xqw-mini-agent 是一个 Python Agent 项目。

## 开发环境

- Python 版本：3.12
- 包管理器：uv（项目使用 uv.lock 进行依赖锁定）

## 常用命令

```bash
# 安装依赖
uv sync

# 运行项目
uv run python main.py

# 添加新依赖
uv add <package-name>

# 添加开发依赖
uv add --dev <package-name>
```

## Obsidian 规则

操作 `notes/` 或 `.md` 文件时使用 `obsidian:obsidian-markdown` skill
