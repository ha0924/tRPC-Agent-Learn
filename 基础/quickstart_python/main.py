"""
tRPC-Agent Quickstart — 多轮对话 + 流式输出

用法:
    1. 复制 .env.example 为 .env，填入模型配置
    2. pip install -r requirements.txt
    3. python main.py

支持的命令:
    /exit  退出对话
    /clear 清空当前会话，开启新对话
"""

import asyncio
import uuid

from dotenv import load_dotenv
from trpc_agent_sdk.runners import Runner
from trpc_agent_sdk.sessions import InMemorySessionService
from trpc_agent_sdk.types import Content, Part

# 加载 .env 中的环境变量（API Key 等）
load_dotenv()


async def run_conversation():
    """多轮对话主循环"""

    # ── 1. 延迟导入 Agent（确保 .env 已加载） ──
    from agent.agent import root_agent

    # ── 2. 初始化 Session 服务和 Runner ──
    app_name = "quickstart_demo"
    session_service = InMemorySessionService()
    runner = Runner(
        app_name=app_name,
        agent=root_agent,
        session_service=session_service,
    )

    # ── 3. 会话配置 ──
    user_id = "demo_user"
    session_id = str(uuid.uuid4())

    # 创建带初始状态的 Session
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state={"user_name": user_id},
    )

    # ── 4. 交互循环 ──
    print("=" * 50)
    print("  tRPC-Agent Quickstart 多轮对话")
    print("  输入 /exit 退出 | /clear 清空会话")
    print("=" * 50)

    while True:
        # 读取用户输入
        try:
            user_input = input("\n👤 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 再见！")
            break

        if not user_input:
            continue

        # 处理命令
        if user_input == "/exit":
            print("👋 再见！")
            break

        if user_input == "/clear":
            session_id = str(uuid.uuid4())
            await session_service.create_session(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id,
                state={"user_name": user_id},
            )
            print("🔄 会话已清空，开始新对话。")
            continue

        # ── 5. 构造消息并流式执行 ──
        user_content = Content(parts=[Part.from_text(text=user_input)])

        print("🤖 Assistant: ", end="", flush=True)

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content,
        ):
            if not event.content or not event.content.parts:
                continue

            # 流式文本输出（打字机效果）
            if event.partial:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end="", flush=True)
                continue

            # 非流式事件：工具调用 / 工具结果 / 思考过程
            for part in event.content.parts:
                if part.thought:
                    # 跳过模型内部思考
                    continue
                if part.function_call:
                    print(
                        f"\n  🔧 [调用工具: {part.function_call.name}"
                        f"({part.function_call.args})]",
                        flush=True,
                    )
                elif part.function_response:
                    print(
                        f"  📊 [工具结果: {part.function_response.response}]",
                        flush=True,
                    )

        # 换行结束本轮
        print()


def main():
    """入口函数"""
    try:
        asyncio.run(run_conversation())
    except KeyboardInterrupt:
        print("\n👋 再见！")


if __name__ == "__main__":
    main()
