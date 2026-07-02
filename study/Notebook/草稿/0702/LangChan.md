## 第一章

查看全部

这些结果提供了关于LangChain最新框架的丰富信息。我的回答将涵盖LangChain 1.0及后续版本、LangGraph、LangSmith、DeepAgents、LangChain Labs等关键组件和更新。回答将采用中文，并引用这些来源。

截至2026年6月，LangChain已演进为一个以**LangChain 1.x核心库**为基础，**LangGraph**为流程引擎，**LangSmith**为开发运维平台的生产级生态。以下是根据官方文档和新闻稿整理的最新框架全景。

### 🚀 核心版本与发布动态

- **稳定版本**：LangChain **v1.3.0** 于2026年5月12日发布，`langchain-core` **v1.4.0** 也于5月30日发布。最新的补丁版本已更新至 **v1.3.10** (2026年6月18日)。
- **官方范式**：官方明确**LCEL (LangChain Expression Language) + LangGraph** 为2026年构建Agent与RAG应用的主流范式。

### 🧩 核心框架与组件解析

LangChain 1.0采用了“分层解耦”的设计，其核心组件包括：

- **LangChain 1.x (`langchain`)**：核心库提供模型集成、工具调用等基础抽象。v1.3.0优化了事件流API (`stream_events`)。1.0版本相比之前**主包体积缩减40%**，**异步处理吞吐量提升3倍** (QPS从120增至380)。
- **LangGraph (`langgraph`)**：作为底层流程引擎，支撑复杂业务流程。**v1.2.0** (2026年5月12日) 引入了 **`DeltaChannel`**，能显著降低长时运行任务（如长期对话）的检查点(Checkpoint)开销。
- **Deep Agents (`deepagents`)**：用于构建能规划、反思的“深度智能体”。**v0.6.0** (2026年5月12日) 新增了实验性的代码执行环境(**QuickJS运行时**)和基于LangSmith Hub的版本化文件系统后端(**`ContextHubBackend`**)。
- **LangSmith**：统一的**智能体开发运维平台**，提供从构建到监控的全生命周期支持。
  - **Fleet On-Call Copilot**：一个用于告警排查的智能体模板。
  - **Computer Use in Fleet**：允许智能体在隔离的虚拟电脑中安全执行代码和API调用。
  - **Agent Builder**：支持用自然语言描述来构建智能体。
  - **Sandboxes**：为智能体提供安全的代码执行沙盒环境。
  - **Polly**：一个能像工程师一样执行操作的AI助手。
- **LangChain Labs**：2026年5月启动的应用研究计划，专注于智能体的**持续学习(Continual Learning)**。

### 🔧 最新特性与改进

- **智能体评估**：`Deep Agents`新增 **`RubricMiddleware`**，允许智能体根据预设标准自我评估和迭代。
- **开发者体验**：强化了**TypeScript类型系统**（定义覆盖率从65%提升至92%），LangGraph v1.1带来了**类型安全**的流式传输和调用。
- **集成与生态**：提供了**一流的MCP工具支持**，并持续增强与Anthropic、OpenAI、Google等模型提供商的适配器。

### 💎 总结

2026年的LangChain已是一个成熟、模块化的生产级应用框架。其核心演进方向是通过**LangGraph**实现强大的流程控制，通过**LangSmith**提供全生命周期管理，并通过**Deep Agents**和**LangChain Labs**等探索智能体的更高阶能力。

如果想深入了解某个特定组件（如LangGraph或LangSmith），我可以为你提供更详细的信息。



帮我归纳

这份PDF是尚硅谷关于**LangChain 1.2**的课程讲义，内容非常系统。我为你梳理了它的核心逻辑和关键结论，帮你快速建立知识框架：

### 一、 LangChain的定位：大模型的“操作系统中间层”

它不是为了封装API而存在，而是为了解决大模型的三大硬伤：**知识滞后**（无实时数据）、**幻觉**（胡编乱造）和**无法行动**（只能输出文本，不能执行任务）。其核心价值是**打通外部资源**（数据库、API、文件）、**封装底层复杂度**，让开发者能快速搭建能“动起来”的智能体。

### 二、 关键版本转折（必须关注！）

讲义重点区分了两个时代，这直接影响你该学哪个版本：

| 维度           | **v0.3 版本（旧时代）**                 | **v1.2 版本（当前主流）**                                |
| :------------- | :-------------------------------------- | :------------------------------------------------------- |
| **核心理念**   | 以“链（Chain）”为核心，调用方式硬编码。 | **范式转移**：以“智能体（Agent）”和“图编排”为核心。      |
| **构建方式**   | 使用 `initialize_agent` 等旧API。       | 官方推荐 `create_agent`，**底层基于 LangGraph**。        |
| **稳定性**     | API变动频繁，被称为“版本碎钞机”。       | **官方承诺 1.x 系列无破坏性变更**，生产级稳定。          |
| **工具与输出** | 类型安全弱，需正则解析输出。            | 支持 Pydantic 类型安全，结构化输出成为“一等公民”。       |
| **扩展性**     | 修改逻辑常需改源码。                    | 引入强大的 **中间件（Middleware）** 系统，灵活拦截扩展。 |

> **结论**：**新项目请直接上手 v1.x**，不要再学 v0.3 的旧写法。

### 三、 LangChain 生态的“四大支柱”（核心架构）

讲义指出，LangChain 已不只是一个库，而是覆盖全生命周期的生态。四者的分工极其明确：

1. **LangChain（基础能力层）**：**“有什么能力”**。提供模型调用、工具定义、消息格式等标准化抽象，是轻量级智能体的起点。
2. **LangGraph（编排引擎层）**：**“怎么跑”**。将智能体流程抽象为**节点（Node）+ 边（Edge）+ 状态（State）**的有向图，解决复杂多步骤、有状态的工作流（支持循环）。
3. **Deep Agents（高级执行框架）**：**“怎么更聪明地跑”**。内置了规划能力、虚拟文件系统、子智能体协作等“电池”，让你不必从零构建复杂逻辑。
4. **LangSmith（可观测性平台）**：**“跑得怎么样”**。全链路追踪、调试和评估工具，让复杂的 Agent 内部运行过程变得透明。

### 四、 核心应用场景（RAG 与 Agent）

讲义重点剖析了这两个最火的方向：

- **RAG（检索增强生成）**：解决“知识不足”。通过**解析→切割→向量检索→重排（Reranker）**等流程，给大模型“开卷考试”的资料。适合高精度知识库问答。
- **Agent（智能体）**：解决“能力不足”。数学公式为：**Agent = LLM + 规划 + 工具 + 记忆 + 行动**。它像大脑中枢，能自主分解任务（如查天气订票）、调用外部API，并能记忆上下文。

### 五、 开发准备与选型建议

- **前置知识**：Python 3.10+ 基础（装饰器、异步）、大模型基本概念（Token、Embedding）。

- **环境管理**：

  - **Conda（课程推荐）**：适合需要管理 **CUDA、系统库** 等复杂底层依赖的场景。
  - **Uv（现代替代）**：适合**纯 Python** 项目（如 RAG、Web后端），速度极快。

- **安装命令**（务必指定版本避免冲突）：

  bash

  ```
  conda create --name langchain1.2 python=3.13.12
  conda activate langchain1.2
  conda install langchain==1.2.12
  ```

  

### 六、 技术选型思路（降本增效）

面对需求时，按**成本从低到高**选择方案：
**纯 Prompt 提示词** → **Agent + Function Calling**（需实时外部数据） → **RAG**（需私有领域知识） → **Fine-tuning 微调**（前三种解决不了，且预算充足时才用）。

------

如果你打算上手写代码，建议重点精读PDF中关于 **LCEL 语法**和 **LangGraph 状态管理**的部分（后续章节），这是目前主流开发范式的基础。需要我帮你梳理 LCEL 的核心写法吗？😊

LangChain模型调用笔记



详细总结一下，我需要一份笔记

我们根据PDF内容，提取关键知识点，按章节结构整理成一份详细笔记。需要涵盖模型调用的准备工作、模型初始化的多种方式（包括使用提供商库、兼容用法、中转平台、init_chat_model）、模型调用方法（invoke、stream、batch、异步）、以及参数、配置、美化输出等拓展内容。笔记要条理清晰，便于复习。

# LangChain 模型创建与调用 学习笔记

> 基于尚硅谷宋红康课程，LangChain v1.x 版本

------

## 一、模型调用的准备工作

### 1.1 核心概念：Model I/O

LangChain 的模型调用遵循三阶段模式：

- **Format（格式化）**：使用 `PromptTemplate` 构建输入提示
- **Predict（预测）**：通过 `Model` 调用大模型
- **Parse（解析）**：使用 `OutputParser` 解析模型输出

> 历史背景：GPT-3 时代以补全模型为主，LangChain 提供高层封装辅助对话、工具调用等；GPT-3.5 后对话模型成为主流，指令跟随能力大幅增强。

### 1.2 模型初始化的三个维度

1. **调用谁的 API** → 模型提供商（DeepSeek、智谱、阿里等）
2. **参数配置方式** → 配置文件（推荐）vs 硬编码
3. **模型部署位置** → 在线云服务 vs 本地部署

### 1.3 常用线上大模型平台

| 平台       | 网址                                                         | 特点                          |
| :--------- | :----------------------------------------------------------- | :---------------------------- |
| OpenRouter | [openrouter.ai](https://openrouter.ai/)                      | 全球主流，含国外模型，需魔法  |
| CloseAI    | [closeai-asia.com](https://closeai-asia.com/)                | 亚洲最大，含国外模型          |
| 阿里云百炼 | [bailian.console.aliyun.com](https://bailian.console.aliyun.com/) | 企业友好，新用户送5000万Token |
| 硅基流动   | [siliconflow.cn](https://siliconflow.cn/)                    | 性价比高，9B以下免费          |
| 百度千帆   | [console.bce.baidu.com/qianfan](https://console.bce.baidu.com/qianfan) | 百度生态                      |
| 火山引擎   | [console.volcengine.com/ark](https://console.volcengine.com/ark) | 字节多模态生态                |

> **注意**：每个平台配置需要三要素：模型名、api-key、base-url。

### 1.4 环境准备

使用 `requirements.txt` 统一管理依赖，避免版本冲突。核心依赖包括：

- `langchain-openai`（OpenAI 兼容接口）
- `langchain-deepseek`（DeepSeek 专用）
- `langchain-community`（智谱、通义等）
- `python-dotenv`（环境变量管理）

------

## 二、模型初始化方式

### 2.1 方式一：使用模型提供商专用类

#### 2.1.1 DeepSeek 模型

python

```
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# 方式1：显式传入参数
deepseek_llm = ChatDeepSeek(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    api_base=os.getenv("DEEPSEEK_BASE_URL"),  # 注意字段名是 api_base
    model="deepseek-v4-flash"
)

# 方式2：自动从环境变量读取（推荐）
deepseek_llm = ChatDeepSeek(model="deepseek-v4-flash")

print(deepseek_llm.invoke("请介绍一下你自己"))
```



- 环境变量：`DEEPSEEK_API_KEY`、`DEEPSEEK_BASE_URL`（默认 `https://api.deepseek.com/v1`）
- 方式3（不推荐）：硬编码 API Key 在代码中

#### 2.1.2 智谱大模型

python

```
from langchain_community.chat_models import ChatZhipuAI

zhipu_llm = ChatZhipuAI(
    model="glm-5.1",
    api_key=os.getenv("ZHIPUAI_API_KEY"),
    api_base=os.getenv("ZHIPUAI_BASE_URL")
)
```



- 依赖：`langchain-community` + `pyjwt`
- 环境变量：`ZHIPUAI_API_KEY`、`ZHIPUAI_BASE_URL`

#### 2.1.3 通义千问（阿里百炼）

python

```
from langchain_community.chat_models import ChatTongyi

tongyi_llm = ChatTongyi(
    model="qwen-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY")
)
```



- 依赖：`dashscope`
- 环境变量：`DASHSCOPE_API_KEY`
- **注意**：`ChatTongyi` 基于专用 SDK，不要设置 `DASHSCOPE_BASE_URL`，否则报错

### 2.2 方式二：兼容用法（ChatOpenAI 统一接口）

对于没有专用类的平台，或希望统一配置风格，可以使用 `ChatOpenAI`：

python

```
from langchain_openai import ChatOpenAI

# 调用 DeepSeek
deepseek_llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    model="deepseek-v4-flash"
)

# 调用智谱
zhipu_llm = ChatOpenAI(
    api_key=os.getenv("ZHIPUAI_API_KEY"),
    base_url=os.getenv("ZHIPUAI_BASE_URL"),
    model="glm-5.1"
)

# 调用通义（需配置 OpenAI 兼容 URL）
tongyi_llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus"
)
```



### 2.3 方式三：中转平台（OpenRouter / CloseAI）

#### OpenRouter（需魔法）

python

```
from langchain_openrouter import ChatOpenRouter

model = ChatOpenRouter(
    model="deepseek/deepseek-v4-flash",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
```



- 专用集成：`langchain-openrouter`
- 也可用 `ChatOpenAI` 兼容方式调用

#### CloseAI

python

```
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="deepseek-v4-flash",   # 或 gpt-5-mini
    api_key=os.getenv("CLOSEAI_API_KEY"),
    base_url=os.getenv("CLOSEAI_BASE_URL")
)
```



------

## 三、统一初始化接口：`init_chat_model()`

LangChain 1.x 推出的统一接口，自动根据模型名称选择对应驱动类。

### 基本语法

python

```
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "provider:model_name",   # 如 "deepseek:deepseek-v4-flash"
    api_key="your-key",
    temperature=0.7,
    max_tokens=1000
)
```



### 使用示例

**1. DeepSeek 官网**

python

```
model = init_chat_model(
    model="deepseek:deepseek-v4-flash",
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL
)
```



**2. 阿里百炼（OpenAI 兼容）**

python

```
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",   # 必须指定 provider
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
```



**3. CloseAI 中转**

python

```
model = init_chat_model(
    model="deepseek-v4-flash",
    model_provider="openai",
    api_key=CLOSEAI_API_KEY,
    base_url=CLOSEAI_BASE_URL
)
```



### 关于 `model_provider`

- 支持的 provider 列表：`anthropic`, `openai`, `deepseek`, `ollama`, `google_genai`, `mistralai`, `cohere`, `groq`, `huggingface`, `xai`, `perplexity`, `together`, `fireworks`, `nvidia`, `ibm`, `bedrock` 等
- 若模型名未带前缀（如 `qwen-plus`），必须通过 `model_provider` 指定
- 若用 `provider:model` 格式，可省略 `model_provider`

------

## 四、模型初始化常用参数

| 参数             | 类型  | 说明                      | 默认值 |
| :--------------- | :---- | :------------------------ | :----- |
| `model`          | str   | 模型名称（必需）          | 无     |
| `model_provider` | str   | 提供商                    | 无     |
| `api_key`        | str   | API密钥，可从环境变量读取 | None   |
| `base_url`       | str   | API请求地址               | None   |
| `temperature`    | float | 随机性控制，0.0~2.0       | 0.7    |
| `max_tokens`     | int   | 最大输出Token数           | None   |
| `timeout`        | float | 超时时间（秒）            | None   |
| `max_retries`    | int   | 失败重试次数              | 6      |

### Temperature 选择建议

- **0.0–0.3**：需要确定性（数学、分类、代码生成）
- **0.5–0.7**：平衡创造性与一致性（聊天、问答）
- **0.8–1.5**：创造性任务（写作、头脑风暴）
- **1.5–2.0**：高度创造性（诗歌、故事）

### Token 估算

- 英文：1 token ≈ 4 字符 ≈ 0.75 单词
- 中文：1 token ≈ 1–2 汉字

------

## 五、模型的调用方法

### 5.1 `invoke()` —— 同步阻塞调用

最核心方法，等待完整响应后一次性返回。

**输入形式：**

1. **文本输入**（最简单）

   python

   ```
   response = model.invoke("翻译成英文：你好世界")
   ```

   

2. **字典列表**（推荐，支持系统提示和多轮对话）

   python

   ```
   messages = [
       {"role": "system", "content": "你是一个专业的数学老师。"},
       {"role": "user", "content": "什么是斐波那契数列？"}
   ]
   response = model.invoke(messages)
   ```

   

   - 角色：`system`（系统设定）、`user`（用户）、`assistant`（AI历史回复）
   - 多轮对话需手动维护消息列表，追加 assistant 回复

3. **消息对象列表**（类型安全）

   python

   ```
   from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
   
   messages = [
       SystemMessage("你是一个Python专家"),
       HumanMessage("什么是生成器？")
   ]
   response = model.invoke(messages)
   ```

   

**返回值：`AIMessage` 对象**

- `content`：模型生成的文本
- `response_metadata`：包含 token 用量、模型版本、延迟指标等
- `usage_metadata`：标准化消耗统计
- `tool_calls`：工具调用信息

**常用属性提取：**

python

```
print(response.content)
print(response.response_metadata['model_name'])
print(response.response_metadata['finish_reason'])
print(response.usage_metadata['total_tokens'])
```



### 5.2 `stream()` —— 流式输出

实时逐 token 返回，提升用户体验。

python

```
for chunk in model.stream("写一首七言律诗"):
    print(chunk.content, end="", flush=True)
```



### 5.3 `batch()` —— 批量调用

并行处理多个独立请求，大幅提升效率。

python

```
inputs = ["翻译成英文：春天来了", "翻译成英文：夏天很热"]
responses = model.batch(inputs)  # 按输入顺序返回列表
```



`batch_as_completed()`：按完成顺序返回（带索引），不等待全部完成。

python

```
for idx, response in model.batch_as_completed(inputs):
    print(f"第{idx}个请求完成：{response.content}")
```



**性能对比**：batch 比循环 invoke 节省约 50% 时间。

### 5.4 异步调用（`ainvoke`, `astream`, `abatch`）

避免阻塞主线程，适合高并发场景。

python

```
import asyncio

async def main():
    task = asyncio.create_task(model.ainvoke("用一句话解释AI"))
    # 并行执行其他任务
    await asyncio.sleep(1)
    response = await task
    print(response.content)

asyncio.run(main())
```



- `astream`：异步流式
- `abatch`：异步批量

------

## 六、异常处理

python

```
try:
    response = model.invoke("Hello")
except ValueError as e:
    print(f"配置错误: {e}")
except ConnectionError as e:
    print(f"网络错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```



------

## 七、本地模型部署与调用（Ollama）

### 7.1 Ollama 简介

本地运行大模型的集成框架，支持 Qwen、DeepSeek 等。

### 7.2 安装

- Windows：下载安装包，可指定安装目录
- Linux：`curl -fsSL https://ollama.com/install.sh | sh`
- Mac：下载 dmg 安装

### 7.3 模型下载与运行

bash

```
ollama run deepseek-r1:1.5b   # 自动下载并启动交互
```



常用命令：

| 命令                  | 说明             |
| :-------------------- | :--------------- |
| `ollama pull <model>` | 下载模型         |
| `ollama list`         | 查看已下载模型   |
| `ollama rm <model>`   | 删除模型         |
| `ollama ps`           | 查看运行中的模型 |
| `ollama stop <model>` | 停止模型         |

### 7.4 LangChain 调用 Ollama

python

```
from langchain_ollama import ChatOllama

ollama_llm = ChatOllama(
    model="deepseek-r1:1.5b",
    base_url="http://localhost:11434"  # 可省略
)

# 或通过 init_chat_model
ollama_llm = init_chat_model(
    model="deepseek-r1:1.5b",
    model_provider="ollama"
)
```



------

## 八、拓展内容

### 8.1 美化输出

- **`pretty_print()`**：美化打印 AIMessage

  python

  ```
  response.pretty_print()
  ```

  

- **`rich` 库**：终端彩色输出

  python

  ```
  from rich import print as rprint
  rprint(response)
  ```

  

### 8.2 模型能力画像（`profile`）

查看模型支持的输入输出能力（需 LangChain 已声明）：

python

```
print(model.profile)
# 输出示例：max_input_tokens, max_output_tokens, text_inputs, image_inputs, tool_calling 等
```



### 8.3 查看完整参数列表

python

```
from langchain_deepseek import ChatDeepSeek
print(ChatDeepSeek.model_fields.keys())   # 所有可配置字段
```



参数构成：

1. **网络连接参数**：`api_key`, `api_base`, `request_timeout`, `max_retries`, `http_client`, `openai_proxy`, `default_headers`
2. **模型推理参数**：`temperature`, `top_p`, `max_tokens`, `stop`, `streaming`, `n`, `reasoning`, `presence_penalty`, `frequency_penalty`
3. **LangChain 框架参数**：`name`, `verbose`, `callbacks`, `tags`, `metadata`, `cache`, `rate_limiter`
4. **高级扩展参数**：
   - `model_kwargs`：传递 API 支持但 LangChain 未直接列出的字段（如 tools）
   - `extra_body`：传递厂商扩展字段（如 DeepSeek 的 `thinking`）

示例：启用 DeepSeek 思考模式

python

```
model = init_chat_model(
    model="deepseek:deepseek-v4-flash",
    extra_body={"thinking": {"type": "enabled"}}
)
response = model.invoke("你好，一句话回答")
# 响应中会包含 reasoning_content
```



### 8.4 运行时 `config` 参数

在调用时动态调整行为（优先级高于初始化参数）：

python

```
config = {
    "run_name": "joke_generation",      # LangSmith 追踪名称
    "tags": ["test", "dev"],            # 分类标签
    "metadata": {"user_id": "123"},     # 业务元数据
    "max_concurrency": 5,               # 最大并发数
    "configurable": {                   # 动态覆盖模型参数
        "temperature": 0.7,
        "max_tokens": 1000
    }
}

response = model.invoke("1+2=?", config=config)
```



------

## 九、总结：模型创建方式对比

| 模型/平台         | 专用类         | ChatOpenAI    | init_chat_model | 备注                     |
| :---------------- | :------------- | :------------ | :-------------- | :----------------------- |
| DeepSeek 官网     | ChatDeepSeek   | ✅             | ✅               | 推荐专用类               |
| 阿里百炼 DeepSeek | ChatTongyi     | ✅             | ✅               | 需指定 provider="openai" |
| 智谱 AI           | ChatZhipuAI    | ✅             | ✅               | 依赖 pyjwt               |
| 通义千问          | ChatTongyi     | ✅（兼容模式） | ✅               | 不要设置 BASE_URL        |
| OpenRouter        | ChatOpenRouter | ✅             | ✅               | 需魔法                   |
| CloseAI           | ❌              | ✅             | ✅               | 无专用类                 |
| Ollama 本地       | ChatOllama     | ❌             | ✅               | 本地部署                 |

------

> **核心原则**：优先使用 `.env` 配置文件管理密钥，推荐 `init_chat_model` 统一接口，根据场景选择合适的调用方法（invoke/stream/batch/异步），并善用 `config` 实现运行时动态控制。

本回答由 AI 生成，内容仅供参考，请仔细甄别



详细总结一下，我需要一份笔记

我们根据提供的PDF内容，为LangSmith的使用整理一份详细的学习笔记。内容涵盖LangSmith概述、功能、账号准备、环境配置、监控查看等。格式清晰，便于复习。

# LangSmith 使用指南 学习笔记

> 基于尚硅谷宋红康课程，LangSmith 官方平台

------

## 一、LangSmith 概述

### 1.1 什么是 LangSmith？

LangSmith 是 LangChain 生态系统中**专门用于 LLM 应用调试、监控、评估和管理的平台**。

**四大核心能力：**

- **追踪（Tracing）**：记录每次 LLM 调用的详细信息
- **监控（Monitoring）**：实时查看应用性能
- **调试（Debugging）**：排查问题和优化性能
- **评估（Evaluate）**：系统化测试 LLM 应用

> 官网地址：https://smith.langchain.com/

------

## 二、LangSmith 具体功能详解

### 2.1 核心应用与开发

#### 1. Tracing（追踪）⭐ 最核心功能

- **功能**：完整记录大模型应用的每一次调用链路（Trace）
- **作用**：当 Agent 或 RAG 系统运行变慢或报错时，可查看：
  - 每一步的 Prompt 内容
  - 模型返回结果
  - Token 消耗量
  - 每个链条节点的耗时
- **价值**：极大方便排查 Bug 和优化性能

#### 2. Monitoring（监控）

- **功能**：提供生产环境的高级数据可视化看板
- **作用**：宏观监控应用运行状况，包括：
  - Token 消耗趋势
  - QPS（每秒请求数）
  - 错误率
  - 平均延迟（Latency）
  - 成本预估
- **价值**：适合应用上线后观察系统稳定性和开销

#### 3. Datasets & Experiments（数据集与实验）

- **功能**：管理测试数据集并运行对比实验
- **作用**：
  - 将用户真实输入、边界情况（Edge Cases）存为数据集
  - 修改 Prompt 或更换模型时，运行自动化对比测试
  - 直观查看新旧版本在同一测试集上的表现差异

#### 4. Evaluators（评估器）

- **功能**：配置和自动化评估任务
- **作用**：大模型输出难以用传统断言测试，这里允许配置：
  - 基于规则的评估（如关键词匹配）
  - 基于模型的评估（LLM-as-a-judge）
  - 评估指标：答案相关性、是否包含幻觉等
- **价值**：对追踪数据或实验结果自动打分

#### 5. Annotation Queues（标注队列）

- **功能**：人工反馈与数据清洗工具
- **作用**：
  - 将部分 Traces 发送到标注队列
  - 团队成员进行手动打分、纠正回答、贴标签
  - 高质量标注数据后续可用于微调模型或充当测试集

------

### 2.2 提示词与调试工具

#### 1. Prompts（提示词管理）

- **功能**：类似“提示词版的 GitHub”
- **作用**：
  - 将 Prompt 从代码中解耦，统一云端管理
  - 版本控制（v1, v2...）
  - 代码中通过 API 动态拉取最新提示词
  - 支持团队协作和分享

#### 2. Playground（演练场）

- **功能**：网页端模型交互界面
- **作用**：
  - 无需写代码，直接选择不同模型（OpenAI、Anthropic、本地模型等）
  - 快速微调和测试 Prompt 效果
  - 一键将调整好的 Prompt 保存到 Prompts 仓库

#### 3. Studio（工作室）

- **功能**：与 LangGraph 深度集成，提供可视化图形交互界面
- **作用**：
  - 可视化查看状态机（State）在各节点间的流转
  - 支持在某个节点“暂停”，手动修改数据后再继续执行
- **价值**：调试复杂智能体交互的利器

#### 4. ContextHub（上下文中）

- **功能**：管理全局上下文或通用组件配置
- **作用**：存放可在多个项目或 Prompt 中复用的公共上下文模板、全局变量或系统预设提示

------

### 2.3 部署与沙盒

#### 1. Deployments（部署）

- **功能**：一键将 LangChain 应用或 LangGraph Agent 部署为线上 API 服务（通常依托 LangGraph Cloud）
- **作用**：提供开箱即用的生产端点，处理高并发、队列管理和状态持久化

#### 2. Sandboxes（沙盒）

- **功能**：提供轻量级在线运行和测试环境
- **作用**：在不污染生产环境的前提下，安全试运行、测试新部署的 Agent 或执行自动化脚本

------

> 💡 **现阶段建议**：重点关注 **Tracing**（观察调用细节）和 **Playground**（快速调优提示词）。当应用结构复杂（如 RAG 检索或多 Agent 协同）时，再引入 Datasets 进行量化评估，并用 Studio 进行可视化调试。

------

## 三、账号准备

### 3.1 注册或登录

1. 访问 LangSmith 官网：https://smith.langchain.com/
2. 选择注册或登录方式（GitHub / Google / Email）
3. 登录成功后进入主界面

### 3.2 获取 API_KEY

1. 点击右上角头像 → **Settings**
2. 左侧菜单选择 **API Keys**
3. 点击 **Create API Key**，输入名称后生成
4. **重要**：复制并妥善保存 API Key（**只显示一次**，关闭弹窗后无法再次查看）
5. 如需删除，点击右侧删除图标

------

## 四、环境变量配置

在项目根目录的 `.env` 文件中添加以下四个环境变量：

env

```
# LangSmith 配置
LANGSMITH_TRACING=true                # 开启追踪
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"   # API 端点
LANGSMITH_API_KEY="your-api-key-here" # 上一步获取的 API Key
LANGSMITH_PROJECT="your-project-name" # 项目名称（自定义，用于区分不同应用）
```



**参数说明：**

| 变量名               | 说明                                 |
| :------------------- | :----------------------------------- |
| `LANGSMITH_TRACING`  | 必须设为 `true` 才能启用追踪         |
| `LANGSMITH_ENDPOINT` | 官方 API 地址，通常无需修改          |
| `LANGSMITH_API_KEY`  | 个人 API 密钥，需妥善保管            |
| `LANGSMITH_PROJECT`  | 项目标识，同一个账号下可创建多个项目 |

------

## 五、查看监控指标

### 5.1 运行代码并自动上报

配置好环境变量后，在 Python 代码中通过 `load_dotenv()` 加载，然后运行任意 LangChain 程序，LangSmith 会自动记录运行指标并同步至后台。

**示例代码：**

python

```
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv(override=True)

model = init_chat_model(
    model="deepseek-v4-flash",
    model_provider="openai",
    api_key=os.getenv("CLOSEAI_API_KEY"),
    base_url=os.getenv("CLOSEAI_BASE_URL")
)

print(model.invoke("你好，用一句话回答"))
```



### 5.2 在 LangSmith 界面查看

1. **登录 LangSmith 官网**，进入项目列表
2. 点击对应项目名称（即 `LANGSMITH_PROJECT` 设置的值）
3. 进入 **Tracing** 界面，可以看到所有运行记录

### 5.3 运行详情查看

- 点击任意一条记录，进入详情页面
- 可查看：
  - 输入 Prompt
  - 输出结果
  - Token 用量（输入/输出/总计）
  - 各节点耗时
  - 模型参数配置

### 5.4 查看运行报表

在项目页面顶部或下滑可切换不同指标报表：

- Token 使用趋势
- 请求延迟分布
- 错误率统计
- 成本估算
- 各模型调用占比

------

## 六、进阶用法：运行时自定义元数据

在调用模型时，可通过 `config` 参数向 LangSmith 传递额外信息，便于追踪和筛选：

python

```
config = {
    "run_name": "joke_generation",        # 本次运行显示的名称
    "tags": ["test", "v2"],               # 标签，便于分类过滤
    "metadata": {                         # 自定义元数据
        "user_id": "shkstart",
        "session_id": "sess_123"
    },
    "configurable": {                     # 动态覆盖模型参数
        "temperature": 0.7,
        "max_tokens": 1000
    }
}

response = model.invoke("1+2=？", config=config)
```



这些信息会显示在 LangSmith 的追踪记录中，方便按业务维度（如用户、会话）进行筛选和分析。

------

## 七、总结

| 功能模块                   | 核心用途                 | 适用阶段       |
| :------------------------- | :----------------------- | :------------- |
| **Tracing**                | 调试调用链路，排查错误   | 开发、测试     |
| **Monitoring**             | 宏观监控性能、成本       | 生产环境       |
| **Datasets & Experiments** | 对比测试 Prompt/模型版本 | 迭代优化       |
| **Evaluators**             | 自动化质量评估           | 测试、上线前   |
| **Annotation Queues**      | 人工标注与反馈           | 数据清洗、微调 |
| **Prompts**                | 提示词版本管理与托管     | 团队协作       |
| **Playground**             | 快速调试验证 Prompt      | 开发阶段       |
| **Studio**                 | 可视化调试复杂 Agent     | 高级调试       |
| **Deployments**            | 一键部署为 API 服务      | 上线发布       |

> **快速上手三步走：**
>
> 1. 注册 LangSmith，获取 API Key
> 2. 在 `.env` 中配置四个环境变量
> 3. 运行代码，自动追踪，在官网查看调用详情

LangSmith 是 LLM 应用开发中不可或缺的调试与监控工具，善用它能显著提升开发效率和线上稳定性。

本回答由 AI 生成，内容仅供参考，请仔细甄别

LangChain消息与提示词模板



详细总结一下，我需要一份笔记

我们根据提供的PDF内容，整理一份详细笔记。笔记要覆盖所有重要知识点，包括消息类型、结构、格式、使用示例，提示词模板的机制、使用方式、高级特性等。按章节结构整理，清晰明了。提供完整笔记。

# LangChain 第04章：消息与提示词模板 学习笔记

> 讲师：尚硅谷-宋红康
> 核心内容：LangChain 中 Message 的体系结构、ChatPromptTemplate 的使用与高级特性

------

## 1. 认识消息（Message）

### 1.1 为什么需要消息？

- **大模型无状态**：每次调用只根据当前输入（上下文）生成输出，服务端不维护会话历史。
- **应用需“记住”对话** → 必须在程序中**手动维护消息列表**。
- LangChain 提供统一的 **Message 标准**，跨模型（OpenAI、Anthropic、Gemini 等）保持一致。

**优势**：

- 兼容性强：自动对齐不同模型的消息格式
- 可扩展性高：支持多模态、自定义字段
- 可追踪性好：便于 LangSmith 等工具调试

------

### 1.2 消息的内部结构

每个 Message 对象包含三类字段：

| 字段                 | 说明                                        |
| :------------------- | :------------------------------------------ |
| **Role**             | 角色类型：system / user / assistant / tool  |
| **Content**          | 消息正文内容                                |
| **Metadata**（可选） | 元数据：消息ID、响应时间、Token消耗、标签等 |

------

### 1.3 常用消息类型

| 类型             | Role 值            | 用途                                | 示例                              |
| :--------------- | :----------------- | :---------------------------------- | :-------------------------------- |
| **系统消息**     | `system`           | 设定AI角色、行为准则、背景          | `"你是一个精通编程的软件架构师"`  |
| **用户消息**     | `user` / `human`   | 用户输入（文本或多模态）            | `"你好啊～"`                      |
| **助手消息**     | `assistant` / `ai` | 模型回复（含文本、工具调用等）      | `"我也很高兴认识你"`              |
| **工具调用消息** | `tool`             | 工具执行结果，需关联 `tool_call_id` | `"今天天气很好"` + `tool_call_id` |

**为什么区分类型？**

- 明确角色 → 清晰区分系统提示、用户输入、AI回复
- 控制行为 → 通过 SystemMessage 精确控制
- 构建多轮对话 → 维护完整上下文
- 调试友好 → 易于追踪

------

### 1.4 消息格式

#### 格式1：JSON 字典格式

json

```
{"role": "system", "content": "你是个善解人意的助手"}
{"role": "user", "content": "你好啊～"}
{"role": "assistant", "content": "我也很高兴认识你"}
{"role": "tool", "content": "<工具输出>", "tool_call_id": "call_xxx"}
```



#### 格式2：对象格式（推荐）

python

```
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

SystemMessage(content="你是个善解人意的助手")
HumanMessage(content="你好啊～")
AIMessage(content="我也很高兴认识你")
ToolMessage(content="<工具输出>", tool_call_id="call_xxx")
```



**消息列表示例**：

python

```
messages = [
    SystemMessage(content="你是一个助手"),
    HumanMessage(content="你好"),
    AIMessage(content="你好！有什么可以帮你？"),
    HumanMessage(content="天气怎么样？"),
    AIMessage(content="让我查询一下..."),
    ToolMessage(content="北京：晴天", tool_call_id="call_123"),
    AIMessage(content="北京今天是晴天")
]
```



------

### 1.5 各消息对象字段详解

#### 1.5.1 SystemMessage

- `content`：系统指令（可省略字段名）

python

```
SystemMessage("你是个善解人意的助手")   # 等价于 SystemMessage(content="...")
```



#### 1.5.2 HumanMessage

- `content`：用户输入
- `metadata`：可选元数据（`name`、`id` 等），是否被模型支持取决于供应商

python

```
HumanMessage(content="Hello!", name="alice", id="msg_123")
```



> ⚠️ 注意：并非所有模型都支持 `name` 等元数据（如 DeepSeek 实测不支持，而 OpenAI 支持）。

#### 1.5.3 AIMessage

- `content`：模型输出文本
- `response_metadata`：响应附加元数据（token用量、模型名等）
- `tool_calls`：工具调用列表（当模型决定调用工具时）
- `usage_metadata`：统一用量信息

**tool_calls 结构**：

python

```
tool_calls = [
    {
        'name': 'get_weather',
        'args': {'city': '杭州'},
        'id': 'call_00_xxx',
        'type': 'tool_call'
    }
]
```



**完整响应示例**（含 metadata）：

python

```
AIMessage(
    content='你好！我是小智...',
    additional_kwargs={'refusal': None},
    response_metadata={
        'token_usage': {'completion_tokens': 118, 'prompt_tokens': 34, 'total_tokens': 152},
        'model_provider': 'openai',
        'model_name': 'gpt-5.4-mini-2026-03-17',
        'finish_reason': 'stop'
    },
    id='lc_run-xxx',
    usage_metadata={'input_tokens': 34, 'output_tokens': 118, 'total_tokens': 152}
)
```



#### 1.5.4 ToolMessage

- `content`：工具返回结果
- `tool_call_id`：**必须**与对应 AIMessage 中的 `tool_calls[].id` 一致
- `name`：工具名称（可选）

python

```
ToolMessage(content="今天北京天气晴朗", tool_call_id="call_00_xxx")
```



------

### 1.6 实战：对话历史管理

#### 核心规则：每次调用必须传递**完整的对话历史**

**正确流程**：

python

```
conversation = []
# 第1轮
conversation.append({"role": "user", "content": "我叫张三"})
response1 = model.invoke(conversation)
conversation.append({"role": "assistant", "content": response1.content})  # 必须保存

# 第2轮
conversation.append({"role": "user", "content": "我叫什么？"})
response2 = model.invoke(conversation)   # AI 记得
```



**错误做法**：

- ❌ 每次重新创建消息列表
- ❌ 忘记保存 AI 回复
- ❌ 未将历史传入下一轮

------

### 1.7 对话历史优化（节省Token）

**策略**：只保留最近 N 轮对话 + 始终保留 System 消息。

python

```
def keep_recent_messages(messages, max_pairs=3):
    """保留最近的 N 轮对话（每轮 = user + assistant）"""
    system_msgs = [m for m in messages if m.get("role") == "system"]
    conversation_msgs = [m for m in messages if m.get("role") != "system"]
    recent_msgs = conversation_msgs[-(max_pairs * 2):]   # 每轮2条消息
    return system_msgs + recent_msgs
```



**应用**：在长对话中调用此函数裁剪历史，再传给模型。

------

### 1.8 实战：多轮对话控制台程序

整合上述知识，实现一个带历史记忆与裁剪的交互式对话：

python

```
EXIT_WORD = "exit"
MAX_PAIRS_HISTORY = 3

messages = [{"role": "system", "content": "你是小谷姐姐..."}]

while True:
    user_input = input("请输入：")
    if user_input.lower() == EXIT_WORD: break
    
    messages.append({"role": "user", "content": user_input})
    
    memory_messages = keep_recent_messages(messages, max_pairs=MAX_PAIRS_HISTORY)
    
    reply_content = ""
    for chunk in model.stream(memory_messages):
        print(chunk.content, end="", flush=True)
        reply_content += chunk.content
    
    messages.append({"role": "assistant", "content": reply_content})
```



------

### 1.9 拓展：content 与 content_blocks

#### content 的两种形式

1. **字符串**（纯文本）
2. **字典列表**（多模态，如图片）

**图片输入示例**（Base64编码）：

python

```
HumanMessage(
    content=[
        {'type': 'text', 'text': '这张图里有什么？'},
        {'type': 'image_url', 'image_url': base64_image}
    ]
)
```



#### content_blocks（LangChain 1.x 新特性）

- 跨模型统一的多模态数据结构，类型安全。
- 结构：`list[TypeDict]`，每个 block 有 `type` 字段。
- 支持类型：`text`, `image`, `audio`, `video`, `tool_call`, `reasoning`。

**推荐写法**（统一格式）：

python

```
HumanMessage(
    content_blocks=[
        {'type': 'text', 'text': '这张图里有什么？'},
        {'type': 'image', 'base64': base64_image, 'mime_type': 'image/png'}
    ]
)
```



**输出格式化**：对于带有“思维链”的模型（如 DeepSeek），`content_blocks` 可自动解析出 `reasoning` 块：

python

```
response.content_blocks
# [{'type': 'reasoning', 'reasoning': '...思考过程...'}, {'type': 'text', 'text': '最终回答'}]
```



> 💡 建议优先检查 `response.content_blocks` 而非 `response.content`，以获取完整信息。

------

## 2. 提示词模板（Prompt Templates）

### 2.1 为什么使用模板？

| 方式               | 优点                                 | 缺点                                       |
| :----------------- | :----------------------------------- | :----------------------------------------- |
| **字符串拼接**     | 简单直接，适合临时demo               | 可读性差，易出错，难以维护，不支持复杂场景 |
| **PromptTemplate** | 结构清晰，变量校验，可复用，集成生态 | 有一定学习成本，对极简场景略重             |

**开发建议**：

- 小项目/临时 → 字符串拼接
- 正式开发 → **必须使用提示词模板**

------

### 2.2 机制演进（重要）

| 时代              | 模型接口                | Prompt工具           | 输入/输出格式           |
| :---------------- | :---------------------- | :------------------- | :---------------------- |
| **旧时代**        | `LLM`（文本补全）       | `PromptTemplate`     | 字符串 → 字符串         |
| **新时代（1.0）** | `ChatModel`（聊天模型） | `ChatPromptTemplate` | **消息列表** → 消息列表 |

**旧时代痛点**：手动拼接角色（如 `"Human: ...\nAI: ..."`），结构混乱，易混淆边界。
**新时代优势**：原生支持 `system/user/assistant` 角色，消息列表结构化，适合多轮对话与Agent。

------

### 2.3 ChatPromptTemplate 使用详解

#### 2.3.1 两种实例化方式

**方式1：`from_messages()`（推荐）**

python

```
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的AI机器人，你的名字是{name}。"),
    ("human", "你好，最近怎么样？"),
    ("ai", "我很好，谢谢！"),
    ("human", "{user_input}"),
])
prompt = chat_template.invoke({"name": "小明", "user_input": "你叫什么名字？"})
```



**方式2：直接初始化**

python

```
prompt_template = ChatPromptTemplate([
    ("system", "你是一个AI开发工程师。你的名字是{name}。"),
    ("human", "{user_input}")
])
```



#### 2.3.2 模板调用的三种方式

| 方法                | 返回类型            | 说明                                      |
| :------------------ | :------------------ | :---------------------------------------- |
| `invoke()`          | `ChatPromptValue`   | 包含消息列表，可直接传入 `model.invoke()` |
| `format()`          | `str`               | 返回纯字符串（不常用，失去角色信息）      |
| `format_messages()` | `list[BaseMessage]` | 返回消息列表                              |

**推荐使用 `invoke()`**，因为它返回的 `ChatPromptValue` 可直接用于模型调用。

#### 2.3.3 结合LLM调用完整示例

python

```
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

model = init_chat_model(model="gpt-5.4-mini", model_provider="openai", ...)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个数学家，你可以计算任何算式"),
    ("human", "{text}"),
])

prompt_value = chat_prompt.invoke({"text": "我今年18岁，舅舅38岁，我和舅舅一共多少岁？"})
output = model.invoke(prompt_value)
print(output.content)
```



#### 2.3.4 更丰富的初始化参数类型

`from_messages()` 的 `messages` 参数可以是以下类型的**序列**：

| 类型                       | 示例                                             | 说明                               |
| :------------------------- | :----------------------------------------------- | :--------------------------------- |
| **str**                    | `"Hello, {name}!"`                               | 默认为 human 角色                  |
| **tuple**                  | `("system", "你是{role}")`                       | 最常用                             |
| **dict**                   | `{"role": "system", "content": "你是{role}"}`    | 字典形式                           |
| **BaseMessage**            | `SystemMessage(content="...")`                   | 已实例化的消息（**不能含占位符**） |
| **MessagePromptTemplate**  | `SystemMessagePromptTemplate.from_template(...)` | 专用模板类                         |
| **BaseChatPromptTemplate** | 嵌套的 `ChatPromptTemplate`                      | 模板嵌套                           |

**MessagePromptTemplate 示例**：

python

```
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

system_prompt = SystemMessagePromptTemplate.from_template("你是一个{role}")
human_prompt = HumanMessagePromptTemplate.from_template("给我解释{concept}")

chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
```



------

### 2.4 高级特性

#### 2.4.1 部分变量预填充（`partial()`）

用于固定某些变量，生成模板变体。

python

```
base_template = ChatPromptTemplate.from_messages([
    ("system", "你是{department}的{role}"),
    ("user", "{task}")
])

# 为IT部门创建专用模板
it_template = base_template.partial(department="IT部门", role="技术支持")
messages = it_template.invoke({"task": "重置密码"})
```



#### 2.4.2 消息占位符（`MessagesPlaceholder`）

用于在模板中**插入动态消息列表**（如对话历史、中间步骤）。

**方式1：`"placeholder"` 字符串**

python

```
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的AI助手"),
    ("placeholder", "{conversation}"),
])
prompt = template.invoke({
    "conversation": [
        ("human", "你好！"),
        ("ai", "今天我能帮你做什么？"),
    ]
})
```



**方式2：`MessagesPlaceholder` 对象（推荐）**

python

```
from langchain_core.prompts import MessagesPlaceholder

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个非常友好的AI助手"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

prompt = prompt_template.invoke({
    "history": [
        ("human", "5 + 2 = ?"),
        ("ai", "5 + 2 = 7"),
    ],
    "question": "结果再乘以4呢？"
})
```



#### 2.4.3 可复用模板库

将模板集中管理，便于复用。

python

```
# templates.py
class PromptLibrary:
    TRANSLATOR = ChatPromptTemplate.from_messages([
        ("system", "你是专业翻译，精通{source_lang}和{target_lang}"),
        ("user", "翻译以下文本：\n{text}")
    ])
    CODE_REVIEWER = ChatPromptTemplate.from_messages([...])

# 使用
from templates import PromptLibrary
messages = PromptLibrary.TRANSLATOR.format_messages(
    source_lang="英语", target_lang="中文", text="Hello world"
)
```



#### 2.4.4 模板组合

通过字符串拼接或 `+` 运算符组合多个模板。

python

```
template1 = ChatPromptTemplate.from_messages([("system", "你是助手")])
template2 = ChatPromptTemplate.from_messages([("user", "{input}")])
combined = template1 + template2
```



------

## 3. 总结与最佳实践

| 知识点         | 要点                                              |
| :------------- | :------------------------------------------------ |
| **消息类型**   | System / Human / AI / Tool，明确角色区分          |
| **消息格式**   | 优先使用对象格式（`SystemMessage` 等）            |
| **对话历史**   | 每次调用必须传递完整历史，并保存AI回复            |
| **历史优化**   | 保留System + 最近N轮对话，节省Token               |
| **多模态**     | 使用 `content_blocks` 统一处理图片、音频等        |
| **思维链**     | 优先读取 `response.content_blocks` 获取 reasoning |
| **提示词模板** | 正式项目必须使用 `ChatPromptTemplate`             |
| **模板调用**   | 推荐 `invoke()` 返回 `ChatPromptValue`            |
| **占位符**     | 使用 `MessagesPlaceholder` 插入动态消息列表       |
| **复用**       | 建立模板库，避免重复定义                          |

------

**最终建议**：

- 小Demo可用字符串，**生产项目必用 ChatPromptTemplate**
- 多轮对话务必管理历史，并考虑裁剪策略
- 多模态或需要思维链时，善用 `content_blocks`
- 模板库 + 占位符 是构建复杂Agent的基石

LangChain工具笔记



详细总结一下，我需要一份笔记

我们根据提供的PDF内容，详细总结一份关于LangChain中Tools的笔记。内容涵盖工具的重要性、定义方式、参数说明、应用案例、强制使用工具、实践经验等。需要结构化、清晰、完整。

# LangChain Tools 详解笔记

> 基于尚硅谷教程整理 | 讲师：宋红康

------

## 一、Tools 概述

### 1.1 工具的重要性

- 大模型（LLM）本身只能“认识世界”（生成文本），无法“改变世界”（执行外部操作）。
- **工具（Tools）** 赋予 LLM 与外部世界交互的能力，如：
  - 搜索、计算、数据库查询
  - 邮件发送、调用第三方 API
- 工具是构建智能体（Agent）的**核心要素**。

### 1.2 工具调用的两种方式

| 方式           | 说明                                                   | 适用场景     |
| :------------- | :----------------------------------------------------- | :----------- |
| **直接调用**   | 使用 `.invoke()` 手动调用工具函数                      | 测试、验证   |
| **绑定到模型** | 通过 `model.bind_tools([工具])` 让 AI 自主决定是否调用 | 开发生产环境 |

**示例（直接调用）**

python

```
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    return f"{city}晴天，温度15°C"

result = get_weather.invoke({"city": "北京"})
print(result)  # 北京晴天，温度15°C
```



**示例（绑定到模型）**

python

```
model_with_tools = model.bind_tools([get_weather])
response = model_with_tools.invoke("北京天气如何？")
if response.tool_calls:
    print("AI想调用工具：", response.tool_calls)
```



### 1.3 工具调用的完整流程

1. **模型绑定工具**：`model.bind_tools([tool1, tool2])`
2. **模型生成工具调用请求**：用户输入 → 模型返回 `AIMessage`，其中包含 `tool_calls`（工具名+参数）
3. **开发者手动执行工具**：从响应中提取 `tool_calls`，调用对应工具（如 `tool.invoke(tool_call)`）
4. **将工具结果（`ToolMessage`）传回模型**：模型结合工具结果生成最终回复

> ⚠️ **注意**：大模型调用工具是**单次推理**，不会自动循环执行，需要开发者手动管理循环。

------

## 二、Message 流转视角下的工具调用

### 不使用 `@tool` 装饰器（手动拼接）

python

```
from langchain.messages import HumanMessage, ToolMessage

def get_weather(city: str):
    return f"{city}天气晴朗"

model_with_tools = model.bind_tools([get_weather])
messages = [HumanMessage("今天北京天气如何")]

response = model_with_tools.invoke(messages)
messages.append(response)

for tool_call in response.tool_calls:
    if tool_call["name"] == "get_weather":
        tool_response = ToolMessage(
            content=get_weather(**tool_call["args"]),
            tool_call_id=tool_call["id"],
            name=tool_call["name"]
        )
        messages.append(tool_response)

final_response = model_with_tools.invoke(messages)
```



### 使用 `@tool` 装饰器（自动生成 `ToolMessage`）

python

```
@tool
def get_weather(city: str):
    """获取天气的工具"""
    return f"{city}天气晴朗~"

model_with_tools = model.bind_tools([get_weather])
# ... 相同流程，但执行工具时：
tool_response = get_weather.invoke(tool_call)  # 直接返回 ToolMessage 实例
```



**关键区别**：被 `@tool` 修饰的函数调用 `.invoke()` 会返回 `ToolMessage`，无需手动拼接。

------

## 三、工具的定义方式

### 方式一：不使用 `@tool` 装饰器

#### 3.1 基本定义

python

```
def get_weather(city: str):
    return f"{city}天气晴朗"
```



底层通过 `convert_to_openai_tool` 转换为标准工具描述。

#### 3.2 工具描述详解

使用 `convert_to_openai_tool` 查看解析结果：

python

```
from langchain_core.utils.function_calling import convert_to_openai_tool
print(convert_to_openai_tool(get_weather))
```



**输出字段说明**：

| 字段                    | 说明                           |
| :---------------------- | :----------------------------- |
| `type`                  | 固定为 `"function"`            |
| `function.name`         | 函数名                         |
| `function.description`  | 从 docstring 提取              |
| `function.parameters`   | JSON Schema 格式的参数定义     |
| `parameters.properties` | 每个参数的名称、类型、描述     |
| `parameters.required`   | 必填参数列表（无默认值的参数） |

**Description 来源**：

- 从函数的 **docstring** 加载

- docstring 建议遵循 **Google 风格**：

  python

  ```
  def get_weather(city: str):
      """
      天气查询工具
      Args:
          city: 城市名称
      Returns:
          天气信息字符串
      """
      return f"{city}天气晴朗"
  ```

  

**参数类型**：通过函数的 **类型注解**（Type Hints）推断。

- 有类型注解 → 在 `properties` 中显示 `"type": "string"`
- 无类型注解 → 参数信息为空对象 `{}`

**参数默认值**：

- 无默认值 → 出现在 `required` 列表中
- 有默认值 → 在 `properties` 中显示 `"default": "值"`，且不会出现在 `required` 中

------

### 方式二：使用 `@tool` 装饰器（推荐）

#### 3.3 基本用法

python

```
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """天气查询工具"""
    return f"{city}天气晴朗"
```



> 必须提供 docstring，否则报错。

#### 3.4 自定义描述（`description`）

python

```
@tool(description="根据城市名称查询当日天气的工具")
def get_weather(city: str):
    """天气查询工具"""
    return f"{city}天气晴朗"
```



优先级高于 docstring。

#### 3.5 解析 docstring（`parse_docstring=True`）

python

```
@tool(parse_docstring=True)
def get_weather(city: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """
    获取当日天气，可选择是否同时查询未来五日天气预报
    Args:
        city: 城市
        units: 气温单位，可选：celsius-摄氏度，fahrenheit-华氏度
        include_forecast: 是否包含未来五日的天气预报
    """
    # 实现...
```



此时参数描述会从 docstring 中提取，而非整体作为 description。

#### 3.6 自定义工具名称（`name_or_callable`）

python

```
@tool("getweather")  # 或 @tool(name_or_callable="getweather")
def get_weather(city: str):
    ...
```



一般不推荐自定义，保持函数名即可。

#### 3.7 自定义参数模式（`args_schema`）

**方式①：使用 Pydantic 模型**

python

```
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    city: str = Field(default="北京", description="城市")
    unit: Literal["celsius", "fahrenheit"] = Field(default="celsius", description="气温单位")
    include_forecast: bool = Field(default=False, description="是否包含未来五日天气预报")

@tool(args_schema=WeatherInput)
def get_weather(city: str, unit: str = "celsius", include_forecast: bool = False) -> str:
    """获取当日天气，可选未来五日天气预报"""
    # 实现...
```



- Pydantic 提供**类型验证**和**枚举限制**
- `Field()` 可设置 `default`、`description` 等
- `Literal` 限定固定选项

**方式②：使用 JSON Schema 字典**

python

```
weather_schema = {
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "units": {"type": "string"},
        "include_forecast": {"type": "boolean"}
    },
    "required": ["location", "units", "include_forecast"]
}

@tool(args_schema=weather_schema)
def get_weather(city: str, unit: str = "celsius", include_forecast: bool = False) -> str:
    ...
```



适合参数结构需要**动态生成**的场景。

------

## 四、工具的应用案例

### 4.1 使用 `args_schema` 示例

python

```
class WeatherSchema(BaseModel):
    city: str = Field(default="北京", description="城市名称")
    if_forecast: bool = Field(default=False, description="是否包含明日天气预报")

@tool("get_weather_and_forecast", description="查询当日天气，可以包含明日天气预报", args_schema=WeatherSchema)
def get_weather(city: str, if_forecast: bool):
    res = f"{city} 今天天气不错"
    if if_forecast:
        res += "\n明天也不错"
    return res
```



### 4.2 使用 `parse_docstring` 示例

python

```
@tool("get_weather_and_forecast", parse_docstring=True)
def get_weather(city: str = "北京", if_forecast: bool = False):
    """
    查询当日天气，可以包含明日天气预报
    Args:
        city: 城市名称
        if_forecast: 是否包含明日天气预报
    """
    res = f"{city} 今天天气不错"
    if if_forecast:
        res += "\n明天要下雨"
    return res
```



### 4.3 多工具调用（管理循环）

python

```
tools = [get_stock_price, search_news]
model_with_tools = model.bind_tools(tools)

message_list = [HumanMessage("苹果公司今天的股价是多少？最近有什么新闻？")]

while True:
    response = model_with_tools.invoke(message_list)
    message_list.append(response)
    if not response.tool_calls:
        break
    for tool_call in response.tool_calls:
        if tool_call["name"] == "get_stock_price":
            result = get_stock_price.invoke(tool_call)
            message_list.append(result)
        elif tool_call["name"] == "search_news":
            result = search_news.invoke(tool_call)
            message_list.append(result)

final_response = model_with_tools.invoke(message_list)
```



**关键**：`while True` 循环处理多次工具调用，直到模型不再需要调用工具。

------

## 五、强制使用工具（`tool_choice`）

`bind_tools()` 支持 `tool_choice` 参数，控制模型是否必须调用工具。

| 取值                                               | 行为                                 |
| :------------------------------------------------- | :----------------------------------- |
| `"none"`                                           | 模型不会调用任何工具，直接生成文本   |
| `"auto"`                                           | **默认值**，模型自主决定是否调用工具 |
| `"required"`                                       | 模型必须调用至少一个工具             |
| `"any"`                                            | 等同于 `"required"`                  |
| `{"type":"function","function":{"name":"工具名"}}` | 强制调用指定工具                     |

**示例：强制调用特定工具**

python

```
model_with_tools = model.bind_tools(
    [get_weather1, get_weather2],
    tool_choice="get_weather2"   # 强制使用 get_weather2
)
```



此时即使问题更适合 `get_weather1`，模型也会调用 `get_weather2`。

------

## 六、实践经验总结

### 1. 清晰的描述

- 工具名称、docstring、参数描述要**准确明确**
- 大模型依赖这些文本理解工具的用途

### 2. 功能单一

- ✅ 每个工具只做一件事
- ❌ 避免一个工具包含多个分支逻辑（如 if action=="weather" ...）

### 3. 如何处理工具失败？

三层防护：

- **工具内部**：`try-except` 捕获异常，返回友好错误信息

- **Agent 级重试**：通过 prompt 提示模型尝试其他方法

- **调用级重试**：使用 `tenacity` 库的 `@retry` 装饰器

  python

  ```
  from tenacity import retry, stop_after_attempt
  
  @retry(stop=stop_after_attempt(3))
  def call_agent(question):
      return agent.invoke({"messages": [{"role": "user", "content": question}]})
  ```

  

### 4. 返回字符串（而非字典）

- ✅ 工具返回 `str` 类型，并尽量用 `json.dumps(..., ensure_ascii=False)` 序列化
- ❌ 避免直接返回 `dict`，可能导致编码问题或模型理解困难

### 5. 同步 vs 异步

- **同步**：简单场景、CPU 密集型任务

- **异步**：IO 密集型（API 调用、数据库、文件操作）

  python

  ```
  @tool
  async def async_tool(x: str) -> str:
      return await async_process(x)
  ```

  

------

## 七、核心概念速查

| 概念                     | 说明                                             |
| :----------------------- | :----------------------------------------------- |
| `@tool`                  | 装饰器，将普通函数转为工具                       |
| `bind_tools()`           | 将工具绑定到模型                                 |
| `tool_calls`             | `AIMessage` 中的属性，包含模型请求调用的工具列表 |
| `ToolMessage`            | 工具执行后返回的消息类型                         |
| `convert_to_openai_tool` | 查看工具被解析后的 OpenAPI 格式                  |
| `args_schema`            | 自定义参数模式（Pydantic 或 JSON Schema）        |
| `parse_docstring`        | 是否从 docstring 解析参数描述                    |
| `tool_choice`            | 控制模型是否/必须调用工具                        |

------

> **总结**：工具是 LangChain 智能体的基石，合理定义工具（清晰的描述、单一职责、健壮的错误处理）能显著提升 AI 应用的可靠性。开发中推荐使用 `@tool` 装饰器 + Pydantic `args_schema` 的方式，既保证类型安全，又便于大模型理解。

LangChain结构化输出笔记

我们根据提供的PDF文件内容，详细总结一份关于LangChain结构化输出的笔记。内容要全面，包括概述、四种模式（Pydantic、TypedDict、JSON Schema、@dataclass）、高级特性、类型校验对比、获取结构化结果方式等。注意笔记要清晰有条理，适合学习参考。

我将按照PDF的结构来组织，但会加以整理和提炼，加入自己的理解。输出格式为Markdown。

# LangChain 结构化输出完整笔记

> 基于尚硅谷课程《06-结构化输出》整理
> 讲师：宋红康
> 目标：将大模型的“自然语言回答”转化为“程序可稳定消费的数据”

------

## 一、结构化输出概述

### 1.1 什么是结构化输出

结构化输出指要求 LLM 最终返回一个**符合预定义结构**的数据对象，例如固定字段的 JSON、Pydantic 模型、TypedDict 等，而非无格式的自然语言文本。

**对比示例：**

- ❌ 非结构化：`"盗梦空间在2010年上映，导演是克里斯托弗·诺兰，评分9.3。"`
- ✅ 结构化：

json

```
{
  "title": "盗梦空间",
  "year": 2010,
  "director": "克里斯托弗·诺兰",
  "rating": 9.3
}
```



**三大价值：**

1. **易于代码处理** – 下游系统可直接读字段，无需再解析自然语言
2. **结果更稳定** – 减少“模型说法变了但意思差不多”导致的解析失败
3. **适合工程化** – 表单抽取、分类、路由、工具参数生成、工作流状态传递等

------

### 1.2 传统方式 vs 结构化输出

**传统方式（繁琐，不推荐）：**

python

```
# 1. 提示词要求 JSON
prompt = "以JSON格式返回: {name, age, occupation}"
response = model.invoke(prompt)

# 2. 手动解析
import json
data = json.loads(response.content)

# 3. 手动验证类型
if not isinstance(data['age'], int):
    raise ValueError("age must be int")

# 4. 手动创建对象
person = Person(**data)
```



**结构化输出（简洁）：**

python

```
structured_llm = model.with_structured_output(Person)
person = structured_llm.invoke("张三是一名30岁的软件工程师")
# 自动解析、验证、创建对象
```



**为什么受欢迎？**

- Prompt 变干净：字段的 `description` 直接充当 Prompt 的一部分
- 类型安全：编辑器自动补全，运行前类型检查
- 极其稳定：依托大模型底层的 JSON 模式，输出错误率极低

------

### 1.3 支持的结构化输出模式

LangChain 1.x 支持以下 Schema 类型：

| 模式                   | 返回类型                   | 是否校验 | 推荐度         |
| :--------------------- | :------------------------- | :------- | :------------- |
| **Pydantic BaseModel** | 类实例（如 `Person` 对象） | ✅ 强校验 | ⭐⭐⭐⭐⭐ 生产首选 |
| **TypedDict**          | 字典（dict）               | ❌ 不校验 | ⭐⭐⭐⭐ 轻量场景  |
| **JSON Schema**        | 字典（dict）               | ❌ 不校验 | ⭐⭐ 跨语言接口  |
| **@dataclass**         | 字典（dict）               | ❌ 不校验 | ⭐⭐⭐ 简洁定义   |

> **注意：** 只有 Pydantic 返回的是 Schema 类实例，其余三种返回字典；只有 Pydantic 在类型不匹配时抛出异常。

------

### 1.4 模型兼容性

**支持** 结构化输出（通过函数调用/工具调用）：

- OpenAI（gpt-4, gpt-3.5-turbo）
- Anthropic（claude-3）
- Groq（llama-3）
- 大部分现代模型

**不支持** 时，LangChain 会自动回退到“提示词 + JSON 解析”方式。

------

## 二、四种模式的使用详解

### 2.1 模式1：Pydantic（生产环境首选）

#### 2.1.1 基本使用

**必备要素：**

- 所有模型必须继承 `BaseModel`
- 使用类型提示（`str`, `int`, `float`, `List[xxx]`, `Optional[xxx]` 等）
- 使用 `Field(description="...")` 添加描述，帮助 LLM 理解字段含义

**示例1：人物信息提取**

python

```
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

# 1. 初始化模型
model = init_chat_model(
    model="gpt-4-mini",
    model_provider="openai",
    api_key=CLOSEAI_API_KEY,
    base_url=CLOSEAI_BASE_URL
)

# 2. 定义 Pydantic 模型
class Person(BaseModel):
    """人物信息"""
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")
    occupation: str = Field(description="职业")

# 3. 绑定结构化输出
structured_llm = model.with_structured_output(Person)

# 4. 调用
result = structured_llm.invoke("张三是一名30岁的软件工程师")
print(result.name)       # 张三
print(result.age)        # 30
print(result.occupation) # 软件工程师
print(type(result))      # <class '__main__.Person'>
```



**示例2：电影信息提取**

python

```
class MovieModel(BaseModel):
    title: str = Field(description="电影标题")
    year: int = Field(description="电影上映年份")
    director: str = Field(description="导演")
    rating: float = Field(description="电影评分，满分十分")

model_with_structure = model.with_structured_output(MovieModel)
response = model_with_structure.invoke("给出盗梦空间的信息")
print(response)  # title='盗梦空间' year=2010 director='克里斯托弗·诺兰' rating=9.3
```



**示例3：情感分析**

python

```
class SentimentAnalysis(BaseModel):
    sentiment: str = Field(description="情感倾向：positive/negative/neutral")
    confidence: float = Field(description="置信度，0-1之间")
    keywords: list[str] = Field(description="关键词列表")

structured_model = model.with_structured_output(SentimentAnalysis)
text = "这个课程内容很实用，学到了很多知识，强烈推荐！"
result = structured_model.invoke(f"分析以下文本的情感：\n{text}")
print(result.sentiment)   # positive
print(result.confidence)  # 0.99
print(result.keywords)    # ['实用', '学到了很多知识', '强烈推荐']
```



------

#### 2.1.2 高级特性

##### (1) 可选字段 – `Optional`

当 LLM 可能无法提供某些字段时，用 `Optional` 避免报错。

python

```
from typing import Optional

class Person(BaseModel):
    name: str = Field(description="姓名")
    age: Optional[int] = Field(description="年龄")   # 可缺失
    occupation: str = Field(description="职业")

result = structured_llm.invoke("张三是一名医生")
# Person(name='张三', age=None, occupation='医生')
```



##### (2) 默认值 – `Field(default=...)`

LLM 未提供时使用默认值（**注意：不同模型对 default 支持不同**）。

python

```
class Person(BaseModel):
    name: str = Field(description="姓名")
    age: int = Field(1, description="年龄")      # 默认 1
    occupation: str = Field(description="职业")
```



- 使用 OpenAI 平台时，若 LLM 未提供 age，可能输出 0（非预期）
- 使用 OpenRouter 平台时，可能正确输出默认值 1
  👉 **建议：不要过度依赖默认值，尽量让 LLM 从上下文推断，或使用 Optional**

**示例：配置信息提取**

python

```
class Config(BaseModel):
    timeout: Optional[int] = Field(30, description="超时时间(单位秒)")
    retry: bool = Field(False, description="是否支持重试")
    max_attempts: int = Field(6, description="最大重试次数")

structured_llm = model.with_structured_output(Config)
result = structured_llm.invoke("配置要求：支持重试，最多重试5次")
# Config(timeout=None, retry=True, max_attempts=5)
```



##### (3) 枚举类型 – `Enum` 或 `Literal`

限制字段的可选值，保证输出规范性。

**方式一：使用 Enum**

python

```
from enum import Enum

class Priority(str, Enum):
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"

class CustomerInfo(BaseModel):
    name: str = Field(description="客户姓名")
    phone: str = Field(description="电话号码")
    email: Optional[str] = Field(description="邮箱")
    issue: str = Field(description="问题描述")
    urgency: Priority = Field(description="紧急程度")   # 只能是低/中/高
```



**方式二：使用 Literal（更简洁）**

python

```
from typing import Literal

class CustomerInfo(BaseModel):
    name: str = Field(description="客户姓名")
    phone: str = Field(description="电话号码")
    email: Optional[str] = Field("未提供", description="邮箱")
    issue: str = Field(description="问题描述")
    urgency: Literal["低", "中", "高"] = Field(description="紧急程度")
```



**应用场景：** CRM 自动填充、工单自动分类、客服辅助

##### (4) 列表提取 – `List[Model]`

提取多条信息，返回列表。

python

```
from typing import List

class Person(BaseModel):
    name: str
    age: int

class PersonList(BaseModel):
    people: List[Person]

structured_llm = model.with_structured_output(PersonList)
result = structured_llm.invoke("张三30岁，李四25岁")
# people=[Person(name='张三', age=30), Person(name='李四', age=25)]
```



**应用场景：** 批量评论分析、文档信息提取（如发票商品列表）

##### (5) 嵌套结构 – `Model` 内部包含 `Model`

python

```
class Address(BaseModel):
    city: str
    district: str

class Company(BaseModel):
    name: str
    address: Address   # 嵌套

structured_llm = model.with_structured_output(Company)
result = structured_llm.invoke("阿里巴巴在杭州滨江区")
# name='阿里巴巴' address=Address(city='杭州', district='滨江区')
```



**更复杂示例（电影 + 演员列表）：**

python

```
class Actor(BaseModel):
    name: str = Field(description="演员姓名")
    role: str = Field(description="饰演的角色")

class Movie(BaseModel):
    title: str = Field(description="电影标题")
    year: int = Field(description="上映年份")
    director: str = Field(description="导演")
    cast: List[Actor] = Field(description="演员列表")
    rating: float = Field(description="评分")

structured_model = model.with_structured_output(Movie)
response = structured_model.invoke("请介绍电影《盗梦空间》")
# 自动填充完整的演员列表
```



> **建议：** 嵌套层级 ≤ 3 层，使用清晰的 `description`，必要时拆分成多个调用。

##### (6) 限制条件 – `Field` 参数校验

在 Pydantic 中可以使用 `min_length`, `max_length`, `ge`, `le`, `gt`, `lt` 等约束。

python

```
class User(BaseModel):
    name: str = Field(min_length=2, max_length=20)
    age: int = Field(ge=0, le=150)
    email: str

# 有效数据通过，无效数据抛出 ValidationError
```



**注意：** 这些约束是 **Pydantic 层面的校验**，LLM 本身可能生成不符合的值，但 Pydantic 会捕获并抛出异常。使用不同平台时表现可能不同（如 OpenRouter 可能自动修正为合理值，而 CloseAI 可能原样输出再报错）。

------

#### 2.1.3 工作流程图解

1. **定义结构** – 编写 Pydantic 类（继承 BaseModel）
2. **协议转换** – LangChain 调用 `model_json_schema()` 将 Python 代码转为 JSON Schema
3. **模型交互与强约束** – JSON Schema 作为 Tools 传入大模型 API，开启 `strict=True` 等模式，约束生成 token
4. **自动解析与验证** – 返回 JSON 字符串 → 解析为字典 → Pydantic 校验 → 返回类实例

------

### 2.2 模式2：TypedDict

#### 2.2.1 什么是 TypedDict

Python 3.8+ 的类型提示工具，为字典提供“结构声明”，**只在静态类型检查时生效，运行时无校验**。

python

```
from typing_extensions import TypedDict, Annotated

class MovieDict(TypedDict):
    title: str
    year: int
    director: str
    rating: float
```



#### 2.2.2 使用方式

与 Pydantic 类似，用 `with_structured_output` 绑定，但返回的是 **字典**，不做校验。

**简单示例：**

python

```
from typing_extensions import TypedDict, Annotated

class MovieTypedDict(TypedDict):
    title: Annotated[str, "电影的正式名称"]
    year: Annotated[int, "电影的公映年份"]
    director: Annotated[str, "电影导演的全名"]
    rating: Annotated[float, "电影在10分制下的评分"]

structured_llm = model.with_structured_output(MovieTypedDict)
response = structured_llm.invoke("给我介绍下电影《星际穿越》")
print(type(response))  # <class 'dict'>
print(response)        # {'title': '星际穿越', 'year': 2014, ...}
```



**嵌套结构：**

python

```
class Actor(TypedDict):
    name: Annotated[str, "演员姓名"]
    role: Annotated[str, "饰演的角色"]

class Movie(TypedDict):
    title: Annotated[str, "电影标题"]
    year: Annotated[int, "上映年份"]
    director: Annotated[str, "导演"]
    cast: Annotated[List[Actor], "演员列表"]
    rating: Annotated[float, "评分"]

response = structured_llm.invoke("给我介绍下电影《盗梦空间》")
print(response['cast'])  # 返回列表字典
```



#### 2.2.3 关于 `...` (Ellipsis) 的用法

在 `Annotated` 中，`...` 表示该字段为 **必填**。

python

```
class MovieDict(TypedDict):
    title: Annotated[str, ..., "电影标题"]      # 必填
    year: Annotated[int, ..., "电影上映年份"]   # 必填
    director: Annotated[str, ..., "导演"]       # 必填
    rating: Annotated[float, "电影评分"]        # 可选（无...）
```



- 若 LLM 未提供必填字段，返回的字典中该字段会存在但值为空字符串
- 若 LLM 未提供可选字段，该字段可能直接被省略

------

### 2.3 模式3：JSON Schema（不推荐）

直接编写 JSON Schema 字典，繁琐且无校验。

python

```
json_schema = {
    "title": "Movie",
    "description": "A movie with details",
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "The title of the movie"},
        "year": {"type": "integer", "description": "The year the movie was released"},
        "director": {"type": "string", "description": "The director of the movie"},
        "rating": {"type": "number", "description": "The movie's rating out of 10"}
    },
    "required": ["title", "year", "director", "rating"]
}

structured_model = model.with_structured_output(json_schema, method="json_schema")
response = structured_model.invoke("给出盗梦空间的信息")
# 返回字典，无校验
```



**说明：**

- `method="json_schema"` 表示使用模型供应商的专用结构化输出功能（不是所有模型都支持）
- `title`, `description`, `type`, `properties`, `required` 是 JSON Schema 标准关键字
- 返回字典，无类型校验

------

### 2.4 模式4：@dataclass

Python 标准库 `dataclasses` 的装饰器，用于简洁定义数据类。

python

```
from dataclasses import dataclass
from pydantic import Field

@dataclass
class Movie:
    """电影的详细信息"""
    title: str = Field(description="电影标题")
    year: int = Field(description="电影上映年份")
    director: str = Field(description="导演")
    rating: float = Field(description="电影评分，满分十分")

structured_model = model.with_structured_output(Movie)
response = structured_model.invoke("给出盗梦空间的信息")
print(type(response))  # <class 'dict'>
```



**注意：**

- 返回的是 **字典**，不是类实例
- **无校验**
- 必须使用 `@dataclass` 装饰（手写 `__init__` 的普通类不能作为 Schema）

------

## 三、类型校验对比（关键差异）

通过伪造服务器返回字段名不匹配的数据（如 `title1` 代替 `title`），观察四种模式的行为。

| 模式            | 返回类型 | 字段不匹配时行为           |
| :-------------- | :------- | :------------------------- |
| **Pydantic**    | 类实例   | **抛出 ValidationError** ❌ |
| **TypedDict**   | 字典     | 原样返回，不报错 ✅         |
| **JSON Schema** | 字典     | 原样返回，不报错 ✅         |
| **@dataclass**  | 字典     | 原样返回，不报错 ✅         |

**结论：** 若你需要 **强校验**，确保下游数据绝对正确，请使用 **Pydantic**；若你更看重灵活性且能接受脏数据，可选择其他三种。

------

## 四、获取结构化结果的两种方式

### 4.1 方式一：`with_structured_output`（推荐）

简洁、直接，是 LangChain 最新推荐的 API。

**基本用法：**

python

```
structured_llm = model.with_structured_output(SomeSchema)
result = structured_llm.invoke("用户输入")
```



**获取原始响应与元数据（`include_raw=True`）：**

python

```
structured_llm = model.with_structured_output(Movie, include_raw=True)
resp = structured_llm.invoke("给我介绍下电影《星际穿越》")

print(resp['raw'])          # 原始 AIMessage 对象（包含 token 用量等）
print(resp['parsed'])       # 解析后的对象（若校验通过）
print(resp['parsing_error']) # 解析错误（若有）
```



返回的字典包含三个字段：

- `raw`：原始 `AIMessage`，包含 `response_metadata`, `usage_metadata` 等
- `parsed`：解析后的 Pydantic 实例（或其他类型的字典）
- `parsing_error`：解析错误信息（仅 Pydantic 会报错，其他方式为 None）

------

### 4.2 方式二：输出解析器（不推荐）

传统方法：在 Prompt 中明确要求输出特定格式，然后使用 `JsonOutputParser` 转换。

python

```
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

# 1. 定义 Prompt
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "回答用户问题,必须始终输出一个包含title和year的JSON对象"),
    ("human", "问题: {question}")
])

# 2. 定义 Schema
class Movie(BaseModel):
    title: str = Field(description="电影标题")
    year: int = Field(description="上映年份")

# 3. 创建解析器
parser = JsonOutputParser(pydantic_object=Movie)

# 4. 构建链
chain = prompt_template | model | parser

# 5. 调用
response = chain.invoke({"question": "介绍电影《盗梦空间》"})
print(response)  # 返回字典
```



**缺点：**

- 依赖提示词质量，LLM 可能不遵守
- 无强校验
- 流程冗长

------

## 五、总结与最佳实践

| 场景                             | 推荐方案                                             |
| :------------------------------- | :--------------------------------------------------- |
| 生产环境，需要强类型校验         | **Pydantic**                                         |
| 快速原型，结构简单，能容忍脏数据 | **TypedDict** 或 **@dataclass**                      |
| 跨语言接口对接，已有 JSON Schema | **JSON Schema**（但注意无校验）                      |
| 需要获取 token 用量等元数据      | 使用 `with_structured_output(..., include_raw=True)` |
| 简单实验，不想定义 Schema        | 直接提示词 + `json.loads()`（不推荐生产）            |

**关键要点：**

1. **Pydantic 是生产首选** – 类型安全 + 自动校验 + 自动补全
2. 字段的 `description` 是给 LLM 看的，一定要写清楚
3. 使用 `Optional` 处理可能缺失的字段
4. 嵌套结构不超过 3 层，并配合清晰描述
5. 不同模型平台对 `default`、校验行为的支持有差异，测试时需留意
6. `with_structured_output` 是现代方式，输出解析器已是“过去式”

------

> 以上笔记基于尚硅谷课程内容整理，涵盖了 LangChain 结构化输出的核心知识点与实战技巧。建议结合代码反复练习，加深理解。

本回答由 AI 生成，内容仅供参考，请仔细甄别

智能体开发笔记



详细总结一下，我需要一份笔记

我们根据提供的PDF文件内容，整理一份详细的笔记。内容涵盖智能体概念、创建与调用、基本用法、高级用法、流式输出、实战等。按章节结构清晰总结，提取关键点。

由于内容很多，要精简但全面。可以按目录组织：

1. 理解Agents
2. Agent的基本用法1：模型的传入方式
3. Agent的基本用法2：如何调用Agent
4. Agent的基本用法3：绑定工具
5. Agent的高级用法1：设置Agent名称
6. Agent的高级用法2：系统提示词
7. Agent的高级用法3：结构化输出
8. Agent的高级用法4：流式输出及模式
9. 实战：多功能智能助手

需要详细但条理清晰。我会逐节提炼核心概念、代码示例关键点、参数说明、注意事项等。

由于是笔记，可适当用列表、表格。

开始整理。

# LangChain Agent 智能体开发笔记（基于尚硅谷教程）

> 讲师：尚硅谷-宋红康
> 框架：LangChain 1.x（基于 LangGraph）
> 核心函数：`create_agent()`（统一入口，取代旧版多种 Agent）

------

## 1. 理解 Agents

### 1.1 什么是 Agent？

- 以大语言模型（LLM）为**推理与决策核心**，结合**记忆、工具调用、环境交互**能力，能够进行**规划决策**并执行复杂任务以实现目标的软件系统。
- Agent 的本质是 **LangGraph 的 `CompiledStateGraph`**（图结构执行流程）。

### 1.2 Agent 的核心组件

| 组件                 | 必要性       |
| :------------------- | :----------- |
| 行动（Action）       | **必须**     |
| 工具（Tool）         | 几乎总是存在 |
| 规划决策（Planning） | 有条件存在   |
| 记忆（Memory）       | 最容易被省略 |

------

## 2. Agent 基本用法 1：模型的传入方式

`create_agent()` 是 LangChain 1.2 构建 Agent 的核心方式。

### 完整参数

python

```
from langchain.agents import create_agent

agent = create_agent(
    model: str | BaseChatModel,          # 必需
    tools: List[BaseTool],               # 必需
    *,
    system_prompt: str = "",             # 系统提示词
    middleware: Sequence = (),           # 中间件
    interrupt_before: List[str] = None,  # 执行前中断（人机协作）
    interrupt_after: List[str] = None,   # 执行后中断
    debug: bool = False,
    name: str | None = None,             # Agent 名称
    response_format: ... = None          # 结构化输出
)
```



### 模型传入的两种方式

#### ① 传入模型字符串（自动创建模型对象）

python

```
agent = create_agent("deepseek-v4-flash")
```



#### ② 传入模型对象（推荐）

python

```
from langchain.chat_models import init_chat_model
model = init_chat_model("gpt-5.4-mini", model_provider="openai", api_key=..., base_url=...)
agent = create_agent(model=model)
```



------

## 3. Agent 基本用法 2：如何调用 Agent

### `agent.invoke()`

- **输入**：字典 `{"messages": [消息列表]}`
- **输出**：字典，包含 `messages` 字段（完整的消息历史）
- **最终答案**：`response['messages'][-1].content`

### 消息格式

支持 `role`：`"system"`, `"user"`, `"assistant"`, `"tool"`。

#### 示例

python

```
response = agent.invoke({
    "messages": [
        {"role": "system", "content": "你是一个小学数学老师..."},
        {"role": "user", "content": "100加上50等于多少？"}
    ]
})
final_answer = response['messages'][-1].content
```



------

## 4. Agent 基本用法 3：绑定工具

工具可以是**内置**或**自定义**的。Agent 根据工具的描述（docstring）决定调用哪个。

### 4.1 绑定单个工具

python

```
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"{city}天气晴朗，25℃"

agent = create_agent(model=model, tools=[get_weather])
```



### 4.2 绑定内置工具（如 TavilySearch）

python

```
from langchain_tavily import TavilySearch

web_search = TavilySearch(max_results=2)
agent = create_agent(model=model, tools=[web_search])
```



### 4.3 绑定多个工具

python

```
agent = create_agent(model=model, tools=[get_weather, get_news])
```



> **最佳实践**：2~5 个工具最佳，太多会混淆。

### 4.4 工具调用流程（ReAct 循环）

text

```
用户问题 → AI 思考 → 调用工具 → 观察结果 → 继续思考 → ... → 最终答案
```



- Agent 反复调用模型和工具，直到某次模型输出**不再包含 `tool_calls`** 则结束。

### 4.5 重试机制

- 当工具返回临时错误（如以 `"TEMP_UNAVAILABLE:"` 开头）时，可在系统提示词中指示 Agent 重试。
- 示例中 Agent 自动重试 3 次直到成功。

### 4.6 常见问题

| 问题               | 原因                     | 解决                                 |
| :----------------- | :----------------------- | :----------------------------------- |
| 如何选择工具？     | 依据工具的 docstring     | 编写清晰描述                         |
| 为什么不调用工具？ | 描述模糊或模型判断不需要 | 明确 docstring                       |
| 选错工具？         | 功能相似或工具太多       | 只给必要的工具，区分描述             |
| 如何限制调用次数？ | 默认无限制               | 通过 `config={"recursion_limit": 5}` |

------

## 5. Agent 高级用法 1：设置 Agent 名称

python

```
agent = create_agent(model=model, name="chat_assistant")
```



**用途**：

- 流式输出归因（多 Agent 场景）
- 消息身份标记
- 调试与 trace 可读性
- 组件化封装
- 前端展示与可观测性

------

## 6. Agent 高级用法 2：系统提示词

通过 `system_prompt` 参数设置，可以传 `str` 或 `SystemMessage`。

### 作用

- 定义 Agent 角色、行为准则、工具使用策略。

### 示例

python

```
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="""你是天气助手。
工作流程：
1. 理解城市查询
2. 使用 get_weather 获取数据
3. 简洁回答
输出格式：天气状况、温度、注意事项"""
)
```



------

## 7. Agent 高级用法 3：结构化输出

通过 `response_format` 参数让 Agent 返回结构化数据（Pydantic 模型、TypedDict、JSON Schema 等），而非自然语言。

### 7.1 模型 vs Agent 结构化输出对比

| 维度     | 模型结构化输出 | Agent 结构化输出        |
| :------- | :------------- | :---------------------- |
| 解析时机 | 每次模型调用   | 仅任务结束时            |
| 数据流转 | 模型→对象      | 模型→工具→反思→...→对象 |
| 适用场景 | 单次确定性任务 | 多步复杂推理            |

### 7.2 四种策略

#### ① ProviderStrategy（使用模型原生结构化输出）

- 适用于 OpenAI、Anthropic Claude 等支持原生结构化输出的模型。

python

```
from langchain.agents.structured_output import ProviderStrategy
agent = create_agent(model=model, response_format=ProviderStrategy(ContactInfo))
```



#### ② ToolStrategy（通过工具调用模拟）

- 兼容大多数支持工具调用的模型，**推荐使用**。

python

```
from langchain.agents.structured_output import ToolStrategy
agent = create_agent(model=model, response_format=ToolStrategy(ContactInfo))
```



#### ③ AutoStrategy（自动选择）

- 直接传入 Schema 类型，LangChain 自动选择 ProviderStrategy 或 ToolStrategy。

python

```
agent = create_agent(model=model, response_format=ContactInfo)  # 但 LangChain 1.2 可能已弃用此写法
```



#### ④ None（默认，自然语言输出）

### 7.3 ToolStrategy 详解

#### 参数

- `schema`（必需）：Pydantic、TypedDict、JSON Schema、dataclass，或 `Union[类型1, 类型2]`
- `tool_message_content`（可选）：自定义成功后的 ToolMessage 内容（节省 token，更友好）
- `handle_errors`（可选）：错误处理策略

#### 支持的 Schema 示例

| 类型        | 示例                                |
| :---------- | :---------------------------------- |
| Pydantic    | `class ContactInfo(BaseModel): ...` |
| TypedDict   | `class ContactInfo(TypedDict): ...` |
| JSON Schema | 字典格式遵循 JSON Schema 规范       |
| dataclass   | `@dataclass class ContactInfo: ...` |

#### `handle_errors` 取值

- `True`（默认）：自动重试，使用内置错误信息
- `False`：抛出异常
- `"自定义字符串"`：返回固定错误提示
- `(ExceptionType1, ...)`：仅捕获指定异常重试
- `callable`：自定义错误处理函数

**常见异常**：

- `MultipleStructuredOutputsError`：返回了多个结构化输出
- `StructuredOutputValidationError`：输出验证失败

------

## 8. Agent 高级用法 4：流式输出及模式

### 8.1 流式输出好处

- 实时反馈，降低用户等待焦虑
- 适合长响应或延迟高的场景

### 8.2 使用 `agent.stream(stream_mode=...)`

| 模式                | 说明                                      | 适用场景                 |
| :------------------ | :---------------------------------------- | :----------------------- |
| `"values"`          | 每步输出完整状态                          | 状态持久化、调试         |
| `"updates"`（默认） | 只输出增量变化                            | 监控 Agent 执行进度      |
| `"messages"`        | 输出流式 token 及元数据                   | 打字机效果（聊天机器人） |
| `"tasks"`           | 输出任务开始/结束信息                     | 监控任务生命周期         |
| `"debug"`           | 比 tasks 更详细，含时间戳等               | 深度调试                 |
| `"checkpoints"`     | 每个检查点触发输出                        | 状态持久化、工作流恢复   |
| `"custom"`          | 通过 `get_stream_writer()` 自定义发送数据 | 输出业务进度日志         |

### 组合模式

python

```
for stream_mode, chunk in agent.stream(
    {"messages": [...]},
    stream_mode=["tasks", "updates"]
):
    print(f"模式：{stream_mode}，数据：{chunk}")
```



------

## 9. 实战：多功能智能助手

实现功能：天气查询、数学计算、时间查询、货币转换、信息搜索。

### 9.1 模型初始化

python

```
model = init_chat_model("gpt-5.4-mini", model_provider="openai", ...)
```



### 9.2 工具定义（使用 `@tool` 装饰器）

每个工具需有清晰的 docstring（含 Args、Returns、Examples），Agent 依据此选择工具。

### 9.3 创建 SmartAssistant 类

- 封装工具列表、系统提示词、`create_agent`
- 维护对话历史 `self.messages`
- `chat()` 方法：添加用户消息 → `agent.invoke` → 更新历史 → 返回最后 AI 消息
- `reset()` 重置历史

### 9.4 主程序

- 演示模式：预设若干问题
- 交互模式：循环接收用户输入，支持 `quit` / `reset`

------

## 总结要点

1. **统一入口**：`create_agent()` 取代旧版多种 Agent 创建函数。
2. **核心组件**：模型、工具、系统提示、名称、结构化输出、中间件（后续）。
3. **工具调用**：基于 ReAct 循环，直到无 `tool_calls`。
4. **结构化输出**：推荐 `ToolStrategy`，支持多种 Schema，可自定义错误处理。
5. **流式输出**：多种模式满足不同监控和交互需求。
6. **工程实践**：工具数量适中（2~5 个），docstring 清晰，合理设置系统提示和 Agent 名称。

LangChain中间件笔记



详细总结一下，我需要一份笔记

我们根据PDF内容，整理一份详细的笔记。笔记要结构化，涵盖中间件的概念、分类、常用内置中间件的使用、其他内置中间件、组合顺序、自定义中间件等。要求详细，但不照搬原文，要提炼关键点。内容很多，需要系统组织。

我将按以下结构组织：

1. 中间件概述（概念、为什么需要、分类）
2. 常用内置中间件详解（Summarization, HumanInTheLoop, PII, TodoList）
3. 其他内置中间件概览（ModelCallLimit, ToolCallLimit, ModelFallback, LLMToolSelector, ToolRetry, ModelRetry, LLMToolEmulator, ContextEditing, FilesystemFileSearch, Shell, Filesystem, Subagent等）
4. 多个中间件组合及执行顺序（洋葱模型）
5. 自定义中间件（hook函数分类、Node-style和Wrap-style的用法、装饰器与类写法、执行顺序）
6. 总结

根据PDF内容，详细说明每个中间件的参数、用法、示例。因为内容多，要精简但不遗漏关键。笔记格式可以用标题、列表、代码块等。

由于用户要求“详细总结”，我会尽量全面。注意使用中文。

开始整理。

# LangChain 中间件（Middleware）详细笔记

> 基于尚硅谷教程整理，涵盖概念、内置中间件、组合顺序及自定义开发。

------

## 一、中间件概述

### 1.1 什么是中间件

- **定义**：Agent 执行流程中的**钩子函数**，在关键节点（模型调用前/后、工具调用前/后）拦截、修改或增强行为，无需改动主流程代码。
- **类比**：流水线上的检查点/插入器，在不改变主线的情况下附加横切逻辑。
- **核心价值**：将日志、鉴权、重试、风控、审计等**横切关注点**从业务主流程中剥离，让 Agent 专注核心推理。

### 1.2 为什么需要中间件

没有中间件时，流程直接：用户输入 → 拼接提示 → 调模型 → 调工具 → 返回。
真实项目会遇到：

- 动态切换模型
- 限制用户工具权限
- 工具报错自动重试
- 插入额外系统提示
- 记录执行日志
- 敏感信息阻断
- 人工审批关键操作

若全部写入主流程会导致：

- 主流程臃肿、混乱
- 横切逻辑难以复用
- 控制粒度不细
- 维护成本高

中间件正是解决这些问题。

### 1.3 中间件的分类

- **自定义中间件**：开发者自己实现
- **内置中间件**：LangChain 提供（与模型供应商无关）
- **供应商定制中间件**：依赖特定模型服务（非重点）

LangChain 提供 **16 个** 与供应商无关的内置中间件，分为六大类（见下节）。

------

## 二、常用内置中间件详解

### 2.1 SummarizationMiddleware（摘要中间件）

**作用**：当历史消息达到 token 或条数阈值时，调用大模型对历史进行摘要，压缩上下文，节省成本。

**关键参数**：

- `model`：用于摘要的模型（对象或名称）
- `trigger`：触发条件列表（满足任一即触发）：
  - `("tokens", N)`：累计 token 数 ≥ N
  - `("messages", N)`：消息条数 ≥ N
  - `("fraction", f)`：累计 token ≥ `max_input_tokens * f`（需模型 profile 提供 `max_input_tokens`）
- `keep`：摘要后保留的原始消息数量/ token（同一时间只接受一种条件）
  - `("tokens", N)` / `("messages", N)` / `("fraction", f)`
- `token_counter`：默认 `count_tokens_approximately`（估算）
- `summary_prompt`：自定义提示词，需包含 `{messages}` 占位符
- `trim_token_to_summarize`：摘要前裁剪历史消息的最大 token 数，默认 4000

**示例要点**：

- 若使用 `fraction` 条件，必须为模型指定 `profile={"max_input_tokens": ...}`
- 摘要结果作为 `HumanMessage` 插入消息列表头部
- `keep` 决定保留最新多少条原始消息

------

### 2.2 HumanInTheLoopMiddleware（人工审核中间件）

**作用**：在工具调用前中断执行，等待用户决策（approve / edit / reject）。

**关键参数**：

- `interrupt_on`：字典，指定哪些工具需要中断及策略
  - `True`：允许 approve / edit / reject
  - `False`：不中断
  - `{"allowed_decisions": ["approve", "reject"], "description": "..."}` 精细控制
- `description_prefix`：自定义中断描述前缀

**使用步骤**：

1. 创建 Agent 时传入 `checkpointer`（如 `InMemorySaver`）

2. 调用 `invoke` 后，若触发中断，响应中会有 `__interrupt__` 字段，包含 `action_requests`

3. 构造决策列表（顺序必须与请求顺序一致），每条决策格式：

   python

   ```
   {"type": "approve"}  # 或 "reject"
   # 或 "edit" 并带 edited_action
   {"type": "edit", "edited_action": {"name": "tool", "args": {...}}}
   ```

   

4. 用 `Command(resume=decisions)` 继续执行，传递相同的 `config`（thread_id）

**注意**：`read_email_tool` 设为 `False` 则不中断；`send_email_tool` 只允许 approve/reject。

------

### 2.3 PIIMiddleware（敏感信息保护中间件）

**作用**：检测并处理对话中的个人身份信息（PII），防止泄露给模型。

**关键参数**：

- `pii_type`：内置或自定义类型（email, credit_card, url, mac_address, ip）
- `strategy`：处理策略
  - `redact`：替换为 `[REDACTED_EMAIL]` 等标签
  - `mask`：部分遮蔽（如 `******5100`）
  - `hash`：替换为哈希值（如 `<url_hash:...>`）
  - `block`：直接抛出异常
- `detector`：自定义检测函数或正则表达式
- `apply_to_input`：是否在模型调用前检测（默认 True）
- `apply_to_output`：是否在模型输出后检测（默认 False）
- `apply_to_tool_results`：是否检测工具输出（默认 False）

**示例**：可同时配置多个 PII 中间件，分别处理不同类型和策略；自定义检测函数需返回 `[{"text":..., "start":..., "end":...}]` 列表。

------

### 2.4 TodoListMiddleware（任务规划中间件）

**作用**：赋予 Agent 任务规划与进度追踪能力，适合多步骤、有依赖关系的复杂任务。

**原理**：通过 `write_todos` 工具维护待办列表（状态：`in_progress` / `completed` / `pending`），Agent 每完成一步自动更新。

**关键参数**：

- `system_prompt`：自定义指导提示词（默认内置）
- `tool_description`：自定义 `write_todos` 工具描述

**典型场景**：代码修复、多文件工程、需要边做边调计划的场景。

**使用要点**：

- Agent 需要配合文件操作、测试等工具
- 中间件会自动注入 `write_todos` 工具
- 状态保存在 `state["todos"]` 中，可在外层读取显示进度

**示例**：修复 `my_add.py`（bug: 返回 `a-b` 而非 `a+b`），Agent 依次执行：列出文件 → 读取 → 修改 → 运行测试，每一步更新 todos。

------

## 三、其他内置中间件概览

### 3.1 ModelCallLimitMiddleware（模型调用次数限制）

- 限制整个会话（thread）或单次运行（run）的模型调用次数
- `exit_behavior`：`"end"`（优雅结束）或 `"error"`（抛异常）
- 参数：`thread_limit`, `run_limit`

### 3.2 ToolCallLimitMiddleware（工具调用次数限制）

- 限制总工具调用次数或特定工具次数
- 同样支持 `exit_behavior`：`"end"`, `"error"`, `"continue"`（默认，让模型知道超限后自行决定）
- 注意 `continue` 可能导致无限循环，需配合容错机制

### 3.3 ModelFallbackMiddleware（模型故障转移）

- 主模型失败时自动切换备用模型
- 可指定多个 fallback 模型列表

### 3.4 LLMToolSelectorMiddleware（智能工具筛选）

- 工具数量过多时，用子模型（轻量）预筛选最相关的工具，减少主模型负担
- 参数：`model`（筛选模型）、`max_tools`（最多选几个）、`always_include`（强制包含的工具名）

### 3.5 ToolRetryMiddleware（工具调用重试）

- 基于指数退避（Exponential Backoff）自动重试失败的工具调用
- 参数：`max_retries`, `backoff_factor`, `initial_delay`, `max_delay`, `jitter`（抖动，防止惊群效应）, `retry_on`（异常类型）, `on_failure`（"continue" 或 "error"）
- **抖动**：加入随机性避免并发重试同时冲击下游，生产环境建议开启

### 3.6 ModelRetryMiddleware（模型调用重试）

- 与 ToolRetry 策略相同，针对模型调用失败

### 3.7 LLMToolEmulator（工具模拟中间件）

- 用 LLM 模拟工具执行，适合在工具未开发完成时测试流程

### 3.8 ContextEditingMiddleware（上下文编辑）

- 自动裁剪或清理工具调用产生的冗长输出，节省 token
- 通过 `ClearToolusesEdit(trigger=..., keep=...)` 配置，在达到 token 阈值时删除旧的工具消息
- 不影响实际消息列表，只影响发送给模型的内容

### 3.9 FilesystemFileSearchMiddleware（文件搜索）

- 提供 `glob_search` 和 `grep_search` 工具，让 Agent 搜索本地文件系统
- 参数：`root_path`, `allowed_extensions`, `use_ripgrep`, `max_file_size_mb`

### 3.10 ShellToolMiddleware（Shell 执行）

- 提供持久化 shell 环境，执行系统命令（Windows 不支持）

### 3.11 FilesystemMiddleware（文件系统操作）

- 源自 deepagents，提供查看目录、读、写、修改文件四个工具

### 3.12 SubagentMiddleware（子 Agent）

- 允许主 Agent 生成子 Agent 处理复杂子任务

------

## 四、多个中间件组合及执行顺序

**顺序非常重要**，类似洋葱模型：

- `before_*` 钩子按列表**正序**执行
- `after_*` 钩子按列表**逆序**执行
- `wrap_*` 中间件：先定义的包在外层，后定义的在内层（先进后出）

**示例**：

python

```
middleware = [M1, M2, M3]
# before: M1 → M2 → M3 → 模型调用
# after:  M3 → M2 → M1
```



因此，应根据依赖关系排列：如先做 PII 检测，再限制调用次数，再摘要，再重试。

------

## 五、自定义中间件

### 5.1 Hook 函数（钩子）分类

LangChain Agent 基于 LangGraph，提供六种钩子：

**Node-style（节点风格）**：

- `before_agent`：Agent 启动前
- `before_model`：模型调用前
- `after_model`：模型调用后
- `after_agent`：Agent 完成后

**Wrap-style（包装风格）**：

- `wrap_model_call`：包裹模型调用（可同时做前后处理）
- `wrap_tool_call`：包裹工具调用

### 5.2 Node-style 用法

#### 装饰器方式：

python

```
from langchain.agents.middleware import before_model, after_model

@before_model
def my_before(state, runtime):
    # 修改 state["messages"] 等
    return None  # 或返回 dict 更新状态，或 {"jump_to": "tools"} 控制流程
```



- `state`：`AgentState`，包含 `messages`, `todos` 等
- `runtime`：上下文环境
- 返回值：`None`（不修改）、`dict`（更新 state）、`{"jump_to": "..."}` 跳转（需 `can_jump_to` 权限）

#### 类方式：

继承 `AgentMiddleware`，实现 `before_model` 等方法：

python

```
class MyMiddleware(AgentMiddleware):
    def before_model(self, state, runtime):
        ...
```



#### 跳转控制（`jump_to`）：

- `"_end_"`：终止 Agent
- `"tools"`：跳转到工具节点
- `"model"`：跳回模型节点（需配合 `can_jump_to` 装饰器参数）
- 使用装饰器时需用 `@before_model(can_jump_to=["tools"])` 声明权限；类方式用 `@hook_config(can_jump_to=[...])`

### 5.3 Wrap-style 用法

#### `wrap_model_call`

- 参数：`request: ModelRequest`, `handler: Callable`
- 可在调用前后修改请求/响应，常用于重试、缓存、动态系统提示
- 示例：在 `request.messages[-1].content` 追加前缀，调用 `handler`，再修改 `response.result[0].content`

#### `wrap_tool_call`

- 参数：`request: ToolCallRequest`, `handler`
- 可修改工具参数、监控执行、重试等

装饰器方式：`@wrap_model_call` / `@wrap_tool_call`
类方式：继承 `AgentMiddleware`，实现同名方法。

### 5.4 装饰器 vs 类写法

- **单钩子、简单逻辑** → 装饰器快速
- **多钩子组合、复杂配置、需复用** → 类更清晰（可传参、可测试、可自省）
- 底层本质相同：装饰器最终也会生成 `AgentMiddleware` 子类实例

### 5.5 执行顺序总结

- `before_*`：**正序**（按 middleware 列表）
- `after_*`：**逆序**
- `wrap_*`：洋葱模型，**外层先进后出**
- 不同钩子类型混合时，整体流程大致为：
  `before_agent` → `before_model` → `wrap_model`（洋葱） → 模型调用 → `wrap_model` 返回 → `after_model` → `after_agent`

------

## 六、总结

- 中间件是 LangChain 1.x 的工程化核心，用于在 Agent 生命周期中插入横切逻辑。
- 内置中间件覆盖成本控制、容错、安全、智能编排、环境交互、调试六大类，开箱即用。
- 组合中间件时注意顺序，利用洋葱模型控制执行粒度。
- 自定义中间件可通过装饰器或类实现，灵活扩展。
- 生产环境中推荐使用类方式组织可复用、可配置的中间件组件。

> 掌握中间件，即可将 Agent 从“原型玩具”升级为“生产级工程系统”。

LangChain记忆上下文笔记



详细总结一下，我需要一份笔记

我们根据用户要求，对提供的PDF内容进行详细总结，形成一份结构化的笔记。内容涉及LangChain中的记忆（Memory）概念，包括短期记忆、长期记忆、上下文管理、静态上下文等。需要条理清晰，覆盖核心概念、代码示例、对比等。输出格式为Markdown。

# LangChain 记忆与上下文管理 学习笔记

> 基于尚硅谷课程《09-上下文与记忆》整理，讲师宋红康。

------

## 一、概述

### 1.1 为什么需要记忆

- 大模型本身是**无状态**的，每次调用都是全新开始，不记得之前对话。
- 复杂多轮交互需要智能体“记住”历史信息。
- **记忆（Memory）** 组件负责存储历史交互信息，让LLM在响应时能“看到”之前的内容。

### 1.2 如何解决记忆问题

- **上下文工程**：将历史消息保存下来，下次请求时一并输入给模型。
- LangChain 1.x 基于 LangGraph 构建，提供了三种上下文管理方式：

| 上下文类型       | 描述                                   | 可变性 | 生命周期 | 访问方法               |
| :--------------- | :------------------------------------- | :----- | :------- | :--------------------- |
| 动态运行时上下文 | 单次运行中演变的可变数据               | 动态   | 单次运行 | LangGraph state 对象   |
| 动态会话上下文   | 会话间共享的持久数据（偏好、历史洞察） | 动态   | 跨对话   | LangGraph store 对象   |
| 静态运行时上下文 | 启动时传入的元数据、工具、数据库连接   | 静态   | 单次运行 | LangGraph context 对象 |

### 1.3 LangChain 记忆分类

- **短期记忆（会话级）**：作用范围在单个 `thread_id` 内，切换线程则记忆消失。
- **长期记忆（跨会话级）**：存储用户特定或应用级数据，可在任何线程中访问。

------

## 二、短期记忆（Short-term Memory）

短期记忆 = **State**（会话内部状态） + **Checkpointer**（持久化机制） + **Thread ID**（会话作用域）

- **State**：默认存储历史消息列表 `messages`。
- **Checkpointer**：将 State 作为检查点持久化保存（快照）。
- **Thread ID**：唯一标识一个会话，相同 `thread_id` 共享记忆。

### 2.1 基于内存的持久化器（InMemorySaver）

适合测试/开发，进程结束则数据丢失。

#### 示例：无记忆（每次都是新对话）

python

```
agent = create_agent(model=model, tools=[])
response1 = agent.invoke({"messages": [HumanMessage("我叫张三")]})
response2 = agent.invoke({"messages": [HumanMessage("我叫什么？")]})
# Agent 不记得，回答“我不知道”
```



#### 示例：有记忆（使用 InMemorySaver）

python

```
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
agent = create_agent(model=model, checkpointer=checkpointer)

config = {"configurable": {"thread_id": "1"}}

# 第一轮
agent.invoke({"messages": [HumanMessage("我叫张三")]}, config=config)

# 第二轮（同一 thread_id）
response = agent.invoke({"messages": [HumanMessage("我叫什么？")]}, config=config)
# Agent 回答：“你叫张三”
```



#### 关键步骤

1. 初始化记忆引擎：`checkpointer = InMemorySaver()`
2. 绑定 Agent：`create_agent(..., checkpointer=checkpointer)`
3. 设定会话 ID：通过 `config` 传入 `thread_id`，相同 ID 共享记忆，不同 ID 完全隔离。

#### 常见问题

- **不记得**：检查是否添加了 `checkpointer`，是否传入了 `config`，`thread_id` 是否一致。
- **数据丢失**：`InMemorySaver` 只在内存中保存，进程重启即丢失，生产环境需用持久化存储（如 PostgreSQL）。
- **内存无限增长**：需使用上下文管理策略（修剪、摘要、删除）。

### 2.2 基于外部存储的持久化器（PostgresSaver）

生产环境使用，数据持久化到数据库。

python

```
from langgraph.checkpoint.postgres import PostgresSaver

DB_URL = "postgresql://user:pass@host:5432/db?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
    checkpointer.setup()  # 创建表（幂等）
    agent = create_agent(model=model, checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "1"}}
    # 后续调用同 InMemorySaver
```



- 数据库表：`checkpoints`（主表）、`checkpoint_blobs`、`checkpoint_writes`、`checkpoint_migrations`。
- 即使重启程序，只要 `thread_id` 相同，历史状态依然可加载。

### 2.3 两种方式对比

| 特性       | InMemorySaver | PostgresSaver |
| :--------- | :------------ | :------------ |
| 数据持久化 | 内存          | 数据库        |
| 进程重启后 | 丢失          | 保留          |
| 跨进程共享 | 否            | 是            |
| 适用场景   | 测试/开发     | 生产环境      |

### 2.4 记忆治理策略（上下文管理）

随着对话积累，历史消息过多会带来问题：

- 上下文窗口有限
- 长上下文表现下降
- Token 成本增加

#### 2.4.1 消息裁剪（Trimming）

在模型调用前裁剪上下文，保留系统消息和最近若干条。

python

```
from langchain.agents.middleware import before_model
from langchain.messages import RemoveMessage

@before_model
def trim_messages(state, runtime):
    messages = state["messages"]
    if len(messages) <= 3:
        return None
    first_msg = messages[0]
    recent = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent
    return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)] + new_messages}

agent = create_agent(model=model, middleware=[trim_messages], checkpointer=InMemorySaver())
```



- 优点：控制 token 用量
- 缺点：丢失旧上下文

#### 2.4.2 消息删除（Deletion）

模型调用后，将某些消息从列表中移除（永久更改状态）。

python

```
from langchain.agents.middleware import after_model

@after_model
def delete_old_messages(state, runtime):
    messages = state["messages"]
    if len(messages) > 5:
        to_delete = len(messages) - 5
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:to_delete]]}
    return None
```



- **RemoveMessage 原理**：追加“墓碑”标记，框架合并器在读取时自动过滤被删除的消息。
- 适合明确要遗忘、清理的场景。

#### 2.4.3 摘要（Summarization）

将早期历史压缩成摘要，保留语义，不保原文。

python

```
from langchain.agents.middleware import SummarizationMiddleware

agent = create_agent(
    model=model_out,
    checkpoint=InMemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model=model_in,           # 用于生成摘要的模型（可用便宜的）
            trigger=[("tokens", 100)], # 超过100 tokens触发
            keep=("messages", 2),      # 保留最近2条消息
            summary_prompt="对历史消息摘要，消息列表如下\n{messages}"
        )
    ]
)
```



- **优点**：更折中，保留关键信息
- **缺点**：摘要模型调用有成本，可能丢失细节
- **触发阈值**：根据模型窗口大小设置（如 4K 窗口设 3000，8K 设 6000）

#### 2.4.4 自定义过滤策略

通过中间件可任意修改消息列表，实现任意过滤逻辑。

### 2.5 理解 State

`AgentState` 是 `TypedDict`，包含三个字段：

- `messages`：历史消息列表（Required）
- `jump_to`：跳转节点标记（NotRequired）
- `structured_response`：结构化输出内容（NotRequired）

示例：在中间件中打印 State 的 `jump_to` 和 `structured_response`，验证其在流程中的变化。

------

## 三、长期记忆（Long-term Memory）

### 3.1 基本理解

- **短期记忆**：会话级别（thread），会话间不共享。
- **长期记忆**：用户/应用级别，跨会话共享（如用户偏好、VIP 状态、历史经验）。

#### 类型划分（参考 CoALA 论文）

| 类型                     | 存储内容         | 示例                                     |
| :----------------------- | :--------------- | :--------------------------------------- |
| 语义记忆（Semantic）     | 事实、偏好、概念 | “用户喜欢简短回答”、“某公司属于 AI 行业” |
| 情景记忆（Episodic）     | 经验、过去动作   | 之前的成功案例、few-shot 示例            |
| 程序性记忆（Procedural） | 规则、做事方法   | 系统提示词、工作流程、工具调用规则       |

### 3.2 存储架构：Store → Namespace → Key → Value

- **Store**：`BaseStore` 子类，如 `InMemoryStore`（测试）、`PostgresStore`（生产）。
- **Namespace**：元组形式的层级路径（如 `("users", "user_123", "preferences")`），用于分组隔离。
- **Key**：字符串，该 namespace 下的唯一标识。
- **Value**：字典 `dict[str, Any]`，存储实际数据。

python

```
store.put(("users", "alice", "memories"), "profile", {"language": "zh-CN", "style": "short"})
item = store.get(("users", "alice", "memories"), "profile")
print(item.value)  # {'language': 'zh-CN', 'style': 'short'}
```



### 3.3 基础 API

#### put() 写入

python

```
store.put(
    namespace=("users", "alice", "memories"),
    key="pref_food",
    value={"category": "food", "text": "Alice likes sushi"},
    index=False,          # 是否建立语义索引
    ttl=None              # 过期时间
)
```



- **InMemoryStore**：每次 put 都创建新 Item，`created_at` 和 `updated_at` 相同。
- **PostgresStore**：更新时 `created_at` 不变，`updated_at` 变化。

#### get() 读取

python

```
item = store.get(("users", "alice", "memories"), "pref_food")
if item:
    print(item.value)  # 字典
    print(item.created_at, item.updated_at)
```



#### search() 检索

支持两种方式：

1. **按 namespace 前缀**：`store.search(("users",))`
2. **按 filter 过滤**：`store.search(("users",), filter={"sports": "跑步"})`
3. **按语义搜索**：需配置索引（embedding 函数、维度、索引字段）

python

```
# 配置语义索引
index_config = {
    "embed": embedding_model,   # 嵌入模型
    "dims": 3072,
    "fields": ["$"]             # 将整个 value 嵌入，或指定字段如 ["course"]
}
store = InMemoryStore(index=index_config)

# 语义检索
results = store.search(("users",), query="数电模电")
for item in results:
    print(item.value, item.score)  # 按相似度降序
```



- `fields` 支持：`["$"]`（整体）、`["field1", "field2"]`（指定字段）、`["parent.child"]`（嵌套）、`["array[*].field"]`（数组）。
- `score` 为相似度分数，排序返回。

### 3.4 在 Agent 中访问长期记忆

#### 3.4.1 在工具（Tool）中访问

通过 `ToolRuntime` 的 `store` 属性访问。

python

```
from langchain.tools import tool, ToolRuntime

@tool
def save_user_info(name: str, runtime: ToolRuntime):
    runtime.store.put(("users",), runtime.state["user_id"], {"name": name})
    return "saved"

@tool
def get_user_info(runtime: ToolRuntime):
    item = runtime.store.get(("users",), runtime.state["user_id"])
    return str(item.value) if item else "unknown"

# 自定义 State 添加 user_id 字段
class CustomState(AgentState):
    user_id: NotRequired[str]

agent = create_agent(
    model=model,
    tools=[save_user_info, get_user_info],
    store=store,              # 注入 store
    state_schema=CustomState,
    system_prompt="用户提及个人信息时记录，询问时检索"
)

# 不同线程（thread_id）通过 user_id 共享长期记忆
response1 = agent.invoke({"messages": ["我是小花"], "user_id": "user-1"})
response2 = agent.invoke({"messages": ["我是谁"], "user_id": "user-1"})  # 跨线程仍记得
```



- 使用 `PostgresStore` 时，数据持久化到数据库，新增表 `store` 和 `store_migrations`。

#### 3.4.2 在中间件（Middleware）中访问

- **Node-style hooks**（如 `before_model`、`after_model`）：通过 `runtime.store` 访问。
- **Wrap-style hooks**（如 `wrap_model_call`、`wrap_tool_call`）：通过 `request.runtime.store` 访问。

示例：`wrap_tool_call` 中校验额度并更新长期记忆。

python

```
class ToolGuard(AgentMiddleware):
    def wrap_tool_call(self, request: ToolCallRequest, handler):
        store = request.runtime.store
        context = request.runtime.context
        username = context.username
        value = store.get(namespace, username).value
        # 校验额度...
        value["tokens_left"] -= cost
        store.put(namespace, username, value)   # 更新长期记忆
        return handler(request)
```



### 3.5 何时写入长期记忆

- **热路径（Hot Path）**：用户发消息时立即写入，下一轮马上生效，但增加延迟。
- **后台（Background）**：先回答，异步整理记忆，主流程更快，但不能立刻生效。

**工程选择**：

- 用户偏好、资料 → 热路径
- 对话摘要、经验沉淀 → 后台

------

## 四、静态运行时上下文（Static Runtime Context）

- 表示**不可变**的数据，如用户元数据、数据库连接等，通过 `invoke` 的 `context` 参数传递。
- 在运行期间不会更改。

### 4.1 在中间件中访问

通过 `runtime.context` 访问（Node-style）或 `request.runtime.context`（Wrap-style）。

#### 示例：动态系统提示词（`@dynamic_prompt`）

python

```
from langchain.agents.middleware import dynamic_prompt

@dataclass
class UserContext:
    username: str

@dynamic_prompt
def personalized_prompt(request: ModelRequest) -> str:
    username = request.runtime.context.username
    preferences = request.runtime.store.get(("users", "preferences"), username).value
    return f"#用户偏好\n{preferences}"

agent = create_agent(
    model=model,
    middleware=[personalized_prompt],
    store=store,
    context_schema=UserContext
)

response = agent.invoke(
    {"messages": ["为什么花儿这样红？"]},
    context=UserContext(username="Ada Lovelace")
)
```



- `@dynamic_prompt` 底层与通用钩子机制一致，专门用于动态修改系统提示词。

### 4.2 在工具中访问静态上下文

通过 `ToolRuntime` 的 `context` 属性访问。

python

```
@tool
def read_user_info(runtime: ToolRuntime[UserContext, Any]):
    user_id = runtime.context.user_id   # 从静态上下文获取
    item = runtime.store.get(namespace, user_id)
    return item.value if item else ""
```



- 需显式指定 `ToolRuntime` 泛型为 `[UserContext, Any]`，否则 LangChain 会警告上下文为 None。

------

## 五、总结

| 维度         | 短期记忆                        | 长期记忆                 | 静态上下文           |
| :----------- | :------------------------------ | :----------------------- | :------------------- |
| **作用域**   | 单线程（thread_id）             | 跨线程（用户/应用级）    | 单次运行（不可变）   |
| **存储介质** | Checkpointer（State）           | Store（Key-Value）       | 运行参数（context）  |
| **生命周期** | 会话结束或切换 thread_id 即消失 | 持久化，不随会话结束     | 单次 invoke 有效     |
| **典型用途** | 对话历史、多轮上下文            | 用户偏好、知识条目、额度 | 用户身份、数据库连接 |
| **治理策略** | 修剪、删除、摘要                | 语义索引、过期时间       | 无（只读）           |

**实践建议**：

- 开发测试用 `InMemorySaver` + `InMemoryStore`。
- 生产环境替换为 `PostgresSaver` + `PostgresStore`。
- 根据场景组合使用三种记忆机制，构建健壮的多轮交互 Agent。



RAG模块详细笔记



详细总结一下，我需要一份笔记

嗯，用户上传了一份关于LangChain RAG模块的PDF文档，内容非常详尽，涵盖了从RAG概念、工作流程到具体组件（加载器、切分器、嵌入模型、向量存储）的实践案例。用户要求我详细总结一下，并生成一份笔记。

这份文档本身就是一份高质量的学习资料，结构清晰，内容扎实。我的任务是将其核心知识提炼、重组，形成一份结构化的学习笔记，方便用户理解和回顾。

考虑到内容量很大，我打算按照文档本身的逻辑主线来组织笔记，但需要更结构化一些，使其更像一份系统的学习指南。可以分成几个核心部分：先讲清楚RAG为什么重要（解决大模型的局限），再拆解其工作流程的六大环节，然后重点深入文档加载、文本切分、嵌入与存储这几个关键步骤的实践与细节，最后用一个完整的案例来串联所有知识点。这样由浅入深，理论与实践结合。

笔记的风格应该清晰、有条理，但避免照搬原文，而是用自己的话进行概括和解释。对于关键的技术选型和参数，需要突出强调，并加入一些自己的理解（比如对切分策略的评价），让笔记不只是复述，而是有思考的总结。最后可以给一些学习建议，帮助用户巩固。

# RAG（检索增强生成）模块详细笔记

## 一、RAG概述

### 1.1 大模型的局限

1. **知识滞后**：LLM训练数据有截止日期，无法反映最新信息
2. **知识缺失**：缺乏特定领域（企业内部资料、私有数据等）的知识
3. **幻觉问题**：模型可能"胡言乱语"，生成不准确或虚构的内容

**当前共识方案**：为大模型提供上下文信息 + RAG检索增强生成

### 1.2 什么是RAG

RAG（Retrieval-Augmented Generation）= **检索（Retrieval）+ 生成（Generation）**

> 核心思想：将检索出来的文档和提示词一起输送给大模型，生成更可靠的答案

**RAG vs 其他方案对比：**

- vs 提示词工程：RAG有更丰富的上下文，无需用户过多描述
- vs 模型微调：RAG时效性和可靠性更好，保护业务数据隐私

**RAG的缺点：**

- 响应时延较高（每次问答都涉及外部检索）
- 消耗大量Token资源

### 1.3 RAG工作流程六大环节

text

```
Source（数据源）→ Load（加载）→ Transform（转换）→ Embed（嵌入）→ Store（存储）→ Retrieve（检索）
```



------

## 二、文档加载器（Document Loaders）

### 2.1 核心概念

- **BaseLoader**：所有加载器的基类，提供`load()`和`lazy_load()`方法
- **Document对象**：包含`page_content`（文本内容）和`metadata`（元数据）

### 2.2 常用加载器及示例

#### TextLoader - 加载TXT文件

python

```
from langchain_community.document_loaders import TextLoader

loader = TextLoader(file_path="./asset/load/01-langchain-utf-8.txt", encoding="utf-8")
docs = loader.load()
```



#### CSVLoader - 加载CSV文件

python

```
from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(file_path="asset/load/04-load.csv")
data = loader.load()
# 每行CSV变成一个Document，metadata中包含行号
```



#### JSONLoader - 加载JSON文件

**关键**：使用`jq_schema`来提取数据

python

```
from langchain_community.document_loaders import JSONLoader

# 提取全部字段
loader = JSONLoader(
    file_path="./asset/load/03-load.json",
    jq_schema=".",           # 提取所有字段
    text_content=False       # 保持原始JSON结构
)

# 提取特定字段
loader = JSONLoader(
    file_path="./asset/load/03-load.json",
    jq_schema=".messages[].content"   # 提取messages中所有content
)

# 自定义组合字段
loader = JSONLoader(
    file_path="./asset/load/03-response.json",
    jq_schema="""
        .data.items[] {
            author,
            created_at,
            content: (.title + "\n" + .content)
        }
    """
)
```



#### PyPDFLoader - 加载PDF

python

```
from langchain_community.document_loaders import PyPDFLoader

# 本地文件
loader = PyPDFLoader(file_path="../asset/load/04-sample.pdf")

# 在线文件
loader = PyPDFLoader(file_path="https://arxiv.org/pdf/alg-geom/9202012")

# extraction_mode: "plain"(默认) 或 "layout"(保留多栏结构)
loader = PyPDFLoader(file_path="...", extraction_mode="layout")
```



> **MinerU替代方案**：支持PDF、Word、PPT、图片等，提供OCR、公式、表格解析

#### Word/Markdown/HTML加载

python

```
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader

# mode="single" 返回单个Document
# mode="elements" 按标题等元素切分
loader = UnstructuredMarkdownLoader(
    file_path="./asset/load/06-load.md",
    mode="elements",
    strategy="fast"  # 或 "hi_res"
)
```



#### DirectoryLoader - 批量加载文件夹

python

```
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PythonLoader

loader = DirectoryLoader(
    path="../asset/load",
    glob="*.py",              # 匹配模式
    use_multithreading=True,   # 多线程加速
    show_progress=True,        # 显示进度条
    loader_cls=PythonLoader    # 指定底层加载器
)
docs = loader.load()
```



------

## 三、文档切分器（Text Splitters）

### 3.1 为什么需要切分？

1. **长文档问题**：大模型有Token上限
2. **检索精度**：小块检索更精准，减少无关信息干扰
3. **成本控制**：减少不必要的Token消耗

### 3.2 切分策略对比

| 策略         | 原理           | 优点               | 缺点           |
| :----------- | :------------- | :----------------- | :------------- |
| 按句子切分   | 自然句子边界   | 语义完整           | 块大小不一     |
| 按固定字符数 | 固定长度切断   | 简单快速           | 可能切断句子   |
| 重叠窗口     | 固定长度+重叠  | 避免关键内容被切断 | 冗余数据       |
| **递归字符** | 多级分隔符尝试 | **灵活高效，首选** | 实现复杂       |
| 语义切分     | 基于向量相似度 | 语义高度保持       | 效率低，速度慢 |

### 3.3 TextSplitter源码分析

**核心参数：**

- `chunk_size`：每个块的最大大小（默认4000）
- `chunk_overlap`：块之间的重叠字符数（默认200）
- `length_function`：计算文本长度的函数（默认`len`）
- `keep_separator`：是否保留分隔符
- `add_start_index`：是否在metadata中添加起始索引

**三种调用方式：**

python

```
# 方式1：传入字符串 → 返回字符串列表
splitter.split_text(text) -> List[str]

# 方式2：传入字符串列表 → 返回Document列表
splitter.create_documents(texts, metadata=None) -> List[Document]

# 方式3：传入Document集合 → 返回Document列表
splitter.split_documents(documents) -> List[Document]
```



### 3.4 具体切分器实现

#### ① CharacterTextSplitter - 按字符切分

python

```
from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=5,
    separator="。"    # 优先按分隔符切割
)
texts = splitter.split_text(text)
```



> **注意**：`separator`优先原则，先尝试在分隔符处切分，再考虑`chunk_size`

#### ② RecursiveCharacterTextSplitter - 递归切分（最常用）

**默认分隔符**：`["\n\n", "\n", " ", ""]`

python

```
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    add_start_index=True,
)
```



**工作原理（"先下探，再回溯"）：**

1. **拆分阶段**：按分隔符列表顺序递归切割超长块
2. **合并阶段**：将小块合并为满足`chunk_size`约束的块，保留`chunk_overlap`重叠

**自定义分隔符（适用于中文等无空格语言）：**

python

```
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""],
    keep_separator=True   # 保留句尾标点
)
```



#### ③ TokenTextSplitter - 按Token切分

python

```
from langchain_text_splitters import TokenTextSplitter

text_splitter = TokenTextSplitter(
    chunk_size=33,
    chunk_overlap=0,
    encoding_name="cl100k_base"   # OpenAI编码器
)
```



**为什么按Token切分？**

- 与LLM的Token计数逻辑一致
- 精确控制Token数，避免超限
- 便于成本控制

#### ④ SemanticChunker - 语义切分

python

```
from langchain_experimental.text_splitter import SemanticChunker
from langchain.embeddings import init_embeddings

text_splitter = SemanticChunker(
    embeddings=embedding_model,
    breakpoint_threshold_type="percentile",   # 阈值类型
    breakpoint_threshold_amount=65.0,         # 阈值量
    sentence_split_regex=r"(?<=[。？！])\s+"   # 句子切分正则
)
```



**工作原理**：将文本向量化，计算相邻句子的语义差异，差异超过阈值时切断。

**参数说明：**

- `breakpoint_threshold_type`：`percentile`（百分位数）、`standard_deviation`（标准差）、`interquartile`（四分位距）、`gradient`（梯度）
- `breakpoint_threshold_amount`：值越小分割越细，值越大分割越粗

#### ⑤ 其他切分器（了解）

- **HTMLHeaderTextSplitter**：按HTML标题标签（h1/h2/h3）切分
- **CodeTextSplitter**：按编程语言语法结构切分（支持Python、Java、Go等）
- **MarkdownTextSplitter**：按Markdown标题切分

------

## 四、文档嵌入模型（Text Embedding Models）

### 4.1 嵌入模型概述

将文本转换为向量表示，使计算机能够理解文本的语义。

**关键特性**：相似的词在向量空间中距离相近

**主要功能：**

- 语义匹配（计算余弦相似度）
- 文本检索（语义搜索）
- 信息推荐
- 知识挖掘
- NLP任务输入

### 4.2 常用嵌入模型

| 模型                   | 机构   | 向量维度 | 序列长度 |
| :--------------------- | :----- | :------- | :------- |
| bge-large-zh           | BAAI   | 1024     | 512      |
| bge-base-zh            | BAAI   | 768      | 512      |
| bge-small-zh           | BAAI   | 512      | 512      |
| bge-m3                 | BAAI   | 1024     | 8192     |
| text-embedding-3-small | OpenAI | 1536     | 8192     |
| text-embedding-3-large | OpenAI | 3072     | 8192     |

### 4.3 初始化方式

python

```
from langchain.embeddings import init_embeddings

# 使用OpenAI
embedding_model = init_embeddings(
    model="openai:text-embedding-3-large",
    api_key=os.getenv("CLOSEAI_API_KEY"),
    base_url=os.getenv("CLOSEAI_BASE_URL")
)

# 使用硅基流动（免费BGE-M3）
embedding_model = init_embeddings(
    model="Pro/BAAI/bge-m3",
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL")
)
```



### 4.4 两种核心方法

python

```
# 句子向量化（单条查询）
embedded_query = embedding_model.embed_query(text="what is AI?")

# 文档向量化（批量）
embedded_docs = embedding_model.embed_documents([
    "text1", "text2", "text3"
])
```



------

## 五、向量存储（Vector Stores）

### 5.1 向量数据库理解

传统数据库 → 精确匹配查询
向量数据库 → 相似性搜索（模糊查询）

> 将数据转化为多维空间中的向量，通过向量距离计算相似度

### 5.2 常用向量数据库

| 数据库        | 特点                         |
| :------------ | :--------------------------- |
| FAISS         | Meta开源，本地运行，高效     |
| Chroma        | 开源免费，轻量级，API极简    |
| Milvus        | 云原生，性能强悍，十亿级向量 |
| Pgvector      | PostgreSQL扩展               |
| Redis         | 内存数据库，原生支持向量搜索 |
| Elasticsearch | 分布式搜索引擎               |
| Pinecone      | 功能丰富的云服务             |

### 5.3 Milvus实战示例

python

```
from pymilvus import MilvusClient

# 连接Milvus
client = MilvusClient(MILVUS_URI)
client.create_database(db_name=DB_NAME)
client.use_database(db_name=DB_NAME)

# 创建集合（需提前指定向量维度）
client.create_collection(
    collection_name=COLLECTION_NAME,
    dimension=EMBED_DIM,
    metric_type="COSINE"   # 余弦相似度
)

# 批量写入数据
data = [
    {"id": i, "vector": vectors[i], "text": chunks[i].page_content}
    for i in range(len(chunks))
]
client.upsert(collection_name=COLLECTION_NAME, data=data)

# 向量检索
results = client.search(
    collection_name=COLLECTION_NAME,
    data=[query_vector],
    limit=k,
    output_fields=["text", "source"]
)
```



**相似度度量类型：**

- `COSINE`：余弦相似度（方向夹角，值越大越相似）
- `L2`：欧氏距离（值越小越相似）
- `IP`：内积（值越大越相似）

------

## 六、完整案例：Atguigu Assistant客服知识库

### 6.1 整体流程

text

```
知识库文件 → 文档加载 → 文本切分 → 向量化 → Milvus存储 → 相似度检索 → LLM生成回答
```



### 6.2 核心配置

python

```
MILVUS_URI = "http://localhost:19530"
DB_NAME = "rag_tutorial"
COLLECTION_NAME = "docs"
EMBED_MODEL_NAME = "Pro/BAAI/bge-m3"
EMBED_DIM = 1024
```



### 6.3 关键代码片段

**文档加载与切分：**

python

```
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(KNOWLEDGE_FILE, encoding="utf-8")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    separators=["===", "\n\n", "\n", "。", "！", "？", "，", " "]
)
chunks = splitter.split_documents(documents)
```



**向量写入：**

python

```
vectors = embed_model.embed_documents([chunk.page_content for chunk in chunks])
data = [{"id": i, "vector": vectors[i], "text": chunks[i].page_content} for i in range(len(chunks))]
client.upsert(collection_name=COLLECTION_NAME, data=data)
```



**检索与生成：**

python

```
def retrieve(question: str, k: int = 5):
    query_vector = embed_model.embed_query(question)
    results = client.search(
        collection_name=COLLECTION_NAME,
        data=[query_vector],
        limit=k,
        output_fields=["text", "source"]
    )
    return results[0]

def generate_answer(question: str):
    hits = retrieve(question)
    context = "\n\n".join([hit["entity"]["text"] for hit in hits])
    user_prompt = f"问题: {question}\n\n上下文: {context}"
    result = agent.invoke({"messages": [{"role": "user", "content": user_prompt}]})
    return result["messages"][-1]
```



------

## 七、总结与最佳实践

### 7.1 切分策略选择建议

| 场景              | 推荐切分器                                      |
| :---------------- | :---------------------------------------------- |
| 通用文本          | RecursiveCharacterTextSplitter                  |
| 中文文本          | RecursiveCharacterTextSplitter + 中文标点分隔符 |
| 代码文件          | CodeTextSplitter                                |
| Markdown文档      | MarkdownTextSplitter                            |
| HTML文档          | HTMLHeaderTextSplitter                          |
| 需要精确Token控制 | TokenTextSplitter                               |
| 高语义要求        | SemanticChunker                                 |

### 7.2 RAG开发要点

1. **文档加载**：利用LangChain丰富的加载器，统一为Document格式
2. **文本切分**：这是最具挑战性的环节，需根据数据类型选择策略
3. **嵌入模型**：选择适合的语言和场景的模型
4. **向量存储**：根据数据规模选择（本地开发用Chroma/FAISS，生产用Milvus）
5. **检索质量**：注意相似度度量类型和K值的选择
6. **生成质量**：构造清晰提示词，加入"如果不知道就回答不知道"的约束

### 7.3 常见问题

1. **chunk_size设置**：需考虑嵌入模型的序列长度限制和LLM的上下文窗口
2. **chunk_overlap设置**：一般设为chunk_size的5%-10%，保证语义连贯
3. **分隔符选择**：根据文本特点自定义，中文建议添加"。！？"等标点
4. **向量维度匹配**：嵌入模型输出维度必须与向量数据库collection的dimension一致