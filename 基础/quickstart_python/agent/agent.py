"""Agent 定义模块 — 创建绑定模型与工具的 LlmAgent"""

from trpc_agent_sdk.agents import LlmAgent
from trpc_agent_sdk.models import LLMModel, OpenAIModel
from trpc_agent_sdk.tools import FunctionTool

from .config import get_model_config
from .prompts import INSTRUCTION
from .tools import get_weather, calculate, get_current_time


def _create_model() -> LLMModel:
    """基于环境变量创建 OpenAI 兼容模型实例"""
    api_key, base_url, model_name = get_model_config()
    return OpenAIModel(model_name=model_name, api_key=api_key, base_url=base_url)


def create_agent() -> LlmAgent:
    """创建根 Agent

    - 绑定 3 个工具：天气查询 / 数学计算 / 时间查询
    - 使用 OpenAI 兼容接口，支持混元 / DeepSeek / GPT 等模型
    """
    return LlmAgent(
        name="assistant",
        description="支持天气查询、数学计算、时间查询的多功能助手",
        model=_create_model(),
        instruction=INSTRUCTION,
        tools=[
            FunctionTool(get_weather),
            FunctionTool(calculate),
            FunctionTool(get_current_time),
        ],
    )


# 模块级实例，供 Runner 直接引用
root_agent = create_agent()
