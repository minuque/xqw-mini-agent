"""Agent 核心逻辑"""

import re
from collections.abc import Callable

from .llm_client import LLMClient
from .prompts import AGENT_SYSTEM_PROMPT


class Agent:
    """ReAct 模式的 Agent"""

    def __init__(
        self, llm: LLMClient, tools: dict[str, Callable], max_iterations: int = 5
    ):
        self.llm = llm
        self.tools = tools
        self.max_iterations = max_iterations

    def run(self, user_prompt: str) -> str:
        """运行 Agent 处理用户请求"""
        prompt_history = [f"用户请求: {user_prompt}"]
        print(f"用户输入: {user_prompt}\n" + "=" * 40)

        for i in range(self.max_iterations):
            print(f"--- 循环 {i + 1} ---\n")

            # 调用 LLM
            full_prompt = "\n".join(prompt_history)
            llm_output = self.llm.generate(full_prompt, AGENT_SYSTEM_PROMPT)

            # 截断多余的 Thought-Action
            llm_output = self._truncate_output(llm_output)
            print(f"模型输出:\n{llm_output}\n")
            prompt_history.append(llm_output)

            # 解析 Action
            action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
            if not action_match:
                observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
                observation_str = f"Observation: {observation}"
                print(f"{observation_str}\n" + "=" * 40)
                prompt_history.append(observation_str)
                continue

            action_str = action_match.group(1).strip()

            # 检查是否结束
            if action_str.startswith("Finish"):
                finish_match = re.match(r"Finish\[(.*)\]", action_str)
                if finish_match:
                    final_answer = finish_match.group(1)
                    print(f"任务完成，最终答案: {final_answer}")
                    return final_answer
                return "错误: Finish 格式不正确"

            # 执行工具
            observation = self._execute_tool(action_str)
            observation_str = f"Observation: {observation}"
            print(f"{observation_str}\n" + "=" * 40)
            prompt_history.append(observation_str)

        return "已达到最大循环次数，任务未完成。"

    def _truncate_output(self, llm_output: str) -> str:
        """截断多余的 Thought-Action 对"""
        match = re.search(
            r"(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)",
            llm_output,
            re.DOTALL,
        )
        if match:
            truncated = match.group(1).strip()
            if truncated != llm_output.strip():
                llm_output = truncated
                print("已截断多余的 Thought-Action 对")
        return llm_output

    def _execute_tool(self, action_str: str) -> str:
        """解析并执行工具调用"""
        tool_match = re.search(r"(\w+)\(", action_str)
        args_match = re.search(r"\((.*)\)", action_str)
        if not tool_match or not args_match:
            return "错误: Action 格式不正确"

        tool_name = tool_match.group(1)
        args_str = args_match.group(1)
        kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

        if tool_name in self.tools:
            return self.tools[tool_name](**kwargs)
        return f"错误:未定义的工具 '{tool_name}'"
