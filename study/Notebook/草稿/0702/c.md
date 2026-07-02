# 第3章 Model I/O与Chains

------

## 1. Model I/O 介绍

**核心三要素**：输入（Prompt） → 处理（Model） → 输出（Parser）。

- **输入**：构造提示（Prompt Template）
- **处理**：调用模型（Model）
- **输出**：解析结果（Output Parser）

> ⭐ 这是与语言模型交互的基础流程，LangChain 的所有高级组件都建立在此之上。

------

## 2. 调用在线模型

### 2.1 常用大模型服务平台

- **CloseAI**（代理）、**OpenRouter**、**阿里云百炼**、**百度千帆**、**硅基流动**
- 使用方式：注册 → 充值 → 创建 API‑Key → 获取 `BASE_URL`

⚠️ **API_KEY 为敏感信息，严禁硬编码**。必须通过环境变量管理。

### 2.2 配置环境变量（两种方式）

#### 方式一：`.env` 文件（项目级）

```bash
# .env 文件内容
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai-proxy.org/v1
```

```python
from dotenv import load_dotenv
import os
load_dotenv()#加载.env文件
api_key = os.getenv("OPENAI_API_KEY")#通过os模块读取环境变量
```

⚠️ **切记**：`.env` **不要**提交到 Git 仓库（加入 `.gitignore`）。

#### 方式二：系统全局环境变量（Windows/Linux）

适合学习环境，避免反复 `load_dotenv()`。

------

### 2.3 OpenAI SDK 调用模型

#### ChatCompletion API（经典）

```python
from openai import OpenAI
client = OpenAI(base_url=..., api_key=...)
completion = client.chat.completions.create(
    model="gpt-4o-mini",# 调用创建的这个client进行聊天的创建
    messages=[{"role": "user", "content": "翻译"}])
print(completion.choices[0].message.content)	
```

#### Responses API（2025 年新推出，支持内置工具调用和服务端状态维护）

```python
response = client.responses.create(
    model="gpt-4o-mini",
    input="..查询天气.",
    tools=[{"type": "web_search"}]
)
print(response.output_text)
```

⭐ **大部分国内模型（Qwen、DeepSeek）兼容 OpenAI 接口规范**，可用上述方式调用。

------

### 2.4 Google SDK 调用 Gemini（了解）

python

```python
from google import genai
client = genai.Client(api_key=..., http_options={"base_url": ...})
response = client.models.generate_content(model="gemini-2.5-flash-lite", contents="..hello.")
```

------

### 2.5 LangChain API 调用模型（重点）

LangChain 封装了不同厂商的 SDK，提供**统一接口**(尤其是结构化输出等复杂场景)

```bash
#安装对应包
pip install langchain-openai   # OpenAI
pip install langchain-deepseek # DeepSeek
```

#### 两种构造 LLM 实例的方式

使用LangChainAPI进行调用的步骤如下：

1）构造LLM ChatModel实例

2）传递Message对象列表或普通字符串对象，调用LLM实例

3）解析调用结果

1. **统一工厂方法 `init_chat_model`**

```python
from langchain.chat_models import init_chat_model
# 定义出一个大模型对象
llm = init_chat_model(
    model_provider="openai",
    model="gpt-4o-mini",
    base_url = os.getenv("OPENAI_BASE_URL"),
    api_key = os.getenv("OPENAI_API_KEY")
    temperature=0.0,   # 控制随机性
    max_tokens=100,    # 限制输出长度
    timeout=30,
    max_retries=2)
response = llm.invoke("你好")# 调用大模型对象
```

2. **特定包下的类**（如 `ChatOpenAI`）

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini", ...)
```

⭐ 两者本质相同，`init_chat_model` 底层调用特定类。

| `model`          | 模型名称或标识符，例如gpt-4o-mini               |
| ---------------- | ----------------------------------------------- |
| `model_provider` | 模型提供厂商,例如：openai                       |
| `base_url`       | 发送请求的 API 端点的 URL。常由模型的提供商提供 |
| `api_key`        | 与模型提供商进行身份验证所需的 API 密钥         |
| `temperature`    | 越高越随机，越低越确定                          |
| `max_tokens`     | 限制输出 token 数（1 个中文 ≈ 1~1.8 个 token）  |
| `timeout`        | 请求超时秒数                                    |
| `max_retries`    | 失败重试次数                                    |

**Token 可视化工具**：[OpenAI Tokenizer](https://platform.openai.com/tokenizer) 或 [百度智能云](https://console.bce.baidu.com/support/#/tokenizer) 

------

#### 调用 LLM 实例的方式

##### 输入类型(`四种重点`)

- **字符串**：简单任务
- **消息列表**（推荐用于对话历史）：

```python
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
messages = [
    SystemMessage(content="你是一个小狗，只会汪汪叫，被踹了会逃跑"),
    HumanMessage(content="（吹了个口哨）"),
    AIMessage(content="汪汪！"),
    HumanMessage(content="哪来的狗？（踹了你一脚）")]
resp = llm.invoke(messages)
```

- **元组/字典**形式也支持：

```python
[("system", "指令"), ("user", "问题")]
[{"role": "system", "content":"给llm指令"}, {"role": "user", "content": "问题"}]
```

| 消息类型        | 用途                     |
| :-------------- | :----------------------- |
| `SystemMessage` | 设定角色、语气、规则     |
| `HumanMessage`  | 用户输入                 |
| `AIMessage`     | 模型回复（含元数据）     |
| `ToolMessage`   | 工具调用结果（特殊场景） |

##### 调用方式

- **同步**：`.invoke(input)`
- **异步**：`.ainvoke(input)` – 提升响应性能
- **流式**：`.stream(input)` – 实现打字机效果
- **批量**：`.batch([inputs])` – 并行处理多个请求

```python
# 异步示例
async def async_invoke():
    llm = ChatOpenAI(model = "gpt-4o-mini")
    response = await llm.ainvoke("你好")
    print(response.content)
# 流式示例
response = llm.stream(
    "写一个1000字的短片小说，要求感人且荒诞中带有意思人性的光辉"
)
for chunk in response:
    print(chunk.content,end="")
#批量调用（了解）
```

------

## 3. 调用本地模型（Ollama）

### Ollama 简介

- 本地运行大模型的集成框架（支持 Qwen、DeepSeek 等）
- 适用于**原型开发**，生产环境建议用 vLLM

### 安装与模型下载

- 官网：[https://ollama.com](https://ollama.com/)⚠️ 生产环境通常使用 vLLM 等专业部署框架。
- 下载后通过 `ollama pull qwen3:8b` 拉取模型

### LangChain 调用

```python
from langchain_ollama import ChatOllama
ollama_llm = ChatOllama(model="qwen3:8b")
resp = ollama_llm.invoke([HumanMessage("你好")])
print(resp.content)
```

------

## 4. 模型调用结果解析（重点）

### 4.1 获取 JSON 结构化输出(高频)*

#### 方式一：通过 Prompt 约束（通用）

使用 `JsonOutputParser` + Pydantic 定义 Schema

```python
#导包（略）
load_dotenv()# 加载环境变量
llm = ChatOpenAI(model = "gpt-4o-mini")# 注册一个大模型对象
# 规定输出的数据类型
class Prime(BaseModel):
    prime: list[int] = Field(description="素数")
    count: list[int] = Field(description="个数")
# 构造一个解析器对象    
parser = JsonOutputParser(pydantic_object=Prime)
#生成一段用于“提示词（Prompt）”的文本指令，告诉大模型（LLM）应该以什么具体的格式返回内容，以便解析器能够成功解析
system_prompt = parser.get_format_instructions()
# 通过大模型进行调用
response = llm.invoke([# 将 system_prompt 放入 system 消息
       	("system",system_prompt),
        ("user","任意生成5个1000-100000之间素数，并标出小于该素数的素数个数")])
print(response.content)#大模型原始响应文本
print("============================================================")
json_output = parser.invoke(response)
print(json_output)#解析后的结构化对象
```

> **加载环境** → 2. **创建 LLM 实例** → 3. **定义 Pydantic 模型** → 4. **创建解析器** → 5. **生成系统提示** → 6. **发送请求** → 7. **获得原始文本** → 8. **解析并校验** → 9. **得到结构化字典**

#### 方式二：利用厂商原生能力（推荐）

- OpenAI：`client.chat.completions.parse(..., response_format=CalendarEvent)`

  ```python
  load_dotenv()  # 从 .env 文件加载环境变量（如 OPENAI_API_KEY）
  
  def openai_json_output_demo():
      import os                     # 导入 os 模块（虽然此处未直接使用，但通常用于读取环境变量）
      from openai import OpenAI     # 导入 OpenAI 官方 SDK 的客户端类
      from pydantic import BaseModel  # 导入 Pydantic 基类，用于定义数据模型
  
      client = OpenAI()             # 实例化 OpenAI 客户端（会自动从环境变量中读取 API Key）
  
      # 使用 Pydantic 定义希望模型输出的数据结构
      class CalendarEvent(BaseModel):
          name: str                 # 事件名称
          date: str                 # 事件日期
          participants: list[str]   # 参与者列表
  
      # 调用 OpenAI 的聊天补全接口，并使用 .parse() 方法
      response = client.chat.completions.parse(
          model="gpt-4o-mini",      # 使用轻量级模型
          messages=[                # 用户消息
              { "role": "user",
                 "content": "Alice and Bob are going to a science fair on Friday.",}],
          response_format=CalendarEvent  # 关键：强制模型输出符合 CalendarEvent 结构的 JSON
      )
  
      # 从响应中直接获取解析后的 Pydantic 对象（已自动校验和转换）
      print(response.choices[0].message.parsed)
      # 输出类似：name='Science Fair' date='Friday' participants=['Alice', 'Bob']
  
      print(type(response.choices[0].message.parsed))  # <class '__main__.CalendarEvent'>
  ```

  

- Gemini：`config={"response_mime_type":"application/json", "response_json_schema": schema}`

  ```python
  def gemini_json_output_demo():
      import os
      from google import genai                      # Google 官方 GenAI SDK（支持 Gemini）
      from pydantic import BaseModel, Field        # Pydantic 用于定义数据模型和字段描述
      from typing import List, Optional            # 类型提示（本示例未使用，但可保留）
  
      # 1、定义一个 Pydantic 模型，表示日历事件的结构
      class CalendarEvent(BaseModel):
          name: str                                # 事件名称
          date: str                                # 事件日期
          participants: list[str]                  # 参与者名单（字符串列表）
  
      # 2、初始化 Gemini 客户端
      client = genai.Client(
          api_key=os.getenv("OPENAI_API_KEY"),     # ⚠️ 注意：这里从环境变量取的是 OPENAI_API_KEY
          # 但实际上应该使用 GOOGLE_API_KEY 或 GEMINI_API_KEY，除非代理服务统一使用 OpenAI 格式的密钥。
          vertexai=True,                           # 启用 Vertex AI 协议（Google Cloud 的托管服务），可提高稳定性
          http_options={
              "base_url": 'https://api.openai-proxy.org/google',  # 自定义代理地址，用于转发请求到 Gemini
          },
      )
  
      # 3、定义用户提示（简单描述一个场景）
      prompt = """
      Alice and Bob are going to a science fair on Friday.
      """
  
      # 4、调用 Gemini 模型生成内容，并强制输出 JSON 格式
      response = client.models.generate_content(
          model="gemini-2.5-flash-lite",           # 使用轻量级快速模型
          contents=prompt,                         # 输入文本
          config={
              "response_mime_type": "application/json",        # 要求模型返回 MIME 类型为 JSON 的数据
              "response_json_schema": CalendarEvent.model_json_schema(),  # 提供 JSON Schema 约束输出结构
          },
      )
  
      # 打印原始响应文本（应为合法的 JSON 字符串）
      print(response.text)
  
      # 5、解析 Gemini 返回的 JSON 字符串，转换为 CalendarEvent 对象
      event = CalendarEvent.model_validate_json(response.text)   # Pydantic 内置方法，直接从 JSON 字符串解析并验证
      print(event)          # 打印对象，显示字段值
      print(type(event))    # 输出 <class '__main__.CalendarEvent'>
  ```

⭐ **LangChain 统一封装 `with_structured_output`**（最推荐）

```python
# 此脚本用于尝试使用LangChain封装模型厂商提供的输出解析功能
# 需要在调用的时候，将输出的数据类型作为参数一起上传过去
llm = ChatOpenAI(model ="gpt-4o-mini")

# 定义返回的数据类型
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]
# 将返回类型的这个类，注册到大模型对象中
new_llm = llm.with_structured_output(schema = CalendarEvent)

response = new_llm.invoke("Alice and Bob are going to a science fair on Friday.")
```

**优势**：无论底层是 OpenAI、Gemini 或其他，调用方式完全一致，换模型只需修改实例化代码。

### 4.2 其他解析器

LangChain 提供多种解析器（XML、逗号分隔列表等），但 **JSON 是主流**，大部分场景够用。

- `StrOutputParser`（最常用，返回字符串）
- `CommaSeparatedListOutputParser`
- `XMLOutputParser`
- `PydanticOutputParser`（旧版，现多用 `JsonOutputParser`）

------

## 5. 提示词模板

作用：将变量插入模板，动态生成提示，避免硬编码。

### 常用模板

- `PromptTemplate`：字符串模板
- `ChatPromptTemplate`：聊天消息模板（推荐）

```python
from langchain_core.prompts import ChatPromptTemplate
# 使用构造方法实例化提示词模板
template = ChatPromptTemplate.from_messages(
    messages=[("system", "你是一个专业的评论员"),
    ("human", "请评价{product}的优缺点，包括{aspect1}和{aspect2}。")
])
prompt_value = template.invoke({"product": "iPhone 15", "aspect1": "性能", "aspect2": "外观"})
# 可直接传给 llm.invoke()	
llm = ChatOpenAI(model = "gpt-5.5")
response = llm.invoke(prompt)
```

------

## 6. Chains 与 LCEL（核心概念 ，重点）

### 6.1 Runnable 接口

LangChain 所有核心组件（模型、解析器、提示模板等）都实现 **`Runnable`** 接口，统一了：

- `invoke` / `ainvoke`
- `batch` / `abatch`
- `stream` / `astream`

**为什么要统一？** 否则每个组件调用方法不同（`.format()`, `.generate()`, `.parse()`），组合困难。

### 6.2 LCEL（LangChain 表达式语言）

用 **管道符 `|`** 将多个 Runnable 串联成链：

```python
# 此脚本演示使用LangChain中的链式处理
# 搭建了一个Runnable的链，链里面有几个组件，首尾相连。
# 前者的输出，作为后者的一个输入
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
# 构建第一个组件 -> 提示词模板
prompt_template = PromptTemplate(
    template="讲一个关于{topic}的冷笑话",
    input_variables=["topic"]
)
# 构建第二个组件 -> 大模型对象
llm = ChatOpenAI(model = "gpt-5.5")

# 构建第三个组件 -> 输出解析器
parser = StrOutputParser()

# 构建链，实现三个组件的连接操作
chain = prompt_template | llm | parser

response = chain.invoke({"topic":"鼠标"})

print(response)
```

链本身也是 Runnable，可继续组合。

### 6.3 RunnableSequence（顺序执行）

按顺序传递输出→输入：

```python
chain = prompt_template | llm | StrOutputParser()
```

### 6.4 RunnableParallel（并行执行）

同时运行多个 Runnable，输入相同，输出合并为字典。

python

```python
# 此脚本用于展示链的并行运行（同时运行多条链）
load_dotenv()

# 英文翻译链的提示词模板组件
english_prompt_template = PromptTemplate.from_template("把这句话翻译成英文：{topic}")
# 韩文翻译链的提示词模板组件
korean_prompt_template = PromptTemplate.from_template("把下面这句话翻译成韩文：{topic}")

# 定义大模型对象的组件
llm = ChatOpenAI(model = "gpt-4o-mini")
# 定义字符串的解析器
parser =  StrOutputParser()

# 定义两条链
english_chain = english_prompt_template | llm | parser
korean_chain = korean_prompt_template | llm | parser

map_chain = RunnableParallel(
    english = english_chain,
    korean = korean_chain
)

response = map_chain.invoke({"topic":"我爱尚硅谷"})
print(response)
```

在 LCEL 中，用字典字面量即可：

```python
map_chain = {
    "para1": chain1,
    "para2": chain2
} | summary_chain   # 并行执行后再汇总
```

提升

```python
# 定义出大模型对象，作为组件添加到链中
llm = ChatOpenAI(model = "gpt-5.5")
# 定义出解析器对象，作为组件添加到链中
parser = StrOutputParser()

prompt_template_1 = PromptTemplate.from_template("正面评价一下{topic}这个问题")
prompt_template_2 = PromptTemplate.from_template("负面评价一下{topic}这个问题")

prompt_template_sum = PromptTemplate.from_template("根据这两个分析：{view_1},和{view_2},给出一个汇总的结果")

chain_1 = prompt_template_1 | llm | parser
chain_2 = prompt_template_2 | llm | parser
chain_sum = prompt_template_sum | llm |parser
# 构建第四个链 -> 映射链
map_chain = {
    "view_1":chain_1,
    "view_2":chain_2
} | chain_sum

response = map_chain.invoke({"topic":"加班"})
print(response)
```



#### 6.5 其他 Runnable 组件（了解）

| 组件                    | 用途                      |
| :---------------------- | :------------------------ |
| `RunnableLambda`        | 将普通函数包装成 Runnable |
| `RunnableBranch`        | 条件分支路由              |
| `RunnablePassthrough`   | 透传输入，保留上下文      |
| `RunnableWithFallbacks` | 失败时回退到备用链        |

------

## 7. 补充说明与趋势

- **Chain 的地位**：随着 Agent 的火热，LangChain 核心正从链式结构转向 **LangGraph**（支持循环、状态管理）。但 Chain 概念在源码和简单流程中仍然常见，理解 LCEL 有助于阅读底层实现。
- **生产建议**：
  - 环境变量务必安全隔离
  - 优先使用 `with_structured_output` 获取类型安全的 JSON
  - 使用异步/流式提升用户体验
  - 本地原型用 Ollama，生产部署用 vLLM 等专业框架

------

`标注` ⭐ 和 ⚠️ 处为高频考点或易错点，需特别留意。