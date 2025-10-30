# ai_resume_helper.py
import pandas as pd  # 其实不用，但保持一致
from openai import OpenAI
import os


# 1. 读取你的简历文本
resume_file = "resume.txt"  # ← 改成你的文件名
with open(resume_file, "r", encoding="utf-8") as f:
    resume_text = f.read()
print("简历加载成功！内容：\n", resume_text[:200])  # 只打印前200字

# 2. 调用 Kimi 修改简历
client = OpenAI(
    api_key="sk-RacZ26mhxpikuKwyX4L9Lo3AnIN6dr3SGP8VLT99uewlkP6w",  # ← 你的 key
    base_url="https://api.moonshot.cn/v1"
)

response = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {"role": "system", "content": "你是一个资深 HR 和 AI 专家。帮我改简历成 AI 数据工程师版。强调数仓经验与 RAG/LLM 的结合。添加一个项目：'基于 LLM 的数据分析工具，能自动分析订单并生成图表'。输出格式：Markdown 简历（姓名/联系/技能/经验/项目）。保持简洁、专业。"},
        {"role": "user", "content": f"""
原简历：
{resume_text}

请改成 AI 导向，突出 35 岁经验优势。
"""}
    ],
    temperature=0.3  # 让它创意点
)

ai_reply = response.choices[0].message.content
print("\n🤖 AI 改好的简历：")
print(ai_reply)

# 3. 保存新简历
with open("new_resume.md", "w", encoding="utf-8") as f:
    f.write(ai_reply)
print("✅ 新简历已保存为：new_resume.md")