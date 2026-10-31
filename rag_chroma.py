import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions


load_dotenv()

#按行切分
with open("notes.txt","r",encoding="utf-8") as f:
    text = f.read()

chunk = [line.strip() for line in text.splitlines() if line.strip()]

#准备Embedding(把文字变成向量)
embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

#创建/打开Chroma，写入段落
client_db = chromadb.PersistentClient(path="./chroma_db")

try:
    client_db.delete_collection("notes")
except Exception:
    pass

collection = client_db.create_collection(
    name="notes",
    embedding_function=embedder,
)

ids = [f"line-{i}" for i in range(len(chunk))]
collection.add(documents=chunk, ids=ids)

#提问并用向量检索
question = input("请输入问题：")
result = collection.query(
    query_texts=[question],
    n_results=2,
)

selected = result["documents"][0]

print("检索到的资料：")
for i,c in enumerate(selected,start=1):
    print("--- 资料", i,"---")
    print(c)

#交给deepseek
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)
context = "\n".join(selected)

response = client.chat.completions.create(
    model=os.getenv("LLM_MODEL"),
    messages=[
        {
            "role": "system","content": "你是问答助手。只能根据资料回答；资料不足就说不知道。",
        },
        {
            "role": "user","content": "资料：\n"+ context + "\n\n问题："+ question,
        },
    ],
)
print("回答：",response.choices[0].message.content)