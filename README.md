# ResearchAI - AI-Powered Research Paper Assistant

An intelligent research assistant that enables users to upload single or multiple research papers, perform semantic search across documents, and interact with them using natural language through Retrieval-Augmented Generation (RAG), session isolation, and Google's Gemini models.

## Live Demo

🚀 **Production Deployment**

**ResearchAI:**  
https://research-paper-assistant-pwd1.onrender.com/

---

## Overview

Research papers often contain dense technical information that can be difficult and time-consuming to navigate. When analyzing multiple interrelated papers, synthesizing findings across different publications becomes even more challenging.

ResearchAI simplifies this process by allowing users to upload academic papers (single or batch) and ask questions in natural language. The system retrieves the most relevant sections from across all indexed documents and generates grounded responses using Retrieval-Augmented Generation (RAG), ensuring answers remain context-aware, aligned with the source material, and backed by page-level citations.

With **Version 2.0**, ResearchAI introduces **multi-paper workspace support**, **session isolation** (preventing document leaks between browser sessions), **page-level source attribution**, and **one-click workspace resets**.

---

## Key Features

### Multi-Paper Document Intelligence (v2.0)
- **Batch PDF Ingestion**: Upload single or multiple research papers simultaneously with drag-and-drop support.
- **Per-Document Tracking**: Live catalog displaying indexed papers, individual chunk counts, and paper count badges.
- **Page-Aware Processing**: Automatic PDF text extraction with PyMuPDF preserving page numbers for citation accuracy.
- **Dynamic Session Management**: Browser-scoped workspaces (`X-Session-ID`) with isolated vector payloads ensuring zero cross-session contamination.

### Multi-Document RAG Pipeline
- **Vector Embeddings**: Dense semantic representations powered by Google Gemini embeddings.
- **Qdrant Cloud Vector Database**: Cloud vector storage with payload keyword indexing on `source`, `document_id`, and `session_id`.
- **Balanced Multi-Document Retrieval**: Searches across each indexed paper independently to guarantee multi-document coverage without drowning out smaller papers.
- **Page-Level Citations**: Every retrieved chunk retains page numbers, document names, and cosine similarity scores.

### AI-Powered Question Answering
- **Powered by Google Gemini 3.8 Flash**: Context-aware synthesis across multiple research papers.
- **Grounded & Academic Responses**: Rigorous academic guardrails instructing Gemini to cite specific papers and pages (`[paper.pdf, p. X]`) while preventing external hallucinations.
- **Follow-Up & Synthesis**: Compare methodologies, summarize findings, and analyze contrasts across papers.

### Interactive User Experience & Production Ready
- **Modern Responsive UI**: Clean dual-pane layout, dark/light theme toggle, real-time upload progress (`[1/N]`), and Markdown answer rendering.
- **One-Click Session Reset**: Purge session vectors from Qdrant and reset frontend state instantly.
- **FastAPI Backend**: Asynchronous REST API ready for cloud deployment on Render.
- **Automated Multi-Session Test Suite**: Integration test suite verifying multi-paper ingestion, session isolation, deduplication, and cross-document retrieval.

---

## System Architecture

```text
                     ┌───────────────────────────────┐
                     │ Multi-PDF Research Papers     │
                     │  (Drag & drop / Batch upload) │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │ Text & Page Metadata Extract  │
                     │         (PyMuPDF)             │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │ Page-Aware Text Chunking      │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │ Gemini Embedding Generation   │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │ Qdrant Vector Cloud           │
                     │ (Session-Isolated Payloads)   │
                     └───────┬───────────────┬───────┘
                             │               │
            Session Reset /  │               │ Balanced Multi-Document
            Isolated Storage │               │ Semantic Retrieval
                             │               ▼
                             │      ┌───────────────────────────────┐
                             │      │ Top-K Per-Document Retrieval  │
                             │      │ + Page Citation Metadata      │
                             │      └────────┬──────────────────────┘
                             │               │
                             │               ▼
                             │      ┌───────────────────────────────┐
                             │      │ Google Gemini 3.8 Flash       │
                             │      │ (Grounded Cross-Paper RAG)    │
                             │      └────────┬──────────────────────┘
                             │               │
                             ▼               ▼
                     ┌───────────────┐ ┌────────────────────────────┐
                     │ Fresh Session │ │ Synthesized Answer with    │
                     │ Clean Storage │ │ Document & Page Citations  │
                     └───────────────┘ └────────────────────────────┘
```

---

## Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** & **Uvicorn**
- **PyMuPDF (`fitz`)** for PDF page extraction
- **LangChain** text splitters

### AI & Vector Database
- **Google Gemini 3.8 Flash** (`gemini-3.8-flash`)
- **Gemini Embeddings** (`text-embedding-004`)
- **Qdrant Cloud** (Cosine Similarity with Payload Schema Filtering)

### Frontend
- **HTML5 & Vanilla CSS** (Tailored modern dark/light themes, CSS variables)
- **Modern JavaScript (ES6+)** with Session Storage & Fetch API
- **Marked.js** for Markdown rendering
- **FontAwesome** icons

### Infrastructure & Testing
- **Render** (Production Cloud Hosting)
- **Pytest** & Custom Multi-Session Automated Test Suite
- **Git** & **GitHub Releases**

---

## Project Structure

```text
research-paper-assistant/
│
├── app/
│   ├── api/
│   │   ├── main.py              # FastAPI application & endpoints
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   └── frontend.py          # Static frontend mount
│   ├── llm/
│   │   └── gemini_client.py     # Gemini client & grounded citation prompt
│   ├── rag/
│   │   ├── chunker.py           # Recursive text chunking
│   │   ├── embeddings.py        # Gemini vector embedding wrapper
│   │   ├── indexer.py           # Multi-PDF page loader, versioning & retry
│   │   ├── loader.py            # PDF text & page extraction (PyMuPDF)
│   │   ├── retriever.py         # Balanced multi-document retriever
│   │   └── vector_store.py      # Qdrant client, schema indexes & session filters
│   └── utils/
│       └── config.py            # Environment variable configurations
│
├── data/
│   └── sample_papers/           # Sample research PDFs (e.g., Attention Is All You Need)
│
├── frontend/
│   ├── index.html               # Dual-pane workspace UI with paper catalog
│   ├── script.js                # Multi-PDF upload, session manager & chat rendering
│   ├── style.css                # Responsive light/dark theme styling
│   └── design.md                # UI/UX design specifications
│
├── tests/
│   ├── test_multi_session.py    # Multi-paper & session isolation integration tests
│   ├── test_rag.py              # RAG pipeline tests
│   ├── test_retriever.py        # Retriever accuracy tests
│   └── ...                      # Additional unit tests
│
├── uploads/                     # Temporary session storage directory
├── requirements.txt             # Project dependencies
├── runtime.txt                  # Python runtime specification
├── README.md                    # Project documentation
└── .env.example                 # Environment variables template
```

---

## API Endpoints

| Method | Endpoint | Description | Headers |
|---|---|---|---|
| `POST` | `/upload` | Upload and index a PDF research paper into the active session | `X-Session-ID` (optional) |
| `POST` | `/ask` | Query across indexed papers with citation-grounded response | `X-Session-ID` (optional) |
| `GET` | `/documents` | List indexed papers and chunk counts for current session | `X-Session-ID` (optional) |
| `POST` | `/session/reset` | Clear session vectors in Qdrant and clean workspace | `X-Session-ID` |
| `GET` | `/health` | Health check endpoint | - |

---

## Workflow

### 1. Multi-Paper Upload
Users upload one or more academic PDFs via drag-and-drop or file selector. An isolated browser session ID (`X-Session-ID`) binds the uploads to the user's workspace.

### 2. Page Extraction & Chunking
PyMuPDF parses each page individually, preserving page numbers (`page_number`). Chunks are generated while retaining document and page provenance.

### 3. Vector Ingestion & Session Indexing
Embeddings are generated with exponential backoff handling rate limits. Vectors are upserted into Qdrant Cloud with payload attributes (`source`, `document_id`, `page_number`, `session_id`). Re-uploading a paper replaces previous versions without creating duplicates.

### 4. Balanced Cross-Document Retrieval
When a user asks a question, the retriever queries vectors for each indexed paper in the session, preventing dominant papers from suppressing relevant context from other documents.

### 5. Grounded Citation Generation
Retrieved chunks with explicit page markers (`[Source: paper.pdf | Page X]`) are provided to Google Gemini. Gemini synthesizes a structured answer citing exact sources and pages (`[paper.pdf, p. X]`).

### 6. Workspace Session Reset
Users can click **New Session** at any time to purge their session's vectors from Qdrant and reset the workspace to an empty state.

---

## Example Questions

```text
# Single Paper Questions
What is the core architecture introduced in this paper?
Summarize the experimental methodology and datasets used.
What are the primary limitations mentioned by the authors?

# Multi-Paper Comparative Questions
Compare the attention mechanism in Paper A with the approach in Paper B.
What are the common evaluation benchmarks used across both papers?
How do the reported accuracies compare between the two architectures?
```

---

## Installation & Local Development

### 1. Clone Repository

```bash
git clone https://github.com/AdityaSah2030/research-paper-assistant.git
cd research-paper-assistant
```

### 2. Create Virtual Environment

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

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from the example:

```env
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
```

### 5. Run Integration Tests

```bash
python -m tests.test_multi_session
```

### 6. Launch Application Locally

```bash
uvicorn app.api.main:app --reload
```

Open your browser at:
```text
http://127.0.0.1:8000
```

---

## Roadmap

### Version 1.x (Completed)
- [x] PDF Upload and text extraction
- [x] Gemini Embeddings & LLM Integration
- [x] Qdrant Cloud Vector Database setup
- [x] Single-document RAG pipeline
- [x] FastAPI REST API backend
- [x] Production Deployment on Render

### Version 2.0 (Current Release - v2.0.0)
- [x] **Multi-Paper Chat & Ingestion**: Batch drag-and-drop upload and querying across multiple papers
- [x] **Page-Level Grounded Citations**: Exact source paper and page number attribution (`[paper.pdf, p. X]`)
- [x] **Browser Session Isolation**: Independent workspaces (`X-Session-ID`) preventing multi-user data leakage
- [x] **Balanced Multi-Document Retrieval**: Per-document search preventing single-document bias
- [x] **Workspace Session Reset**: One-click session clearing for fresh research topics
- [x] **Automated Multi-Session Test Suite**: Comprehensive testing for session isolation and multi-paper RAG
- [x] **Modern UI/UX**: Dual-pane workspace, document count badges, progress indicator, and dark/light themes

### Future Enhancements (Version 2.x & Beyond)
- [ ] Research Trend & Citation Network Analysis
- [ ] Automated Knowledge Graph Generation
- [ ] User Authentication & Cloud Saved Workspaces
- [ ] Persistent Chat History & Research Notebooks
- [ ] Export Research Summaries (PDF & LaTeX formats)
- [ ] Local LLM Support (Ollama / Llama.cpp)

---

## License

This project is licensed under the MIT License.

---

## Current Release

```text
Version: v2.0.0
Status: Production Deployment Live (Multi-Paper RAG & Session Isolation)
```

---

### ⭐ If you found this project useful, consider giving it a star on GitHub!