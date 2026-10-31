# DocAsk

基于 RAG 的本地文档问答：读取文本笔记，经切分与向量检索后，由大模型根据检索到的片段生成回答，并提供 Streamlit 网页界面。

## 功能

- 读取 `notes.txt`，按行切分后写入向量库
- 使用 Embedding + Chroma 做语义检索（Top-K）
- 将检索结果注入提示词，调用 DeepSeek（OpenAI 兼容 API）生成回答
- Streamlit 页面展示问题、检索片段与最终回答

## 技术栈

- Python 3
- OpenAI Python SDK（对接 DeepSeek）
- ChromaDB + Sentence Transformers
- Streamlit
- python-dotenv

## 快速开始

### 1. 环境

```powershell
cd DocAsk
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

若尚无 `requirements.txt`，可先安装：

```powershell
pip install openai python-dotenv chromadb streamlit sentence-transformers
```

### 2. 配置

在项目根目录创建 `.env`（该文件已被 `.gitignore` 忽略，请勿提交）：

```env
LLM_API_KEY=你的密钥
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

按需编辑 `notes.txt` 作为知识库文本。

### 3. 运行

网页版：

```powershell
streamlit run app.py
```

命令行版：

```powershell
python rag_chroma.py
```

国内下载 Embedding 模型如遇超时，可设置：

```powershell
$env:HF_ENDPOINT="https://hf-mirror.com"
```

## 目录说明

| 文件 | 说明 |
|------|------|
| `app.py` | Streamlit 网页入口 |
| `rag_chroma.py` | 命令行向量 RAG |
| `rag_mini.py` | 关键词检索 + LLM 的简易 RAG |
| `retrieve_demo.py` | 关键词 Top-K 检索演示 |
| `chunk_demo.py` | 文本切分演示 |
| `ask_notes.py` | 全文塞入提示词问答 |
| `chat.py` | 纯 LLM 对话 |
| `notes.txt` | 本地知识库文本 |
| `chroma_db/` | Chroma 持久化目录（本地生成，不入库） |

## 说明

- 首次提问可能较慢（需加载 Embedding 模型；当前实现每次会重建集合）
- 请避免连续快速点击「提问」，以免向量库状态异常
- 知识库短句若缺少主语，模型可能把不同条目的信息错误归并；建议笔记中写清主语
- 请妥善保管 API Key，不要将 `.env` 推送到远程仓库
