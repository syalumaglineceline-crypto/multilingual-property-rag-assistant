# Multilingual Property RAG Assistant

A multilingual retrieval-augmented assistant for source-grounded UK property-market information.

This project is being built as a portfolio system demonstrating:

- Python application development
- multilingual semantic search
- vector databases
- Retrieval-Augmented Generation (RAG)
- REST API development with FastAPI
- user interface development with Streamlit
- source citation and traceability
- evaluation and responsible AI practices

## Current Stage

This first stage implements the project foundation and a working **multilingual retrieval API**.

The next stage will add the LLM generation layer so the system can produce grounded answers from the retrieved sources.

## Technology Stack

- Python
- FastAPI
- Chroma
- Sentence Transformers
- multilingual MiniLM embeddings
- Streamlit
- PyPDF
- pytest

## Repository Structure

```text
multilingual-property-rag-assistant/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── schemas.py
│   └── rag/
│       ├── __init__.py
│       ├── chunking.py
│       ├── document_loader.py
│       ├── embeddings.py
│       ├── ingest.py
│       ├── service.py
│       └── vector_store.py
├── scripts/
│   └── ingest_documents.py
├── data/
│   └── raw/
│       └── .gitkeep
├── docs/
│   ├── architecture.md
│   └── responsible_ai.md
├── evaluation/
│   └── retrieval_questions.jsonl
├── tests/
│   └── test_chunking.py
└── streamlit_app.py
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env`.

The first retrieval stage does not require a paid LLM API key.

### 4. Add source documents

Place `.pdf`, `.txt`, or `.md` files inside:

```text
data/raw/
```

Only use documents that you are permitted to store and process.

### 5. Build the vector index

```bash
python scripts/ingest_documents.py
```

### 6. Start the REST API

```bash
uvicorn app.api:app --reload
```

FastAPI exposes:

```text
GET  /health
GET  /stats
POST /retrieve
```

### 7. Start the Streamlit interface

In a second terminal:

```bash
streamlit run streamlit_app.py
```

## Example Retrieval Request

```json
{
  "question": "What factors affect UK house prices?",
  "top_k": 4
}
```

The API returns semantically relevant source chunks and metadata.

## Development Roadmap

### Stage 1

- project structure
- multilingual embedding model
- document loading
- deterministic chunking
- persistent Chroma vector database
- document ingestion pipeline
- FastAPI retrieval endpoints
- Streamlit retrieval UI
- initial multilingual retrieval questions
- Responsible AI documentation

### Stage 2

- LLM answer generation
- strict source-grounded prompt
- inline citations
- unsupported-answer refusal
- same-language response behaviour
- `/ask` REST endpoint

### Stage 3

- multilingual evaluation set
- retrieval Recall@K / MRR
- answer faithfulness checks
- citation correctness
- latency measurements
- error analysis

### Stage 4

- final UI polish
- architecture diagram
- API examples
- screenshots
- model/system card
- deployment documentation

## Responsible Use

This project is an information-retrieval and question-answering demonstration. It should not be used to provide mortgage, legal, financial, property-valuation, or investment advice.

See `docs/responsible_ai.md` for the current risk and mitigation framework.
