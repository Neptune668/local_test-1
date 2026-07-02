# 4.5 向量存储与检索 精炼笔记

## 4.5.1 向量数据库的理解

- **传统数据库**：存储照片元数据（时间、地点等），仅支持精确查询。
- **向量数据库**：将内容（图片、文本等）编码为高维向量，存储在多维空间中，支持**相似性搜索**（模糊匹配）。
- **向量化应用**：以图搜图、视频推荐、相似商品推荐等，本质是向量间的距离/相似度计算。

## 4.5.2 常用的向量数据库

LangChain 提供统一接口，可切换多种向量库：

| 数据库        | 特点                                         |
| :------------ | :------------------------------------------- |
| FAISS         | 本地高效相似性搜索库                         |
| Chroma        | 轻量级、开源，API极简                        |
| Milvus        | 云原生，支持十亿级向量，功能强大             |
| Pgvector      | PostgreSQL 扩展，增加向量类型和相似搜索      |
| Redis         | 内存数据库，原生支持向量搜索                 |
| Elasticsearch | 分布式搜索引擎，统一管理结构/非结构/向量数据 |

## 4.5.3 Milvus 介绍和部署

### 4.5.3.1 架构

- 组件解耦：查询节点、数据节点、索引节点可独立扩缩容。0.支持数百亿级向量检索。

### 4.5.3.2 Collection 及数据类型

- **结构**：数据库 → Collection（表）→ 实体（行）。
- **Schema**：定义字段（主键、向量、标量）。
- **支持的数据类型**：
  - 向量字段：稠密向量（FLOAT_VECTOR等）、稀疏向量（SPARSE_FLOAT_VECTOR）、二进制向量。
  - 标量字段：VARCHAR, BOOL, INT, FLOAT, DOUBLE, ARRAY, JSON。
- **主键**：INT64 或 VARCHAR；可开启 AutoId 自动生成。
- **稠密向量**：通常由深度学习模型（如 Sentence-BERT）生成。
- **稀疏向量**：表示关键词及权重（如 BGE-M3 的 `lexical_weights`），适用于文本关键词匹配。

### 4.5.3.3 索引

- **稠密向量索引**：
  - **HNSW**（分层导航小世界）：基于图，高精度低延迟，内存开销大。
  - **FLAT**：暴力搜索，100%召回率。
- **稀疏向量索引**：
  - **SPARSE_INVERTED_INDEX**（倒排索引），支持相似度指标：
    - IP（内积）：`score = Σ(词权重1 × 词权重2)`
    - BM25：基于 TF-IDF 和文档长度归一化。

### 4.5.3.4 部署方式

- **Milvus Lite**：本地轻量（仅 FLAT 索引，仅 Mac/Linux）。
- **Milvus Standalone**：单机 Docker 部署（课程使用）。
- **Milvus Distributed**：Kubernetes 集群部署。
- **启动**：`docker load -i milvus_image.tar`加载镜像，执行 `standalone_embed.sh start`（Linux）或 `standalone.bat start`（Windows）。
- **客户端工具**：Attu 可视化连接。

------

## 4.5.4 Milvus 创建 Collection

### 步骤

1. **构建 Schema**（定义字段名、类型、维度、主键等）。
2. **添加索引参数**（指定字段的索引类型和度量方式）。
3. **创建 Collection**。

### 代码要点

python

```
from pymilvus import MilvusClient, DataType

client = MilvusClient(uri="http://localhost:19530")

# 1. Schema
schema = MilvusClient.create_schema(auto_id=True)
schema.add_field("id", DataType.INT64, is_primary=True)
schema.add_field("vector", DataType.FLOAT_VECTOR, dim=1024)
schema.add_field("text", DataType.VARCHAR, max_length=1500)
schema.add_field("metadata", DataType.JSON)
schema.add_field("sparse_vector", DataType.SPARSE_FLOAT_VECTOR)

# 2. 索引参数
index_params = MilvusClient.prepare_index_params()
index_params.add_index(field_name="vector", index_type="HNSW", metric_type="L2")
index_params.add_index(field_name="sparse_vector", index_type="SPARSE_INVERTED_INDEX", metric_type="IP")

# 3. 创建 Collection
client.create_collection(
    collection_name="demo_collection",
    schema=schema,
    index_params=index_params
)
```



------

## 4.5.5 Milvus 操作实体

### 4.5.5.1 插入实体

- 数据格式：`List[Dict]`，每个 Dict 对应一条记录，字段需符合 Schema。
- 使用 `BGEM3FlagModel` 同时生成稠密向量和稀疏向量。
- 示例：

python

```
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("assets/models/bge-m3")
embeddings = model.encode(texts, return_dense=True, return_sparse=True)

data_list = []
for doc, dense, sparse in zip(docs, embeddings["dense_vecs"], embeddings["lexical_weights"]):
    data_list.append({
        "vector": dense,
        "sparse_vector": sparse,
        "text": doc.page_content,
        "metadata": doc.metadata
    })

client.insert(collection_name="demo_collection", data=data_list)
```



### 4.5.5.2 删除实体

- 通过 `filter` 条件（如主键范围或其他标量字段）。

python

```
client.delete(
    collection_name="demo_collection",
    filter="id in [463480757150366907, 463480757150366908]"
)
```



------

## 4.5.6 Milvus 检索

### 4.5.6.1 向量检索

- **稠密向量检索**：使用 `client.search`，指定 `anns_field="vector"`，metric 多为 L2 或 IP。
- **稀疏向量检索**：类似，指定 `anns_field="sparse_vector"`，metric 多为 IP。
- **混合检索（Hybrid Search）**：同时使用稠密和稀疏，并通过 **Reranker**（如 RRFRanker）融合排序。
  - RRF 公式：`score = Σ 1/(k + rank_i)`，k 通常为 60。
- 示例：

python

```
from pymilvus import AnnSearchRequest, RRFRanker

dense_req = AnnSearchRequest(data=[dense_vec], anns_field="vector", param={"metric_type":"L2"}, limit=5)
sparse_req = AnnSearchRequest(data=[sparse_vec], anns_field="sparse_vector", param={"metric_type":"IP"}, limit=5)

results = client.hybrid_search(
    collection_name="demo_collection",
    reqs=[dense_req, sparse_req],
    ranker=RRFRanker(k=60),
    limit=5,
    output_fields=["id", "text", "metadata"]
)
```



### 4.5.6.2 标量检索

- 使用 `client.query`，支持 SQL-like 过滤条件，不涉及向量计算。
- 示例：

python

```
# 对 text 字段模糊搜索
client.query(collection_name, filter='text like "%大模型%"', output_fields=["id","text"], limit=5)

# 对 JSON 字段过滤
client.query(collection_name, filter='metadata["source"] like "%sample%"', output_fields=["id","metadata"])
```

**重排序**（Reranker）是指在初步检索（Recall）完成后，对候选结果进行二次排序优化的过程。其目标不是扩大召回范围，而是在已有候选集内提升排序质量和结果相关性。在典型的检索系统中，重排序通常位于向量检索或混合检索之后，用于融合多路检索结果或引入更精细的排序策略。

此处介绍RRFReranker。RRFRanker 策略的主要工作流程如下：

（1）收集搜索排名：收集来自向量搜索各路径的结果排名（rank_1、rank_2）。

（2）合并排名：根据公式转换各路径的排名（rank_rrf_1、rank_rrf_2）。

计算公式涉及 N，N 代表检索器的数量。ranki (d) 是第 i 个检索器生成的文档 d 的排名位置。k 是一个平滑参数，通常设置为 60。

（3）聚合排名：基于合并后的排名对搜索结果进行重新排序，以生成最终结果。

其示意图如下：

------

## 4.6 生成（RAG）

- 检索到相关文档后，将文档内容拼接成上下文，传递给 LLM。
- 使用 LangChain 的 `ChatOpenAI` 或其他 LLM。
- 示例：

python

```
retrieval_res = hybrid_vector_search_example_rrf(client, query)   # 返回前 k 条
context = "\n".join([item["text"] for item in retrieval_res[0]])
messages = [
    {"role": "system", "content": "你是一个专业的法律问答机器人..."},
    {"role": "user", "content": f"根据以下上下文回答问题：{context}\n问题：{query}"}
]
response = llm.invoke(messages)
print(response)
```



------

## 核心要点回顾

- **向量化**：将文本/图像转为稠密或稀疏向量。
- **索引**：HNSW（稠密）/ 倒排（稀疏）加速搜索。
- **混合检索**：结合稠密（语义）和稀疏（关键词）优势，RRF 融合排序。
- **RAG**：检索 + 生成，让 LLM 基于检索到的文档回答问题。
- **部署**：Milvus Standalone 适合开发，Docker 快速启动。