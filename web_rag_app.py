# web_rag_app.py
import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import os


# === 1. 初始化（只运行一次）===
@st.cache_resource
def init_rag():
    # Chroma + 中文嵌入
    client = chromadb.PersistentClient(path="chroma_db")
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="shibing624/text2vec-base-chinese"
    )
    collection = client.get_or_create_collection("my_knowledge", embedding_function=embedding_func)

    # 加载知识库
    with open("knowledge_base.txt", "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
    if collection.count() == 0:
        collection.add(documents=lines, ids=[f"id{i}" for i in range(len(lines))])

    # Kimi
    kimi = OpenAI(api_key="sk-w7xxxxxxNC2s", base_url="https://api.moonshot.cn/v1")
    return collection, kimi


collection, kimi = init_rag()


# === 2. RAG 查询函数 ===
def rag_query(question):
    results = collection.query(query_texts=[question], n_results=3)
    context = "\n".join(results['documents'][0])

    prompt = f"知识：{context}\n问题：{question}\n请简洁回答。"
    response = kimi.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[{"role": "system", "content": "你只用知识回答。"}, {"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


# === 3. Streamlit 页面 ===
st.set_page_config(page_title="AI 工程师 - RAG 助手", page_icon="🤖")
st.title("🤖 我的 AI 数据分析助手")
st.markdown("**35岁数仓老兵 → AI 工程师转型实战项目**")

# 侧边栏说明
with st.sidebar:
    st.header("项目能力")
    st.write("✔ 向量检索（Chroma）")
    st.write("✔ 中文 RAG")
    st.write("✔ 自动出图 + 简历改写")
    st.write("✔ Web 部署")
    st.markdown("[🌟 GitHub 项目](https://github.com/eninem123/llm-data-analyzer)")

# 聊天界面
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("问我简历、项目、数据分析..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            answer = rag_query(prompt)
        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})