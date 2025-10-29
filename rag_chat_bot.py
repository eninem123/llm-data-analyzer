# rag_chat_bot.py
import pandas as pd
from openai import OpenAI
import os

# 1. 加载知识库（简历 + 数据）
resume_file = "new_resume.md"
with open(resume_file, "r", encoding="utf-8") as f:
    resume_text = f.read()

df = pd.read_csv("orders.csv")
data_text = "| " + " | ".join(df.columns) + " |\n"
data_text += "| " + " --- |" * len(df.columns) + "\n"
for _, row in df.iterrows():
    data_text += "| " + " | ".join(str(x) for x in row) + " |\n"

knowledge = f"简历：\n{resume_text}\n\n订单数据：\n{data_text}\n\n额外知识：我35岁，失业2年，转AI。"

print("✅ 知识库加载成功！（简历 + 数据）")

# 2. 初始化 Kimi
client = OpenAI(
    api_key="sk-xxxxx",  # ← 你的 key
    base_url="https://api.moonshot.cn/v1"
)

# 3. 聊天循环（RAG 风格：检索知识 + 生成）
print("\n🤖 欢迎使用 RAG 聊天机器人！输入 'exit' 退出。")
while True:
    user_input = input("\n你问： ")
    if user_input.lower() == 'exit':
        break

    # RAG：简单检索（实际中用向量，这里先用全知识）
    prompt = f"""
知识库：{knowledge}

用户问题：{user_input}

基于知识库回答。如果问题是关于简历的，强调 AI 经验；如果是数据，分析订单。
如果无关，说“我只懂简历和订单”。
"""

    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": "你是一个 RAG 助手，只用知识库回答。简洁、专业。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    print("🤖 AI 答：", response.choices[0].message.content)