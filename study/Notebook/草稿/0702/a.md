第 3 章 Model I/O与Chains

1.1 Model I/O 介绍

Model I/O 部分是与语言模型进行交互的核心组件，包括输入提示（Prompt Template）、调用模型（Model）、输出解析（Output Parser）。简单来说，就是输入、处理、输出这三个步骤。



1.2 调用在线模型

1.2.1 常用大模型服务平台介绍

有许多提供大模型API服务的平台，如下所示：

Ø CloseAI：https://platform.closeai-asia.com/，可提供国外OpenAI, Anthropic，Google等公司最新模型调用代理；

Ø OpenRouter：https://openrouter.ai/，提供闭源模型和开源模型调用代理；

Ø 阿里云百炼：https://bailian.console.aliyun.com/，提供大模型API调用、模型微调、模型评测等一系列服务，是一站式大模型应用开发平台；

Ø 百度千帆：https://console.bce.baidu.com/qianfan/overview，类似于阿里云百炼，同样为一站式企业级大模型开发与应用平台；

Ø 硅基流动：https://www.siliconflow.cn/，类似上两个平台，不再赘述。

使用时只需要注册、充值并创建API-Key，之后即可使用API-Key与BASE_URL来调用平台提供的相应的模型的服务。

API_KEY为敏感信息，在不同的平台获取到API_KEY之后，需要将API_KEY和BASE_URL通过环境变量存储起来，后续在实际调用时，需要加载环境变量后，从环境变量当中读取，而不是直接硬编码在业务代码当中。

配置环境变量有两种方式：

1）通过.env文件配置，适用于实际项目当中

通过.env配置过程如下：

（1）在项目根目录中创建.env文件，添加环境变量：此处以OPENAI_BASE_URL和OPENAI_API_KEY为例

（2）在代码当中通过dot_env模块（需要安装包：python-dotenv）的load_dotenv方法加载环境变量 

（3）在代码当中通过os模块读取环境变量

.env文件内容如下所示：

OPENAI_API_KEY=sk-xxx

OPENAI_BASE_URL=https://api.openai-proxy.org/v1

读取示例如下所示：

\# pip install python-dotenv

```python
\# 1、从dotenv导入load_dotenv方法
from dotenv import load_dotenv 
\# 2、调用load_dotenv方法加载.env文件
load_dotenv() 
\# 3、通过os模块读取环境变量
import os
api_key = os.getenv("OPENAI_API_KEY")
print(api_key)
```



**在实际开发过程中，一定要注意：不要将.env****放在git****管理目录当中，避免数据泄露**。

2）在Windows当中配置全局环境变量，适用于学习环境下，经常需要使用到的某些环境变量。

本课程当中，会将部分环境变量，通过Windows做全局配置，避免重复执行load_dotenv操作：

​                               

1.2.2 OpenAI SDK 调用模型

OpenAI 的 GPT 系列模型影响了大模型技术发展的开发范式和标准。大部分模型，例如 Qwen、ChatGLM、DeepSeek 等模型，它们的使用方法和函数调用逻辑基本遵循 OpenAI 定义的规范，都可以使用OpenAI SDK来进行调用。

OpenAI的接口调用方式也经历的一些转变，其中最为经典的一套API，称之为**ChatCompletionsAPI**（官方文档链接：https://platform.openai.com/docs/api-reference/chat）。

而在2025年年中，OpenAI又发布了一套新的API: ResponsesAPI（官方文档链接：https://platform.openai.com/docs/api-reference/responses）。

ResponsesAPI是当前OpenAI中最先进的一套API，对ChatCompletionsAPI做了多处升级，例如，支持服务端内置工具调用，支持服务端维护状态（短期记忆）等。

1）ChatCompletionAPI 调用示例

```python
\# pip install openai

from openai import OpenAI

import os

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(

  base_url=os.getenv("OPENAI_BASE_URL"),  # 平台提供的 URL

  api_key=os.getenv("OPENAI_API_KEY"),  # 平台提供的 API-Key

)
completion = client.chat.completions.create(

  model="gpt-4o-mini",  # 模型名称

  messages=[{"role": "user", "content": "将'你好'翻译成意大利语"}],  # 用户输入
)
print(completion.choices[0].message.content)
```

2）ResponsesAPI调用示例

```python
import os

from openai import OpenAI

 

client = OpenAI()

 

response = client.responses.create(

  model="gpt-5.1",

  input="中国国内今天发生了哪些大事儿？",

  tools=[{"type": "web_search"}] # 可以自动调用内置工具

)

 

print(response.output_text)

```

1.2.3 Google SDK 调用模型（了解）

如果需要调用Gemini相关模型，需要使用google的SDK，以下为一个具体的调用示例：

```python
# pip install google-genai
def call_gemini():
    import os
    from google import genai
    from dotenv import load_dotenv
    load_dotenv()
    client = genai.Client(
        api_key=os.getenv("OPENAI_API_KEY"), 
        http_options={
            "base_url": 'https://api.openai-proxy.org/google' # 此处需要根据个人所选择的大模型服务平台去做具体调整
        },
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="你是谁，能做什么",
    )
print(response.text)
```



1.2.4 LangChain API 调用模型

通过上面两个例子，可以看到，对于不同厂商的模型，需要学习不同的SDK的API来进行调用（**注意**：虽然大部分模型厂商可以兼容OpenAI SDK规范，但是对于复杂场景下，例如后面会学习到的结构化输出等场景，各厂商之间具体构造参数的方式仍有差别），而通过LangChain调用API，其封装了不同模型调用时，复杂的出入参的构建和解析，得到llm对象之后，我们可以通过统一的方法来进行模型调用和结果解析。

在使用langchain进行模型调用时，需要先安装相应的包。对于OpenAI，需要安装langchain-openai包，而如果需要使用DeepSeek的模型，则需要安装langchain-deepseek。（具体可参考官网：https://docs.langchain.com/oss/python/integrations/providers/overview）。

使用LangChainAPI进行调用的步骤如下：

1）构造LLM ChatModel实例

2）传递Message对象列表或普通字符串对象，调用LLM实例

3）解析调用结果

 

1.2.4.1 构造LLM ChatModel实例

LLM ChatModel实例代表了一个可调用的LLM对象，有两种方式进行初始化，

1）langchain提供的统一方法init_chat_model；

2）使用特定包下（例如langchain-openai）下的ChatModel类（例如langchain_openai 下的ChatOpenAI类）。

下面首先介绍init_chat_model的初始化参数，代码示例如下：

```python
# pip install langchain
# pip install langchain-openai
def get_model_from_init():
    import os
    import dotenv
    dotenv.load_dotenv()
    from langchain.chat_models import init_chat_model

    llm = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    resp = llm.invoke("你好")
    print(type(resp))  # <class 'langchain_core.messages.ai.AIMessage'>
    print(resp.content) # 获取结果

```

init_chat_model所接收的相关参数如下面所示：



| **参数**           | **说明**                                                     |
| ------------------ | ------------------------------------------------------------ |
| **model**          | 模型名称或标识符，例如gpt-4o-mini                            |
| **model_provider** | 模型提供厂商,例如：openai                                    |
| **base_url**       | 发送请求的 API 端点的 URL。常由模型的提供商提供              |
| **api_key**        | 与模型提供商进行身份验证所需的 API 密钥                      |
| **temperature**    | 控制模型输出的随机性。数字越高，回答越有创意；数字越低，回答越确定，涉及到大模型采样相关内容（https://zhuanlan.zhihu.com/p/1981752176578667658） |
| **timeout**        | 在取消请求之前，等待模型响应的最大时间（以秒为单位）         |
| **max_tokens**     | 限制响应中的总tokens 数量，控制输出长度                      |
| **max_retries**    | 请求失败时系统尝试重新发送请求的最大次数                     |



在此处介绍下max_tokens所涉及到的token的概念：大模型处理的最小单位是 token（相当于自然语言中的词或字），输出时逐个 token 依次生成。模型提供商通常也是以 token 的数量作为其计量或收费的依据。1个中文Token≈1-1.8个汉字，1个英文Token≈3-4字母。

Token与字符转化的可视化工具：

Ø OpenAI提供：https://platform.openai.com/tokenizer

Ø 百度智能云提供：https://console.bce.baidu.com/support/#/tokenizer

使用特定包下的类构造LLM实例和init_chat_model在本质上是一样的（init_chat_model底层就是调用特定包下的类构造LLM实例），参考代码如下所示：

```python
def get_model_from_openai_package():
    import os
    import dotenv
    dotenv.load_dotenv()
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    resp = llm.invoke("你好")
    print(type(resp))
    print(resp.content)

if __name__ == "__main__":
    get_model_from_openai_package()
```

对于其他厂商，代码类似，此处不再赘述。



1.2.4.2 调用LLM实例

调用LLM实例时，有两处需要关注：调用传入的对象类型和调用方式。

1）调用传入对象类型

前面的例子当中，我们直接传入字符串对象，这通常适用于不需要保留对话历史的直接生成任务。

除此以外，更加好的方式是传入一个消息列表：

```python
def invoke_llm_with_message_list():
    import os
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    resp = llm.invoke([SystemMessage(content="你是一个专业的数学助手"),HumanMessage(content="你好，你是谁")])
    print(type(resp))
    print(resp.content)

if __name__ == "__main__":
    invoke_llm_with_message_list()

```

消息列表表示了一段“聊天记录历史”；而不同的消息类型，则代表了不同的角色，各种类型及相关描述如下：

| **消息类型**      | **描述**                                                     |
| ----------------- | ------------------------------------------------------------ |
| **SystemMessage** | 代表一组初始指令，用于引导模型的行为。可以使用系统消息来设定语气、定义模型的角色，并建立响应的指导方针 |
| **HumanMessage**  | 表示用户输入，可以在message当中传递其他元数据信息            |
| **AIMessage**     | 模型生成的响应，包括文本内容、工具调用和token使用量等元数据信息 |
| **ToolMessage**   | 表示工具调用的输出                                           |

HumanMessage、AIMessage 和 SystemMessage 是常用的消息类型。

ToolMessage 是在工具调用场景下才会使用的特殊消息类型。

消息对象，除了使用HumanMessage等类以外，还可以通过元组对象来表示，元组对象第一个元素表示角色，第二个元素表示具体消息内容；也可以通过OpenAI官方使用的dict来表示，dict当中有两个键，第一个为role，表示角色，第二个为content，表示内容。

示例代码如下：

```python
def invoke_llm_with_message_list_use_tuple():
    import os
    import dotenv
    dotenv.load_dotenv()
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    # 以下两种方式是等价的
    messages_list = [("system","你是一个专业的数学助手"),("user","你好，你是谁")]
    message_list = [{"role":"system","content":"你是一个专业的数学助手"},{"role":"user","content":"你好，你是谁"}]
    resp = llm.invoke(message_list)
    print(type(resp))
    print(resp.content)

if __name__ == "__main__":
invoke_llm_with_message_list_use_tuple()
```

2）调用方式

除了上述调用方式外，LangChain的LLM对象还支持异步调用、流式调用、批调用等多种方式。

**异步调用**在实际生产环境下非常实用，可以大大提高程序的响应性能，示例代码如下：

```python
import asyncio
async def call_llm_async():

    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini"
    )
    response = await llm.ainvoke(
        input=[("user", "什么是LangChain")]
    )
    print(response.content)

if __name__ == "__main__":
    asyncio.run(call_llm_async())
```

**流式调用**，可以让大模型输出结果实现打字机效果，示例代码如下：

```python
def call_llm_streaming_mode():

    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini"
    )
    # 调用stream方法，返回迭代器对象
    response = llm.stream(
        input=[("user", "什么是LangChain")]
    )
    # 遍历迭代器对象，打印每个chunk的内容
    for chunk in response:
        print(chunk.content,end="")

call_llm_streaming_mode()
```

**批次调用**，可以并行发出多个请求，统一回收相关结果，示例代码如下：

```python
def call_llm_batch_mode():
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini"
    )
    # 调用batch方法，底部通过thread 并行调用模型
    response = llm.batch(
        inputs=[[("user", "什么是LangChain")],("user","LangChain的核心价值是什么呢？")]
    )
    # 打印每个问题的回答
    for question_chunk in response:
        print(question_chunk.content)

call_llm_batch_mode()
```

1.3 调用本地模型

1.3.1 Ollama介绍

Ollama是一个开源项目，其项目定位是：一个本地运行大模型的集成框架。目前主要针对主流的LlaMA架构的开源大模型设计，可以实现如 Qwen、Deepseek 等主流大模型的下载、启动和本地运行的自动化部署及推理流程。注意：Ollma主要用于原型设计和本地开发等，实际生产环境下做大模型部署会使用VLLM等框架。

Ollama目前作为一个非常热门的大模型托管平台，已被包括LangChain、Taskweaver等在内的多个热门项目高度集成。

Ollama官方地址：https://ollama.com 

Ollama Github开源地址：https://github.com/ollama/ollama 

1.3.2 Ollama安装。

1.3.3 模型下载

1.3.4 调用本地模型

举例：

```python
# pip install langchain-ollama
from langchain_ollama import ChatOllama

ollama_llm = ChatOllama(model="qwen3:8b")
messages = [HumanMessage(content="你好，请介绍一下你自己")]

resp = ollama_llm.invoke(messages)
print(resp.content)

```

1.4 模型调用结果解析

当我们和模型进行对话时，模型会通过自然语言进行回复。在对话式场景下，这没有什么问题，但是对于在实际生产环境当中，将大模型用以非对话场景，或者对话场景下的中间产出时，我们希望模型以一种更加结构化的方式进行输入，例如JSON等，而LangChain设计了一系列包（例如langchain_core.output_parsers）和方法专门用来解决此类问题。

1.4.1 获取JSON结果

要想大模型输出Json字符串，有两种方式：

（1）在Prompt当中明确约束大模型输出Json；

（2）通过部分厂商直接提供的接口参数进行限制。

1.4.1.2 通过Prompt约束

要使用Prompt明确约束大模型输出，需要使用到langchain所提供的JSONOutputParser,整体流程如下：

（1）通过Pydantic定义Json schema；

（2）使用构造好的JSON Schem构造JsonOutputParser实例json_parser；

（3）调用json_parser的get_format_information()方法，将json结构输出约束，放到SystemMessage当中；

（4）将SystemMessage和UserMessage都给到LLM，进行调用，结果使用json_parser.parse()方法，解析成PythonDict对象。

下面以一个具体实例来讲解，定义JSON结构：

```python
def json_output_parser():
    import os
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import JsonOutputParser
    from pydantic import BaseModel, Field
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    class Prime(BaseModel):
        prime: list[int] = Field(description="素数")
        count: list[int] = Field(description="小于该素数的素数个数")
    json_parser = JsonOutputParser(pydantic_object=Prime)
    # print(json_parser.get_format_instructions())
    res = llm.invoke([("system",json_parser.get_format_instructions()),("user","任意生成5个1000-100000之间素数，并标出小于该素数的素数个数")])
    print(res.content)
    parsed_res = json_parser.invoke(res)
    print(type(parsed_res))

```

Prompt约束，对于模型能力有一定依赖，如果模型参数不够强，容易出现幻觉，从而导致生成的JSON字符串语法有问题，或者是不符合我们所定义的JSON结构。

1.4.1.3 通过厂商能力

对于主流大模型厂商，其API已经提供了专门的参数，用以限制模型输出内容符合我们所定义的schema结构。

以OpenAI为例，其官方文档如下：https://platform.openai.com/docs/guides/structured-outputs

示例代码如下所示：

```python
def openai_json_output_demo():
    import os
    from openai import OpenAI
    from pydantic import BaseModel  

    client = OpenAI()

    class CalendarEvent(BaseModel):
        name: str
        date: str
        participants: list[str]

    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Alice and Bob are going to a science fair on Friday.",
            }
        ],
        response_format=CalendarEvent
    )

    print(response.choices[0].message.parsed)
```

再以Google Gemini为例，

```python
def gemini_json_output_demo():
    import os
    from google import genai
    from pydantic import BaseModel, Field
    from typing import List, Optional
    # 1、定义一个Pydantic模型，用于表示日历事件
    class CalendarEvent(BaseModel):
        name: str
        date: str
        participants: list[str]

    # 2、初始化Gemini客户端
    client = genai.Client(
        api_key=os.getenv("OPENAI_API_KEY"),
        vertexai=True, # 可选，优先使用vertexai协议访问，稳定性更高
        http_options={
            "base_url": 'https://api.openai-proxy.org/google',
        },
    )

    # 3、定义一个提示模板，用于生成日历事件
    prompt = """
    Alice and Bob are going to a science fair on Friday.
    """

    # 4、调用Gemini模型生成内容
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": CalendarEvent.model_json_schema(),
        },
        
    )

    print(response.text)
    
    # 5、解析Gemini模型的响应,将JSON字符串转换为CalendarEvent对象
    event = CalendarEvent.model_validate_json(response.text)
    print(event)

```

两个案例当中，都没有在Prompt当中明确指定以JSON输出，但是调用API返回结果仍然能够正确得到结果。

LangChain也对这种能力提供了封装：不同厂商的模型都是继承了ChatModel基类，而ChatModel提供了 with_structured_output方法，传入pydantic base model类作为schema对象，得到一个新的llm对象，调用新的llm对象即可。

具体代码如下所示：

```python
def json_output_use_langchain():
    import os
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
    from langchain_core.output_parsers import JsonOutputParser
    from pydantic import BaseModel, Field
    # 1、初始化llm: 可以使用OpenAI,也可以使用Gemini
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.0,
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY")
    )
    # llm = ChatGoogleGenerativeAI(
    #     model="gemini-2.5-flash-lite",
    #     temperature=0.0,
    #     base_url='https://api.openai-proxy.org/google',
    #     api_key=os.getenv("OPENAI_API_KEY"),
    # )

    # 2、定义一个Pydantic模型，用于表示日历事件
    class CalendarEvent(BaseModel):
        name: str
        date: str
        participants: list[str]
    
    #3、使用with_structured_output，得到一个新的llm，用于生成结构化输出
    new_llm=llm.with_structured_output(schema=CalendarEvent)
    #4、调用新的llm，生成结构化输出
    res = new_llm.invoke("Alice and Bob are going to a science fair on Friday.")
    print(res)
    print(type(res))

```

不管使用什么模型，都是调用统一的方法，就能够实现相关的需求，如果需要换模型，只需要调整llm实例化代码即可，其余代码无需改动，这正是LangChain框架的强大之处。

1.4.2 获取其他类型的解析结果

要想获取其他形式的结果，例如XML等，也可通过output_parser当中的其他类来实现，在output_parser包中提供的parser有如下：

__all__ = [

  "BaseCumulativeTransformOutputParser",

  "BaseGenerationOutputParser",

  "BaseLLMOutputParser",

  "BaseOutputParser",

  "BaseTransformOutputParser",

  "CommaSeparatedListOutputParser",

  "JsonOutputKeyToolsParser",

  "JsonOutputParser",

  "JsonOutputToolsParser",

  "ListOutputParser",

  "MarkdownListOutputParser",

  "NumberedListOutputParser",

  "PydanticOutputParser",

  "PydanticToolsParser",

  "SimpleJsonOutputParser",

  "StrOutputParser",

  "XMLOutputParser",

]

由于JSON的强大，对于其他类型，此处不再赘述，大部分场景下，使用JSON输出即可满足需求。



1.5 提示词模板

在应用开发中，固定的提示词限制了模型的灵活性和适用范围。通过提示词模板，我们可以将变量插入到模板中，从而创建出不同的Prompt。

LangChain当中有多种类型的提示模板，常用的有 PromptTemplate（字符串提示模板）和 ChatPromptTemplate（聊天提示模板）。

提示词模板以字典作为输入，其中每个键代表要填充的提示模板中的变量。并输出一个 PromptValue。这个 PromptValue 可以传递给聊天模型，也可以转换为字符串或消息列表。PromptValue 存在的目的是为了方便在字符串和消息之间切换。

以下使用PromptTemplate为例子做一个介绍：

```python
def prompt_template_demo():
    from langchain_core.prompts import ChatPromptTemplate
    from langchain.chat_models import init_chat_model
    # 使用构造方法实例化提示词模板
    chat_prompt_template = ChatPromptTemplate.from_messages(
        messages=[
            ("system", "你是一个专业的评论员"),
            ("human", "请评价{product}的优缺点，包括{aspect1}和{aspect2}。"),
        ],
    )

    chat_message_list = chat_prompt_template.invoke({"product": "iPhone 15", "aspect1": "性能", "aspect2": "外观"})

    llm = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
    )
    resp = llm.invoke(chat_message_list)
print(resp.content)

```

1.6 Chains

在前面的例子当中所涉及到的模型调用、解析器调用，以及对PromptTemplate调用，都使用到了invoke方法，这是因为这些类都实现了LangChain最底层定义的Runnable接口，其代表了LangChain 中可以调用、批处理、流式传输、转换和组合的工作单元，是使用 LangChain 组件的基础，它在许多组件中实现，例如语言模型、输出解析器、检索器、编译的 LangGraph 图等。

Runnable 接口定义了一系列标准的方法，如下所示：

| **invoke /  ainvoke** | **将单个输入转换为输出** |
| --------------------- | ------------------------ |
| **batch / abatch**    | 批量将多个输入转换为输出 |
| **stream / astream**  | 从单个输入生成流式输出   |
| …                     |                          |

为什么需要统一调用方式？

假设没有统一调用方式，每个组件调用方式不同，组合时需要手动适配：

Ø 提示词渲染用 .format()

Ø 模型调用用 .generate()

Ø 解析器解析用 .parse()

Ø 工具调用用 .run()

代码会变成：

```python
prompt_text = prompt.format(topic="猫")  # 方法1
model_out = model.generate(prompt_text)  # 方法2
result = parser.parse(model_out)  # 方法3
Runnable 统一调用方式：
# 分步调用
prompt_text = prompt.invoke({"topic": "猫"})  # 方法1
model_out = model.invoke(prompt_text)  # 方法2
result = parser.invoke(model_out)  # 方法3
```

所有实现了Runnable接口的组件，均可以通过一种特定的方式，将其连接起来，打包成一整个可调用对象，这也就是LangChain当中的Chain的由来，而这种方式则称之为LCEL。

LCEL （LangChain Expression Language），中文名称为LangChain 表达式语言，是一种从现有的Runnable 构建新的 Runnable 的声明式方法，用于声明、组合和执行各种组件（模型、提示、工具、函数等）。

```python
# LCEL管道式
chain = prompt | model | parser  # 用管道符组合
result = chain.invoke({"topic": "猫"})  # 所有组件统一用invoke
```

无论组件的功能多复杂（模型/提示词/工具），调用方式完全相同。并且可以通过管道符 | 组合，自动处理类型匹配和中间结果传递。

我们称使用 LCEL 创建的 Runnable 为“链”，“链”本身就是 Runnable。

LCEL 两个主要的组合原语是 RunnableSequence 和 RunnableParallel。许多其他组合原语可以被认为是这两个原语的变体。

1.6.1 RunnableSequence 可运行序列

RunnableSequence 按顺序“链接”多个可运行对象，其中一个对象的输出作为下一个对象的输入。

LCEL重载了 | 运算符，以便从两个 Runnables 创建 RunnableSequence。

```python
chain = runnable1 | runnable2

# 等同于

chain = RunnableSequence([runnable1, runnable2])
```

举例：提示模板➡️模型➡️输出解析器

```python
import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt_template = PromptTemplate(
    template="讲一个关于{topic}的笑话",
    input_variables=["topic"],
)

llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai", # 注意，此处没有再传入base_url=xxx 是因为默认也会读取相关环境变量，
)

parser = StrOutputParser()

chain = prompt_template | llm | parser

resp = chain.invoke({"topic": "人工智能"})
print(resp)
```

1.6.2 RunnableParallel 可运行并行

RunnableParallel 同时运行多个可运行对象，并为每个对象提供相同的输入。

对于同步执行，RunnableParallel 使用 ThreadPoolExecutor 来同时运行可运行对象。对于异步执行，RunnableParallel 使用 asyncio.gather 来同时运行可运行对象。

构造RunnableParallel实例时，参数列表是可变数量关键字参数，一个参数名对应着一个可运行组件，每个可运行组件输出结果将作为参数名key所对应的值，封装到整个运行实例的结果当中。

具体代码如下所示：

```python
def runnable_parallel_demo():

    import os
    from langchain.chat_models import init_chat_model
    from langchain_core.prompts import PromptTemplate
    from langchain_core.runnables import RunnableParallel
    from langchain_core.output_parsers import StrOutputParser

    llm = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
    )

    english_chain = (
        PromptTemplate.from_template("把这个句子{topic}翻译成英文") | llm | StrOutputParser()
    )
    korean_chain = (
        PromptTemplate.from_template("把这个句子{topic}翻译成韩文") | llm | StrOutputParser()
    )

    map_chain = RunnableParallel(english=english_chain, korean=korean_chain)

    resp = map_chain.invoke({"topic": "人工智能是一种智能技术"})
    print(resp)

if __name__ == "__main__":
runnable_parallel_demo()
```

在LCEL当中，要想定义并行运行结构，只需通过字典的方式定义即可，代码如下所示：

```python
def runnable_parallel_use_lcel_demo():

    import os
    from langchain.chat_models import init_chat_model
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    # 1、初始化两个模型
    llm = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
    )
    deepseek_llm = init_chat_model(
        model="deepseek-chat",
        model_provider="deepseek",
    )
    

    # 2、创建两个并行运行的chain：使用两个不同的模型回答同一个问题，用以对比结果
    paragraph_1_chain = (
        PromptTemplate.from_template("对这首诗{poem}做一下赏析，分析它蕴含的含义") | llm | StrOutputParser()
    )
    paragraph_2_chain = (
        PromptTemplate.from_template("对这首诗{poem}做一下赏析，分析它蕴含的含义") | llm | StrOutputParser()
    )

    # 3、对前面的两个chain的结果进行分析总结
    summary_chain = (
        PromptTemplate.from_template("这两种赏析，第一种：{paragraph_1}，第二种：{paragraph_2}，哪个更好，为什么") | llm | StrOutputParser()
    )

    # 4、构造LCEL：将前面的两个chain并行运行，然后将结果传递给summary_chain
    map_chain = {
        "paragraph_1": paragraph_1_chain,
        "paragraph_2": paragraph_2_chain,
    } | summary_chain
    
    
    poem= """
    菩提本无树，
    明镜亦非台，
    本来无一物，
    何处惹尘埃。
    """
    # 5、运行LCEL
    resp = map_chain.invoke({"poem": poem})
    print(resp)

if __name__ == "__main__":
runnable_parallel_use_lcel_demo()
```

1.6.3 其他Runnable结构

LangChain所提供的其他Runnable组件，如下表所示，此处不再详细介绍。

| **名称**                  | **描述**                                                     |
| ------------------------- | ------------------------------------------------------------ |
| **RunnableLambda**        | 将普通函数，封装成符合Runnable接口的可运行组件               |
| **RunnableBranch**        | 对输入进行if-else判断，并路由到不同的函数中                  |
| **RunnablePassthrough**   | 接收输入并将其原样输出；LCEL 体系中的“无操作节点”，用于在流水线中透传输入或保留上下文，也可以用于向输出中添加键 |
| **RunnableWithFallbacks** | 对Runnable组件进行兜底，使得 Runnable 失败后可以回退到其他 Runnable |

随着Agent的火热发展，LangChain框架的核心也从Chain这种链式结构逐渐转向支持循环迭代的Agent；构建方式，也从LCEL转成了通过LangGraph进行构建，因此对于Chain这种结构，只需要了解即可，在查看LangChain源码时，可能会发现在某些地方还会用到，能够明白其作用即可