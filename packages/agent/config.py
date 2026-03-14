"""配置管理模块"""

import os

# LLM 配置
API_KEY = "sk-sp-c1bd5e0edf8b48f6a560ac2953c7e231"
BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"
MODEL_ID = "qwen3-max-2026-01-23"

# Tavily API 配置
TAVILY_API_KEY = "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"

# Agent 配置
MAX_ITERATIONS = 5  # 最大循环次数


def setup_env():
    """设置环境变量"""
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
