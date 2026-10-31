import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

#读文件并切分
with open("notes.txt","r",encoding="utf-8") as f:
    text = f.read()

#chunk_size = 30
#chunks = []
#for i in range(0,len(text),chunk_size):
#    chunks.append(text[i : i + chunk_size])
chunks = [line.strip() for line in text.splitlines() if line.strip()]
#提问
question = input("请输入问题：")

#关键词打分检索
scored = []
for idx,chunk in enumerate(chunks):
    score = 0
    for ch in question:
        if ch.strip() == "":
            continue
        if ch in chunk:
            score += 1
    scored.append((score,idx,chunk))

scored_sorted = sorted(scored, key=lambda x: x[0],reverse=True)

#支取分数足够高的段，避免了废字刷分
min_score = 3
top_k = 2
selected = []
for score,idx,chunk in scored_sorted:
    if score < min_score:
        continue
    selected.append(chunk)
    if len(selected) >= top_k:
        break

print("检索到",len(selected),"段：")
for i,c in enumerate(selected,start=1):
    print("---资料",i,"---")
    print(c)

#把资料交给模型
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)
if len(selected) == 0:
    context = "(没有检索到相关资料)"
else:
    context = "\n".join(selected)

response = client.chat.completions.create(
    model=os.getenv("LLM_MODEL"),
    messages=[
        {
            "role":"system","content":"你是问答助手。只能根据「资料」回答；资料不足就说不知道，不要编造。"
        },
        {
            "role":"user","content":"资料：\n"+context+"\n\n问题："+question,
        },
    ],
)

print("回答：",response.choices[0].message.content)