# 第3章 Model I/O与Chains · 重点标注版

## 1.1 Model I/O 介绍

- **核心三要素**：输入（Prompt） → 处理（Model） → 输出（Parser）。

> 💡 **本质**：这是与大模型交互最基础的“三步走”范式，后续所有复杂链（Chain）和代理（Agent）都建立在此之上。

------

## 1.2 调用在线模型

### 1.2.1 常用大模型服务平台

- **平台**：CloseAI、OpenRouter、阿里云百炼、百度千帆、硅基流动（了解即可）。
- **关键操作**：注册 → 创建 `API-Key` → 配置 `BASE_URL`。

⚠️ **【极高风险·必看】**：

1. **环境变量配置是强制安全要求**，**严禁**将 `API-Key` 硬编码在业务代码中！

2. **方式一（项目级）**：`.env` 文件 + `python-dotenv` 加载。

   ```bash
   # .env 文件内容
   OPENAI_API_KEY=sk-xxx
   OPENAI_BASE_URL=https://api.openai-proxy.org/v1
   ```

   ```python
   from dotenv import load_dotenv
   load_dotenv()
   import os
   api_key = os.getenv("OPENAI_API_KEY")
   ```

3. **方式二（系统级）**：Windows全局变量（适合学习)，避免反复 `load_dotenv()`。

4. **🔥 铁律**：**千万不要将 `.env` 文件上传到 Git 仓库**，否则 API-Key 会立即泄露！

------

### 1.2.2 OpenAI SDK 调用模型

- **行业标准**：OpenAI 的 API 规范（ChatCompletions）已成为事实标准，绝大多数国产模型（Qwen、DeepSeek等）均兼容。

- **两套API的区别**（⭐ 面试/理解重点）：

  - #### ChatCompletion API（经典）

    python

    ```
    from openai import OpenAI
    client = OpenAI(base_url=..., api_key=...)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "翻译"}]
    )
    print(completion.choices[0].message.content)
    ```

    

    #### Responses API（2025 新版，更先进）

    - 支持**内置工具调用**（如 web_search）
    - 支持**服务端维护状态**

    python

    ```
    response = client.responses.create(
        model="gpt-5.1",
        input="...",
        tools=[{"type": "web_search"}]
    )
    print(response.output_text)
    ```

    

    ⭐ **大部分国内模型（Qwen、DeepSeek）兼容 OpenAI 接口规范**，可用上述方式调用。

- **Token概念（🔥 计费与限制依据）**：

  - 最小处理单位，1个中文 ≈ 1~1.8 个汉字，1个英文 ≈ 3~4 个字母。
  - **可视化工具**：OpenAI Tokenizer / 百度智能云 Tokenizer（务必实际操作感受一下）。

------

### 1.2.4 LangChain API 调用模型（⭐ 框架核心价值）

- **为什么用LangChain？** 封装不同厂商SDK的复杂出入参，**提供统一调用接口**。
- **核心步骤**：
  1. **构造实例**：`init_chat_model`（统一）或 `ChatOpenAI`（特定包）。
  2. **关键参数**：`model`、`base_url`、`api_key`、`temperature`（随机性）、`max_tokens`（输出长度限制）。
  3. **调用方式（生产必备）**：
     - **同步**：`invoke`（基础）。
     - **异步**：`ainvoke`（🔥 高并发/高性能场景必用）。
     - **流式**：`stream`（实现“打字机”效果，提升用户体验）。
     - **批处理**：`batch`（底层多线程并行，节省总耗时）。
  4. **消息类型**：`SystemMessage`（设定人设）、`HumanMessage`（用户）、`AIMessage`（模型回复）、`ToolMessage`（工具结果）。

> 💡 **最佳实践**：传递**消息列表**而非裸字符串，以支持多轮对话历史。

------

## 1.3 调用本地模型 (Ollama)

- **定位**：**仅用于本地原型设计和开发测试**。生产环境部署请用 vLLM 等框架。
- **支持**：Qwen、DeepSeek 等 LLaMA 架构模型。
- **调用**：通过 `langchain_ollama.ChatOllama` 无缝接入 LangChain 体系。

------

## 1.4 模型调用结果解析（🔥 结构化输出）

**痛点**：模型返回自然语言，无法直接用于程序逻辑判断。

### 两种获取JSON的方式（核心对比）：

1. **通过Prompt约束（传统方式）**：
   - 配合 `JsonOutputParser` 和 Pydantic Schema，将格式说明塞入 SystemMessage。
   - ⚠️ **缺点**：依赖模型智力，小参数模型容易“幻觉”，生成格式错误。
2. **通过厂商原生能力（🔥 强烈推荐）**：
   - OpenAI 用 `response_format`，Gemini 用 `response_json_schema`。
   - **LangChain 统一封装（必会）**：`new_llm = llm.with_structured_output(schema=YourPydanticModel)`。
   - ✅ **巨大优势**：换模型（OpenAI换Gemini）时，**只需改 `llm` 实例化代码，业务调用逻辑（`invoke`）完全不用动**！这正是 LangChain 的精髓所在。

------

## 1.5 提示词模板

- **作用**：将固定文本变为可插入变量的“填空模板”，提升复用性。
- **常用**：`ChatPromptTemplate.from_messages([("system", "..."), ("human", "请评价{product}")])`
- **调用**：`.invoke({"product": "iPhone"})` 输出标准的消息列表。

------

## 1.6 Chains（🔥 LCEL 与 Runnable 接口）

### 1.6.0 基石：Runnable 接口（LangChain 的基石）

- **定义**：所有组件（模型、解析器、提示词、甚至整个Chain）都实现了 `Runnable` 接口。
- **统一方法**：`invoke`、`batch`、`stream`。

> 💡 **灵魂追问**：为何要统一？没有统一前，提示词用 `.format`，模型用 `.generate`，解析用 `.parse`，组合起来极其混乱。统一后，所有组件调用方式完全一样！

### LCEL（LangChain 表达式语言）

- **核心操作**：使用管道符 `|` 将多个 Runnable 串联。
- **示例**：`chain = prompt | model | parser` → 调用 `chain.invoke(...)`。
- **本质**：自动处理类型匹配和中间结果传递，代码极其简洁优雅。

### 两种基本组合模式：

1. **RunnableSequence（顺序执行）**：
   - 前一个输出作为后一个输入。
   - 典型：提示词 → 模型 → 解析器。
2. **RunnableParallel（并行执行）**：
   - 同一输入，同时喂给多个 Runnable（如同时让GPT和DeepSeek回答）。
   - 构造方式：`{"分支1": chain1, "分支2": chain2}`。
   - 结果汇总为字典，供后续步骤使用。

> 💡 **实战技巧**：常用于同时请求多个模型对比结果，或者先并行处理多个维度，再汇总总结。

### 其他组件（了解即可）：

- `RunnableLambda`（封装自定义函数）、`RunnableBranch`（条件路由）、`RunnablePassthrough`（透传上下文）。

------

## 🔥 终极趋势与学习建议

- **当前趋势**：LangChain 的核心正从 **Chain（链式）** 转向 **Agent（代理）**，构建方式也从 **LCEL** 转向 **LangGraph**（支持循环和状态管理）。
- **学习定位**：**Chain 和 LCEL 是基础，必须理解其思想**，但在实际最新项目中，直接写复杂 Chain 的场景在减少。看懂源码、理解 `Runnable` 接口即可，**不必过度深入复杂的 Chain 嵌套**，后续重心应放在 LangGraph 上。