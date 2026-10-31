#关键词检索

#读笔记全文
with open("notes.txt","r",encoding="utf-8") as f:
    text = f.read()
#切成小段
chunk_size = 30
chunks = []
for i in range(0,len(text),chunk_size):
    chunks.append(text[i:i+chunk_size])
#你输入的问题
question = input("请输入问题：")
#给每一段打分：问题里的字出现的越多，分越高
scored = []

for idx,chunk in enumerate(chunks):
    score = 0
    for ch in question:
        if ch.strip() == "":
            continue
        if ch in chunk:
            score += 1
    scored.append((score,idx,chunk))
#按分数从高到低排
scored_sorted = sorted(scored,key=lambda x: x[0],reverse=True)
#打印得分最高的前2段
top_k=2
print("问题：",question)
print("最相关的段落：")
found = 0
for score,idx,chunk in scored_sorted:
    if score <= 0:
        continue
    print("---第",idx + 1,"段 | 得分",score,"---")
    print(chunk)
    found += 1
    if found >= top_k:
        break
if found == 0:
    print("没有找到明显相关的段落。")