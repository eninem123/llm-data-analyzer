# rag_vector_db.py
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import os

# 1. 初始化 Chroma + 嵌入模型（中文）
client = chromadb.PersistentClient(path="chroma_db")  # 保存到本地
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="shibing624/text2vec-base-chinese"  # 中文神器
)
collection = client.get_or_create_collection(
    name="my_knowledge",
    embedding_function=embedding_func
)

# 2. 加载知识库并向量化
print("🔄 正在加载知识库并向量化...")
with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]

documents = lines
ids = [f"id{i}" for i in range(len(documents))]

# 存入向量数据库（自动去重）
collection.add(documents=documents, ids=ids)
print(f"✅ 知识库加载完成！共 {len(documents)} 条")

# 3. 初始化 Kimi
kimi_client = OpenAI(
    api_key="sk-xxxxs",  # ← 你的 key
    base_url="https://api.moonshot.cn/v1"
)


# 4. 向量检索 + 生成（RAG 核心）
def ask_question(question):
    # 步骤1：向量检索 Top-3 相关内容
    results = collection.query(query_texts=[question], n_results=3)
    context = "\n".join(results['documents'][0])

    # 步骤2：构造 RAG Prompt
    prompt = f"""
相关知识：
{context}

问题：{question}
请基于以上知识回答，简洁专业。如果不知道，说“无法回答”。
"""

    # 步骤3：调用大模型
    response = kimi_client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": "你是一个精准的 RAG 助手，只用检索到的知识回答。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content


# 5. 聊天循环
print("\n🤖 进阶 RAG 机器人启动！（向量数据库版）输入 'exit' 退出。")
while True:
    q = input("\n你问： ")
    if q.lower() == 'exit':
        break
    answer = ask_question(q)
    print("🤖 AI 答：", answer)