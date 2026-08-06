# Research Paper Assistant using RAG & Agentic AI

An intelligent research assistant that enables users to upload research papers, perform semantic search, and obtain context-aware answers using Retrieval-Augmented Generation (RAG) and Agentic AI workflows.

## Overview

Research papers often contain large amounts of technical information that can be difficult to navigate efficiently. This project provides an AI-powered assistant that helps users interact with research papers through natural language conversations.

The system processes uploaded PDF documents, creates vector embeddings, retrieves relevant context, and generates grounded responses using Large Language Models (LLMs).

## Features

- Upload and process research papers in PDF format
- Semantic search using vector embeddings
- Retrieval-Augmented Generation (RAG)
- Context-aware question answering
- Conversational memory for follow-up queries
- FastAPI backend for scalable deployment
- Support for Gemini API
- Planned support for local LLMs via Ollama

## System Architecture

```text
PDF Upload
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embeddings
    ↓
Qdrant Vector Database
    ↓
Retriever
    ↓
LLM (Gemini / Ollama)
    ↓
Generated Response
```

## Tech Stack

### Backend

- Python
- FastAPI
- LangChain
- LangGraph

### AI & RAG

- Google Gemini
- Qdrant
- Embedding Models
- Retrieval-Augmented Generation (RAG)

### Tools

- Git
- Jupyter Notebook

## Project Structure

```text
research-paper-assistant/
│
├── backend/
│   ├── api/
│   ├── rag/
│   ├── database/
│   └── utils/
│
├── frontend/
│
├── docs/
│
├── screenshots/
│
├── requirements.txt
├── README.md
└── .env.example
```

## Workflow

1. Upload a research paper in PDF format.
2. Extract and preprocess document content.
3. Generate vector embeddings.
4. Store embeddings in Qdrant.
5. Retrieve relevant chunks using semantic search.
6. Generate context-aware responses using Gemini.
7. Maintain conversational context for follow-up questions.

## Example Questions

- What is the main contribution of this paper?
- Summarize the methodology used by the authors.
- What datasets were used for evaluation?
- What are the limitations mentioned in the paper?
- Compare the proposed approach with previous methods.

## Future Improvements

- Multi-paper comparison
- Citation extraction
- Research trend analysis
- Knowledge graph generation
- Local model support using Ollama
- Interactive web interface
- Research paper summarization reports

## Installation

```bash
git clone https://github.com/your-username/research-paper-assistant.git

cd research-paper-assistant

pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

## Status

🚧 Currently under active development.

