# ask_ai_with_chart.py
import pandas as pd
from openai import OpenAI
import matplotlib.pyplot as plt
import os
# matplotlib乱码
# 找到 matplotlib 的配置文件 matplotlibrc（可通过 import matplotlib; print(matplotlib.matplotlib_fname()) 查看路径），修改以下内容：
# import matplotlib
# print(matplotlib.matplotlib_fname())  # 输出配置文件路径，如：
# # Windows: C:\Users\用户名\AppData\Local\Programs\Python\Python3x\Lib\site-packages\matplotlib\mpl-data\matplotlibrc
# # macOS/Linux: /usr/local/lib/python3.x/site-packages/matplotlib/mpl-data/matplotlibrc
# 用文本编辑器打开 matplotlibrc，找到以下配置并修改（去掉行首的 # 注释）：
# # 字体设置：添加中文字体到优先列表
# font.family         : sans-serif
# font.sans-serif     : SimHei, WenQuanYi Micro Hei, Heiti TC, Microsoft YaHei, DejaVu Sans

# 解决负号显示问题
# axes.unicode_minus  : False
# 1. 读取数据
df = pd.read_csv("orders.csv")
print("数据加载成功！共", len(df), "条订单")

# 2. 手动转 Markdown（零依赖）
data_text = "| " + " | ".join(df.columns) + " |\n"
data_text += "| " + " --- |" * len(df.columns) + "\n"
for _, row in df.iterrows():
    data_text += "| " + " | ".join(str(x) for x in row) + " |\n"

# 3. 调用 Kimi 分析
client = OpenAI(
    api_key="sk-RacZ26mhxpikuKwyX4L9Lo3AnIN6dr3SGP8VLT99uewlkP6w",  # ← 你的 key
    base_url="https://api.moonshot.cn/v1"
)
print(data_text)
response = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {"role": "system", "content": "你是一个数据分析师。回答要简洁，只说结论。"},
        {"role": "user", "content": f"""
数据如下：
{data_text}

问题：哪个用户总金额最高？金额是多少？请用 Python 代码画一个柱状图，x轴是用户，y轴是总金额。
代码要完整、可直接运行，用 matplotlib，保存为 chart.png。
"""}
    ],
    temperature=0
)

ai_reply = response.choices[0].message.content
print("\n🤖 AI 回答：")
print(ai_reply)

# 4. 提取 AI 给的 Python 代码（假设它在 ```python ``` 代码块中）
import re

code_match = re.search(r"```python(.*?)```", ai_reply, re.DOTALL)
if code_match:
    code = code_match.group(1).strip()
    print("\n🎨 正在运行 AI 生成的画图代码...")

    # 安全执行代码（只运行画图）
    exec(code)

    print("✅ 图表已保存为：chart.png（在当前文件夹）")
else:
    print("❌ AI 没返回画图代码，手动补一张...")
    # 手动画图保底
    user_spend = df.groupby("用户")["金额"].sum()
    user_spend.plot(kind='bar', title="用户总消费")
    plt.ylabel("金额")
    plt.savefig("chart.png")
    plt.show()
