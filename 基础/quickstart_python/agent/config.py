"""模型配置模块 — 从环境变量读取 LLM 配置"""

import os


def get_model_config() -> tuple[str, str, str]:
    """从环境变量获取模型配置

    Returns:
        (api_key, base_url, model_name) 三元组
    """
    api_key = os.getenv("TRPC_AGENT_API_KEY", "")
    base_url = os.getenv("TRPC_AGENT_BASE_URL", "")
    model_name = os.getenv("TRPC_AGENT_MODEL_NAME", "")

    missing = [
        name
        for name, val in [
            ("TRPC_AGENT_API_KEY", api_key),
            ("TRPC_AGENT_BASE_URL", base_url),
            ("TRPC_AGENT_MODEL_NAME", model_name),
        ]
        if not val
    ]
    if missing:
        raise ValueError(
            f"缺少必要的环境变量: {', '.join(missing)}。"
            "请在 .env 文件或系统环境中设置。"
        )

    return api_key, base_url, model_name
