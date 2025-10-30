# ask_ai.py
import pandas as pd
from openai import OpenAI

# 1. 读取假数据
df = pd.read_csv("orders.csv")
print("数据加载成功！共", len(df), "条订单")

# 2. 把数据转成文字（大模型只能读文字）
data_text = df.to_markdown()

# 3. 调用 Kimi 大模型
client = OpenAI(
    api_key="sk-RacZ26mhxpikuKwyX4L9Lo3AnIN6dr3SGP8VLT99uewlkP6w",  # ← 把你的 key 粘贴这里！
    base_url="https://api.moonshot.cn/v1"
)

response = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {"role": "system", "content": "你是一个数据分析师，帮我分析订单数据。"},
        {"role": "user", "content": f"""数据如下：{data_text}问题：哪个用户买的东西最多？买了几次？总金额多少？"""}
    ],
    temperature=0
)

# 4. 打印 AI 回答
print("\n🤖 AI 回答：")
print(response.choices[0].message.content)
