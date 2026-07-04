# AI Financial Research Assistant

Upload a financial PDF — an annual report, 10-K, earnings release, whatever — and ask it questions in plain English instead of scrolling through 80 pages hunting for one number.

It uses Retrieval-Augmented Generation (RAG) with a locally running LLM via [Ollama](https://ollama.com), so your documents never leave your machine.

## Why I built this

Digging through long financial filings to find one specific thing — a risk factor, a revenue figure, a line of guidance — is tedious. I wanted something that indexes a document into a vector database and lets an AI answer questions using only the relevant parts of it, with page citations, so I could actually trust and verify the answer instead of taking it on faith.

## Features

- Email/password auth with JWT
- Upload PDF financial documents
- Automatic text extraction, chunking, and embedding
- Ask natural-language questions about a document
- Answers cite the page numbers they came from
- Dashboard showing upload/processing status

## Tech stack

| Layer      | Tools |
|------------|-------|
| Frontend   | React, Vite, Tailwind CSS, React Router, Axios |
| Backend    | FastAPI, SQLAlchemy, JWT auth |
| AI         | Ollama (Llama 3), Sentence-Transformers, LangChain-style RAG pipeline |
| Database   | PostgreSQL + pgvector |
| Deployment | Docker, Docker Compose |

## How it works

1. You upload a PDF.
2. The backend pulls the text out page-by-page (PyMuPDF) and splits it into overlapping chunks.
3. Each chunk gets converted into a vector embedding (Sentence-Transformers) and stored in Postgres via pgvector.
4. When you ask a question, that question gets embedded too, and the database finds the chunks closest in meaning.
5. Those chunks get stuffed into a prompt and sent to a local Llama 3 model through Ollama.
6. You get back an answer, along with the page numbers it was pulled from.

## Project structure

```
ai-financial-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app + routing
│   │   ├── config.py          # env-based settings
│   │   ├── database.py        # SQLAlchemy engine/session
│   │   ├── models.py          # User, Document, Chunk tables
│   │   ├── schemas.py         # request/response validation
│   │   ├── auth.py            # password hashing + JWT
│   │   ├── routes/            # auth, documents, chat endpoints
│   │   └── services/          # pdf parsing, embeddings, RAG pipeline
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/              # Login, Register, Dashboard, Chat
│   │   ├── components/         # Navbar, ProtectedRoute
│   │   ├── context/AuthContext.jsx
│   │   └── services/api.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Getting started

You'll need three things installed: **Python 3.11+, Node.js 18+, and Ollama**. A full Windows setup walkthrough is below if you run into environment issues along the way — I did, more than once.

Quick sanity check before you start:

```bash
python --version
node --version
npm --version
docker --version
docker ps
```

Then:

```bash
# 1. Spin up Postgres + pgvector, the backend, and the frontend
docker compose up --build

# 2. Pull and run the AI model (on your host machine, not inside Docker)
ollama pull llama3
ollama serve
```

Open `http://localhost:5173`, create an account, upload a PDF, and start asking questions.

## Try it out

A sample AI-generated financial document is included so you can test it right away without hunting one down yourself. A few questions to try:

- "What was the revenue growth year over year?"
- "What are the major business risks?"
- "What guidance was given for next fiscal year?"
- "What acquisition did the company make?"

## Windows setup walkthrough

1. Install [Python 3.11+](https://www.python.org/downloads/) (check "Add python.exe to PATH" during install), [Node.js 18+](https://nodejs.org/), [Docker Desktop](https://www.docker.com/products/docker-desktop/), and [Ollama](https://ollama.com/download).
2. Pull the model once: `ollama pull llama3`
3. Clone the repo and start everything:
git clone https://github.com/mythri-rdy/AI-Financial-Research-Assistant.git
cd AI-Financial-Research-Assistant
docker compose up --build
4. In a separate terminal, make sure Ollama is running: `ollama serve` (if it says the port is already in use, it's already running — that's fine).
5. Open `http://localhost:5173`, sign up, and upload a PDF (there's a sample in `samples/` if you don't have one handy).

## Roadmap

- [ ] Multi-document comparison
- [ ] OCR support for scanned PDFs
- [ ] Export chat history to PDF
- [ ] Financial ratio calculator

## License

MIT