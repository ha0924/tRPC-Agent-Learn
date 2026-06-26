# tRPC-Agent 学习总览

> 腾讯 tRPC-Agent 框架学习计划 — 从基础到实战的完整路径

---

## 一、学习阶段总览

| 阶段 | 核心目标 | 关键产出 |
|------|---------|---------|
| **基础** | 理解 Agent 核心抽象，跑通最小示例 | 支持多轮对话与流式输出的基础 Agent |
| **进阶** | 掌握记忆 / 知识库 / 多 Agent / 协议 / 评测 | 能设计复杂 Agent 系统的架构能力 |
| **实战** | 动手构建多个独立场景项目 | 5 个可运行的实战项目 |
| **进阶挑战** | 综合应用，交付企业级项目 | 企业知识助手 / 研发自动化助手 |

---

## 二、基础阶段（4 个模块）

### 2.1 Agent 工程化核心概念

**目标**：理解框架中的基础抽象及一次完整调用链路。

| 概念 | 说明 |
|------|------|
| **Agent** | 智能体，封装了模型、工具、指令的核心执行单元 |
| **Runner** | 运行器，驱动 Agent 执行循环（输入 → 推理 → 工具调用 → 输出） |
| **Model** | 大模型接口抽象，统一不同 LLM 的调用方式 |
| **Tool** | 工具，Agent 可调用的外部能力（函数、API、服务等） |
| **Session** | 会话，管理消息历史、状态和 token 用量 |
| **Memory** | 长期记忆，跨会话的信息沉淀与召回 |
| **Graph** | 图编排，以 DAG 方式组合多个 Agent 节点 |

**完整调用链路**：
```
用户输入 → Runner 接收 → Session 加载历史 → Memory 召回 → 构造 Prompt
→ Model 推理 → 判断是否需要工具调用 → Tool 执行 → 模型再推理
→ 生成事件流输出 → Session 保存状态 → 返回用户
```

### 2.2 跑通 Python / Go Quickstart

**目标**：基于 `LlmAgent`、`Runner` 和模型配置，完成一个支持**多轮对话**与**流式输出**的基础 Agent。

**关键步骤**：
1. 安装 tRPC-Agent SDK（Python / Go）
2. 配置模型（API Key、Model Name、Endpoint）
3. 创建 `LlmAgent`，设定 system instruction
4. 使用 `Runner` 驱动执行
5. 实现多轮对话循环 + 流式事件消费

### 2.3 Function Calling 与工具调用

**目标**：将普通函数封装为 `FunctionTool`，理解工具调用全流程。

**核心知识点**：
- **工具 Schema**：名称、描述、参数类型定义（JSON Schema）
- **入参解析**：模型生成的参数 → 工具函数接收
- **返回值**：工具执行结果 → 回传模型继续推理
- **错误处理**：工具执行异常的捕获与反馈机制
- **触发过程**：模型根据 system prompt + 用户意图决定是否调用工具

### 2.4 Session 会话管理

**目标**：掌握会话中消息、状态、事件、token usage 的管理方式。

| 后端类型 | 适用场景 |
|---------|---------|
| **InMemory** | 本地开发、测试、单进程短生命周期 |
| **Redis** | 高并发、多实例、需要低延迟的生产环境 |
| **SQL** | 需要持久化审计、会话回溯、结构化查询的场景 |

---

## 三、进阶阶段（5 个模块）

### 3.1 Memory 与 Knowledge / RAG

| 维度 | Memory（长期记忆） | Knowledge（知识库 / RAG） |
|------|-------------------|-------------------------|
| **数据来源** | Agent 运行过程中沉淀 | 外部文档主动导入 |
| **写入** | 自动 / 手动写入记忆条目 | 文档加载 → 切分 → 向量化 |
| **检索** | 按 user / session 召回 | 语义相似度检索 Top-K |
| **用途** | 个性化、偏好、历史决策 | 领域知识问答、文档 QA |

**RAG 流程**：
```
文档加载 → 文本切分（Chunk）→ 向量化（Embedding）
→ 向量存储（Vector Store）→ 语义检索 → 上下文拼接 → Prompt → 模型生成
```

### 3.2 多 Agent 协作与图编排

| 编排模式 | 说明 | 场景举例 |
|---------|------|---------|
| **Chain** | 串行执行，上一个输出作为下一个输入 | 翻译 → 审校 → 排版 |
| **Parallel** | 并行执行，合并结果 | 多维度分析并汇总 |
| **Cycle** | 循环执行，直到满足终止条件 | 自我纠错、迭代优化 |
| **TeamAgent** | 多 Agent 协作团队 | 角色分工协作完成任务 |
| **GraphAgent** | DAG 图编排 | 审批流、诊断流、任务流 |

**GraphAgent 核心机制**：
- **节点（Node）**：每个 Agent 或处理函数
- **边（Edge）**：节点间的数据流转
- **条件路由**：根据状态 / 输出动态选择下游节点
- **状态 Reducer**：多分支结果的合并策略
- **Checkpoint**：执行中间状态的持久化快照
- **Interrupt / Resume**：支持人工审批、暂停恢复

### 3.3 MCP、A2A 与 AG-UI 协议

| 协议 | 定位 | 方向 |
|------|------|------|
| **MCP** | Model Context Protocol | Agent ↔ 外部工具服务 |
| **A2A** | Agent-to-Agent | Agent ↔ Agent 互通 |
| **AG-UI** | Agent-to-UI | Agent → 前端结构化事件流 |

**服务化部署方式**：
- FastAPI Server
- Gateway Server
- Go Server

### 3.4 Skills 与 CodeExecutor

> 📖 详细笔记：[`进阶/3.4-Skills与CodeExecutor.md`](进阶/3.4-Skills与CodeExecutor.md)

**Skills**：
- 通过 `SKILL.md` 描述技能（frontmatter：name / description / location + 正文 SOP）
- Progressive Disclosure（渐进式披露）：启动只注入目录，按需 load 全文，省 context
- 支持 skill load → run 的生命周期，封装可复用的任务能力
- Skill vs Tool vs MCP：手册 vs 刀片 vs 外部服务

**Workspace Runtime**（执行环境的标准化抽象层）：
- 目录约定：`work/inputs/`（输入）、`out/`（产出）、`runs/`（日志）
- 装载具体 Executor backend（local / container / e2b 等）
- 生命周期：Create → Init Hook → StageInputs → RunProgram → Collect → Destroy
- 持久化策略：PerSession（同会话复用）/ PerTurn（每轮独立）

**CodeExecutor 执行环境**（安全谱系）：
| 环境 | 安全级别 | 隔离技术 | 适用场景 |
|------|---------|---------|---------|
| 本地执行 (local) | 低 | 无 | 本地开发调试 |
| Workspace Runtime | 中低 | 路径白名单 + 用户确认 | IDE Agent |
| 容器执行 (container) | 中 | Docker（Namespaces/Cgroups/Capabilities/Seccomp）| 自建生产 |
| Jupyter Kernel | 中 | Kernel 进程隔离 | 数据分析友好 |
| E2B 公有云 | 高 | Firecracker microVM（独立内核）| SaaS / 海外 |
| Cube 私有化 | 高 | KVM microVM（兼容 E2B 协议）| 国内企业 / 强合规 |

**核心要点**：
- Cube = "E2B 的国产平替"，协议 100% 兼容，应用代码零改动
- tRPC-Agent-Go 的 `codeexecutor/e2b` 同时支持 E2B 公有云和 Cube 私有化
- 安全防御不只是"防代码逃逸"，更要防"数据被合规带走"（5 级隐私防御）
- 镜像策略：场景化镜像 + 四层缺包兜底 + 容器池预热 = "时间更快 + 越用越快"

### 3.5 评测、优化与可观测性

**评测体系**：
- **Eval Set**：评测用例集合（输入 + 期望输出 / 行为）
- **Metric**：量化指标（准确率、召回率、相关性等）
- **LLM Judge**：用大模型评判 Agent 输出质量
- **Rubric Evaluator**：基于评分细则的结构化评估

**优化手段**：
- Prompt Iteration（提示词迭代）
- AgentOptimizer（自动化优化）

**可观测性**：
- **OpenTelemetry**：分布式 tracing
- **Langfuse**：Agent 专用 tracing 与分析
- **监控指标**：token usage、延迟、错误率

---

## 四、实战阶段（5 个项目）

### 项目 1：工具调用基础助手
- 天气查询、搜索、文件处理、计算器、时间查询
- 多轮对话 + Function Calling

### 项目 2：RAG 问答 Agent
- 文档加载 → 向量检索 → 上下文拼接
- 多轮追问 + 答案生成

### 项目 3：Session 持久化
- 使用 Redis 或 SQL 持久化会话
- 验证：会话恢复、历史裁剪、摘要生成、token 统计

### 项目 4：自定义 Skill
- 编写 `SKILL.md` 封装可复用任务
- Agent 运行时动态加载并调用 Skill

### 项目 5：Agent 服务化
- 通过 MCP / A2A / AG-UI / FastAPI / Gateway 暴露 Agent 为服务
- 可被前端、工具平台或其他 Agent 调用

---

## 五、进阶挑战（4 个项目）

### 挑战 1：多 Agent 企业知识助手
**要求覆盖**：多轮对话 | 工具调用 | 知识库检索 | 长期记忆 | 任务拆解 | 流式事件 | 运行日志

### 挑战 2：研发自动化助手
**技术栈**：Skills + CodeExecutor + MCP + Session / Memory
**流程**：需求分析 → 代码检索 → 任务拆解 → 执行反馈 → 结果总结

### 挑战 3：GraphAgent 工作流编排
**机制**：条件路由 + 状态 Reducer + Checkpoint + Interrupt / Resume
**场景**：审批流 / 诊断流 / 规划流 / 多步骤任务执行

### 挑战 4：Agent 评测体系建设
**内容**：Eval Cases + LLM Judge + Rubric 指标 + Tracing
**目标**：数据驱动地比较不同 prompt、模型、工具策略的效果

---

## 六、推荐学习路径

```
Quickstart（跑通最小 Agent）
    ↓
Tools（FunctionTool / MCPToolset / Streaming Tool / Agent-as-Tool）
    ↓
Session / Memory / Knowledge（短期上下文 → 长期记忆 → 外部知识）
    ↓
Multi-Agent / GraphAgent（链式 → 并行 → 循环 → 图编排）
    ↓
Server / Protocols（MCP → A2A → AG-UI → 服务化部署）
    ↓
Evaluation / Observability（评测 → 日志 → Tracing → Metrics → 质量优化）
```

---

## 七、学习资源

| 类型 | 内容 |
|------|------|
| 源码与示例 | tRPC-Agent-Python 仓库 README + `examples/` |
| 源码与示例 | tRPC-Agent-Go 仓库 README + 基础 Agent / GraphAgent / Server 示例 |
| 官方文档 | `docs/` 目录：Session、Memory、Knowledge、Tools、MCP、A2A、AG-UI、Evaluation、Observability |

---

## 八、验收标准

### 最终交付物
**企业知识助手** 或 **研发自动化助手**，至少包含：

- [x] 多轮对话
- [x] 工具调用
- [x] 知识库检索
- [x] 长期记忆
- [x] 任务拆解
- [x] 流式事件输出
- [x] 运行日志
- [x] 评测集
- [x] 一种服务化协议（MCP / A2A / AG-UI / FastAPI）

### 能力验证
> 如果学习者能够清楚解释一次 Agent 运行中的**模型输入**、**工具调用**、**状态变化**、**记忆召回**、**事件输出**和**评测结果**，就说明已经从"使用 Agent 框架"进入到"理解 Agent 工程系统"的阶段。

---

*文档创建时间：2026-06-25*
