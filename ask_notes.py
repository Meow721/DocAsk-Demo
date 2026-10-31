import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

#读资料
with open("notes.txt","r",encoding="utf-8") as f:
    notes = f.read()

#连模型
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)

#问问题
question = input("请输入问题：")

#把资料和问题一起发给模型
response = client.chat.completions.create(
    model=os.getenv("LLM_MODEL"),
    messages=[
        {
            "role":"system",
            "content":"你是问答助手。只能根据用户提供的笔记回答；笔记里没有就说不知道。",
        },
        {
            "role":"user",
            "content":"笔记内容如下：\n"+ notes +"\n\n我的问题："+ question,
        },
    ],
)

print("问题：",question)
print("回答：",response.choices[0].message.content)