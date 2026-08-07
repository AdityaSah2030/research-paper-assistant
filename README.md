# ResearchAI - AI-Powered Research Paper Assistant

An intelligent research assistant that enables users to upload research papers, perform semantic search, and interact with them using natural language through Retrieval-Augmented Generation (RAG), Agentic AI workflows, and Google's Gemini models.

## Live Demo

🚀 **Production Deployment**

**ResearchAI:**  
https://research-paper-assistant-pwd1.onrender.com/

---

## Overview

Research papers often contain dense technical information that can be difficult and time-consuming to navigate.

ResearchAI simplifies this process by allowing users to upload academic papers and ask questions in natural language. The system retrieves the most relevant sections from the document and generates grounded responses using Retrieval-Augmented Generation (RAG), ensuring answers remain context-aware and aligned with the source material.

The project combines semantic search, vector databases, and modern LLMs to create an interactive research assistant for students, researchers, and developers.

---

## Key Features

### Document Intelligence

- Upload and process PDF research papers
- Automatic text extraction and chunking
- Semantic understanding of document content
- Context-aware retrieval

### RAG Pipeline

- Vector embeddings generation
- Qdrant Cloud vector database integration
- Similarity-based document retrieval
- Grounded response generation

### AI-Powered Question Answering

- Powered by Google Gemini
- Context-aware responses
- Follow-up question support
- Reduced hallucinations through retrieval

### Production Ready

- FastAPI backend
- Cloud-hosted deployment on Render
- Qdrant Cloud integration
- Environment-based configuration

---

## System Architecture

```text
                ┌─────────────────┐
                │  Research Paper │
                │      (PDF)      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Text Extraction │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Document Chunking│
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Embeddings    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Qdrant Cloud DB │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Semantic Search │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Google Gemini   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Generated Answer│
                └─────────────────┘
```

---

## Tech Stack

### Backend

- Python
- FastAPI
- LangChain
- LangGraph

### AI & RAG

- Google Gemini
- Qdrant Cloud
- Vector Embeddings
- Retrieval-Augmented Generation (RAG)

### Infrastructure

- Render
- GitHub
- REST APIs

### Development Tools

- Jupyter Notebook
- Git
- VS Code

---

## Project Structure

```text
research-paper-assistant/
│
├── app/
│   ├── api/
│   ├── rag/
│   ├── services/
│   ├── models/
│   └── utils/
│
├── data/
├── notebooks/
│
├── requirements.txt
├── README.md
└── .env.example
```

---

## Workflow

### 1. Upload Paper

User uploads a research paper in PDF format.

### 2. Document Processing

The document is parsed, cleaned, and divided into manageable chunks.

### 3. Embedding Generation

Each chunk is converted into vector embeddings.

### 4. Vector Storage

Embeddings are stored in Qdrant Cloud.

### 5. Retrieval

Relevant chunks are retrieved using semantic similarity search.

### 6. Response Generation

Gemini receives the retrieved context and generates a grounded answer.

### 7. Conversational Interaction

Users can continue asking follow-up questions about the paper.

---

## Example Questions

```text
What is the main contribution of this paper?

Summarize the methodology used by the authors.

What datasets were used for evaluation?

What limitations are discussed?

Compare this approach with previous methods.

Explain the proposed architecture in simple terms.
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/AdityaSah2030/research-paper-assistant.git

cd research-paper-assistant
```

### Create Virtual Environment

#### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key

QDRANT_URL=your_qdrant_cloud_url

QDRANT_API_KEY=your_qdrant_api_key
```

### Run Locally

```bash
uvicorn app.api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## Roadmap

### Version 1.x

- [x] PDF Upload
- [x] Gemini Integration
- [x] Qdrant Cloud Integration
- [x] RAG Pipeline
- [x] FastAPI Deployment
- [x] Public Production Deployment

### Version 2.0

- [ ] Multi-Paper Chat
- [ ] Citation-Aware Responses
- [ ] Research Trend Analysis
- [ ] Knowledge Graph Generation
- [ ] User Authentication
- [ ] Chat History
- [ ] Research Report Generation

### Future Enhancements

- Local LLM Support (Ollama)
- Multi-Agent Research Workflows
- Research Assistant Dashboard
- Collaborative Research Spaces

---


## License

This project is licensed under the MIT License.

---

## Current Release

```text
Version: v1.0.0
Status: Production Deployment Live
```

---

### ⭐ If you found this project useful, consider giving it a star on GitHub.