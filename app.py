import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
import streamlit as st

load_dotenv()

st.title("DocAsk 本地文档问答")
question = st.text_input("请输入问题")

if st.button("提问") and question.strip():
    with open("notes.txt","r",encoding="utf-8") as f:
        text = f.read()

    chunk = [line.strip() for line in text.splitlines() if line.strip()]
    #文字 → 向量
    embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    client_db  = chromadb.PersistentClient(path="./chroma_db")

    try:
        client_db.delete_collection("notes")
    except Exception:
        pass

    collection = client_db.create_collection(
        name="notes",
        embedding_function=embedder,#????
    )

    ids = [f"line-{i}" for i in range(len(chunk))]
    collection.add(documents=chunk,ids=ids)

    result = collection.query(
        query_texts=[question],
        n_results=2,
    )
    selected = result["documents"][0]

    st.subheader("检索到的资料")
    for i,c in enumerate(selected,start=1):
        st.write(f"--资料 {i}--")
        st.write(c)

    client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
    )
    context = "\n".join(selected)

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {
                "role":"system",
                "content":"你是问答助手。只能根据资料回答；资料不足就说不知道。",
            },
            {
                "role": "user",
                "content": "资料：\n" + context + "\n\n问题：" + question,
            },
        ],
    )

    st.subheader("回答")
    st.write(response.choices[0].message.content)