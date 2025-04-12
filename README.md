# 🚀 Multilingual Health RAG System (HackerzStreet 2025)

## 👨‍💻 Authors
- **Ansh Agrawal, Ekaansh, Devansh,Arnav**
- 📅 Date: **13/4/2025**



## 📝 Introduction
This project presents a fully **open-source**, **cloud-agnostic** multilingual **Retrieval-Augmented Generation (RAG)** system for **insurance documentation**. Designed to support **multiple Indian languages**, the system enables both **text and voice-based interactions** while ensuring **privacy-friendly, cost-effective deployment** without reliance on proprietary cloud platforms.

By integrating **open-source LLMs (LLaMA)** and leveraging **FastAPI, FastText, Deep Translate**, the system delivers **context-aware responses with enhanced accuracy**.

This chatbot not only facilitates **real-time translation** and **multilingual conversations**, but also supports essential **transactional services** such as **policy inquiries** and **service requests**, making it a practical and scalable solution for the insurance sector. 🏦💬

### 🌟 Key Features
- 🌍 **Multilingual support** for **9 Indian languages**
- 🎙️ **Voice and text input processing**
- 📄 **PDF document processing** and embedding generation
- 🧠 **Context-aware responses using RAG**
- 🔄 **Real-time translation**

### 🛠️ Tech Stack
- 🚀 **FastAPI** for backend
- 🏷️ **FastText** for embeddings
- 🌐 **Deep Translate** for language translation
- 🦙 **LLaMA 3 (via Ollama)** for response generation
- ⚛️ **React** for frontend

## ⚙️ Installation & Setup

### 📌 Prerequisites
- 🐍 **Python 3.13+**
- 📂 **FastText pre-trained model (cc.en.300.bin)**
- 💻 **Node.js and npm for frontend**
- 🦙 **Ollama installed and running**

### 📥 Installation Steps
1️⃣ Clone the repository:
```bash
git clone https://github.com/AnshAggr1303/HackerzStreet-25.git
cd HackerzStreet-25
```

2️⃣ Create and activate virtual environment:
```bash
python -m venv rag_env
source rag_env/bin/activate  # On Windows: rag_env\Scripts\activate
```

3️⃣ Install dependencies:
```bash
cd backend
pip install -r requirements
```

## 🚀 Usage Guide

### 🦙 Running the Ollama server (open-source LLM)
📥 Download Ollama from [Ollama Official Site](https://ollama.com/download)

Run the following commands in terminal:
```bash
ollama serve
ollama run llama3
```
To stop the server:
```bash
ollama stop llama3
```

### 🦙 Downloading the embeddings model (Fasttext by Facebook Research)
Run the following commands in terminal in the backend/app/models folder:
```bash
wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz
gunzip cc.en.300.bin.gz
```


### ▶️ Running the Project (after creating your environment)

1️⃣ Start the FastAPI server:
```bash
cd backend
uvicorn app.main:app --reload
```

2️⃣ Start the frontend server:
```bash
cd frontend
npm i
npm run dev
```

## 🏛️ Architecture Overview

### 📂 Directory Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embedding_service.py
│   │   ├── translation_service.py
│   │   ├── rag_service.py
│   │   ├── llm_service.py
│   │   └── speech_service.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── embeddings_output/
└── models/
```

### 🔑 Core Components
📄 **Embedding Service** : Processes PDFs and generates FastText embeddings  
🔍 **RAG Service** : Handles context retrieval and query processing  
🌎 **Translation Service** : Manages language detection and translation  
🎤 **Speech Service** : Handles voice input/output processing  
🧠 **LLM Service** : Interfaces with LLaMA for response generation  

## 📡 API Documentation

### 🔌 Endpoints

#### 📤 `POST /api/upload`
Handles **voice input processing** 🎤
```json
Request:
- FormData with 'file' field (audio/mpeg)

Response:
{
    "audio_content": bytes,
    "detected_language": string
}
```

#### 💬 `POST /api/query`
Handles **text input processing** 📝
```json
Request:
{
    "prompt": string
}

Response:
{
    "response": string,
    "detected_language": string
}
```

### 📚 References
- 📘 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 📗 [FastText Documentation](https://fasttext.cc/)
- 🦙 [LLaMA Documentation](https://github.com/facebookresearch/llama)
