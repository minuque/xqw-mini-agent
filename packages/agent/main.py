"""入口脚本"""

from packages.agent.agent import Agent
from packages.agent.config import API_KEY, BASE_URL, MODEL_ID, setup_env
from packages.agent.llm_client import LLMClient
from packages.agent.tools import get_attraction, get_weather


def main():
    # 初始化
    setup_env()
    llm = LLMClient(model=MODEL_ID, api_key=API_KEY, base_url=BASE_URL)

    tools = {
        "get_weather": get_weather,
        "get_attraction": get_attraction,
    }

    agent = Agent(llm=llm, tools=tools)

    # 运行
    user_prompt = (
        "你好，请帮我查询一下今天南京的天气，然后根据天气推荐一个合适的旅游景点。"
    )
    agent.run(user_prompt)


# uv run python -m packages.agent.main
if __name__ == "__main__":
    main()
