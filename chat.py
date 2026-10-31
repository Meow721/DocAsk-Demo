import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)

print("开始聊天。输入 exit 结束。")

while True:
    user_text = input("你：")
    if user_text.strip().lower() == "exit":
        print("已结束。")
        break

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {"role":"system","content":"你是一个简洁的中文助手。"},
            {"role":"user","content": user_text},
        ],
    )

    print("助手:",response.choices[0].message.content)