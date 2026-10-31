#练习 把长文本切成小段

with open("notes.txt","r",encoding="utf-8") as f:
    text = f.read()

chunk_size = 20
chunks = []

for i in range(0,len(text),chunk_size):
    piece = text[i : i + chunk_size]
    chunks.append(piece)

print("一共切成",len(chunks),"段")

for idx,c in enumerate(chunks,start=1):
    print("---第",idx,"段---")
    print(c)