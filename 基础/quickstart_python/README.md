# tRPC-Agent Python Quickstart

支持**多轮对话**与**流式输出**的基础 Agent 示例。

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的模型配置

# 3. 运行
python main.py
```

## 项目结构

```
quickstart_python/
├── .env.example      # 环境变量模板
├── requirements.txt  # Python 依赖
├── main.py           # 入口：多轮对话循环 + 流式输出
├── README.md
└── agent/
    ├── __init__.py
    ├── config.py     # 从环境变量读取模型配置
    ├── prompts.py    # System Instruction
    ├── tools.py      # 3 个工具：天气 / 计算器 / 时间
    └── agent.py      # LlmAgent 声明，绑定模型与工具
```

## 交互命令

| 命令 | 说明 |
|------|------|
| `/exit` | 退出对话 |
| `/clear` | 清空会话，开始新对话 |

## 示例对话

```
👤 You: 北京今天天气怎么样？
  🔧 [调用工具: get_weather({"city": "北京"})]
  📊 [工具结果: {"temperature": "25°C", "condition": "晴", ...}]
🤖 Assistant: 北京今天天气晴朗，气温 25°C，湿度 60%，北风3级。

👤 You: 帮我算一下 2 的 10 次方
  🔧 [调用工具: calculate({"expression": "2 ** 10"})]
  📊 [工具结果: {"expression": "2 ** 10", "result": "1024"}]
🤖 Assistant: 2 的 10 次方等于 1024。

👤 You: 现在几点了？
  🔧 [调用工具: get_current_time({})]
  📊 [工具结果: {"datetime": "2026-06-25 16:30:00", ...}]
🤖 Assistant: 现在是北京时间 2026年6月25日 16:30。
```
