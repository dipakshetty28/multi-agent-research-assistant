# Multi-Agent Research Assistant

Production-style starter repo for a **multi-agent research platform** built with **LangGraph**, **FastAPI**, **Chroma vector DB**, and a **React + Vite UI**.

It supports:
- document ingestion into a vector store
- retrieval-augmented generation (RAG)
- a structured research pipeline with **researcher -> writer -> editor** agents
- response caching for repeated report requests
- clean API boundaries and modular services
- Docker and CI workflows

## Architecture

```text
Frontend (React/Vite)
    |
    v
FastAPI API
    |
    +--> LangGraph workflow
    |      researcher -> writer -> editor
    |
    +--> Retrieval service
    |      chunking -> embeddings -> Chroma -> similarity search
    |
    +--> LLM service
    |      OpenAI-compatible chat/embeddings
    |
    +--> Cache service
           request fingerprint -> cached report
```

## Tech Stack

- Python 3.11
- FastAPI
- LangGraph
- ChromaDB
- React + TypeScript + Vite
- Docker / Docker Compose
- GitHub Actions

## Repo Structure

```text
multi-agent-research-assistant/
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  ├─ core/
│  │  ├─ graphs/
│  │  ├─ models/
│  │  ├─ services/
│  │  └─ main.py
│  ├─ tests/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  └─ .env.example
├─ frontend/
│  ├─ src/
│  │  ├─ components/
│  │  ├─ lib/
│  │  ├─ pages/
│  │  ├─ App.tsx
│  │  └─ main.tsx
│  ├─ Dockerfile
│  ├─ package.json
│  ├─ tsconfig.json
│  ├─ vite.config.ts
│  └─ .env.example
├─ docker-compose.yml
└─ .github/workflows/
```

## Environment Variables

### Backend
Copy `backend/.env.example` to `backend/.env`.

Important values:
- `OPENAI_API_KEY`
- `OPENAI_CHAT_MODEL`
- `OPENAI_EMBEDDING_MODEL`
- `CHROMA_PERSIST_DIRECTORY`
- `ALLOWED_ORIGINS`

### Frontend
Copy `frontend/.env.example` to `frontend/.env`.

- `VITE_API_BASE_URL=http://localhost:8000`

## Run Locally

### 1. Start with Docker

```bash
docker compose up --build
```

Frontend:
- http://localhost:5173

Backend:
- http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### 2. Manual backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Manual frontend setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev -- --host 0.0.0.0 --port 5173
```

## API Overview

### Health
```http
GET /api/v1/health
```

### Ingest documents
```http
POST /api/v1/knowledge/ingest
Content-Type: application/json

{
  "documents": [
    {
      "id": "doc-1",
      "title": "Example Research Note",
      "text": "Long source text here...",
      "metadata": {
        "source": "manual"
      }
    }
  ]
}
```

### Generate report
```http
POST /api/v1/reports/generate
Content-Type: application/json

{
  "query": "Analyze the AI coding assistant market for mid-size B2B teams.",
  "use_cache": true,
  "top_k": 6
}
```

## LangGraph Flow

The workflow is intentionally simple and production-friendly:

1. **researcher**
   - retrieves relevant context from Chroma
   - builds evidence notes and key findings
2. **writer**
   - converts findings into a structured report draft
3. **editor**
   - improves clarity, consistency, actionability, and final format

