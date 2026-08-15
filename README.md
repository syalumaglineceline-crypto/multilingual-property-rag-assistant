# Multilingual Property RAG Assistant

A multilingual Retrieval-Augmented Generation (RAG) assistant for source-grounded UK property-market information.

This project demonstrates an end-to-end applied AI workflow combining multilingual semantic retrieval, vector search, multilingual reranking, LLM-based answer generation, REST API development, and a conversational user interface.

## Project Overview

The assistant allows users to ask questions about indexed UK property-market documents.

The workflow is:

1. Source documents are loaded and split into deterministic text chunks.
2. Chunks are converted into multilingual vector embeddings.
3. Embeddings are stored in a persistent Chroma vector database.
4. A user question is embedded using the same multilingual model.
5. Semantically relevant candidate passages are retrieved.
6. A multilingual cross-encoder reranks the retrieved candidates.
7. The highest-ranked passages are supplied to an LLM using a source-grounded prompt.
8. The system generates an answer with inline source references.
9. Retrieved evidence is displayed alongside the answer for traceability.

The multilingual design allows questions written in different languages to retrieve relevant information from primarily English-language source documents.

## Current Capabilities

The current implementation includes:

- multilingual semantic retrieval
- cross-lingual retrieval from English-language source documents
- multilingual cross-encoder reranking of retrieved passages
- persistent Chroma vector storage
- deterministic document chunking
- PDF, TXT, and Markdown document ingestion
- source-grounded LLM answer generation
- inline source references
- unsupported-answer handling
- configurable retrieval depth
- FastAPI REST endpoints
- conversational Streamlit interface
- chat-session history
- retrieval-source inspection
- Responsible AI documentation
- initial automated testing

## Technology Stack

- Python
- FastAPI
- Chroma
- Sentence Transformers
- multilingual MiniLM embeddings
- multilingual CrossEncoder reranking
- OpenAI API
- Streamlit
- PyPDF
- Pydantic
- HTTPX
- pytest

## System Architecture

```text
Source Documents
       |
       v
Document Loader
       |
       v
Deterministic Chunking
       |
       v
Multilingual Embeddings
       |
       v
Chroma Vector Database
       |
       v
User Question
       |
       v
Semantic Candidate Retrieval
       |
       v
Multilingual Cross-Encoder Reranking
       |
       v
Top Retrieved Source Passages
       |
       v
Grounded LLM Prompt
       |
       v
Generated Answer + Citations
       |
       v
FastAPI / Streamlit Interface
```

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
│       ├── generator.py
│       ├── ingest.py
│       ├── reranker.py
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

### 1. Clone the repository

```bash
git clone https://github.com/syalumaglineceline-crypto/multilingual-property-rag-assistant.git
cd multilingual-property-rag-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment using the command appropriate for your operating system.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy:

```text
.env.example
```

to:

```text
.env
```

Add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5-mini
```

Never commit your real API key or `.env` file to the repository.

### 5. Add source documents

Place supported source documents inside:

```text
data/raw/
```

Supported formats include:

```text
.pdf
.txt
.md
```

Only use documents that you are permitted to store and process.

### 6. Build the vector index

Run:

```bash
python -m scripts.ingest_documents
```

This loads the source documents, creates text chunks and embeddings, and stores them in the persistent Chroma vector collection.

### 7. Start the REST API

Run:

```bash
python -m uvicorn app.api:app --reload
```

The API provides:

```text
GET  /health
GET  /stats
POST /retrieve
POST /ask
```

FastAPI interactive documentation is available through the standard `/docs` route while the API is running.

### 8. Start the Streamlit Interface

Open a second terminal and run:

```bash
streamlit run streamlit_app.py
```

The Streamlit application sends questions to the `/ask` endpoint and displays both the generated answer and the retrieved supporting passages.

## API Usage

### Retrieve Relevant Passages

`POST /retrieve`

Example request:

```json
{
  "question": "What factors affect UK house prices?",
  "top_k": 4
}
```

The endpoint performs multilingual semantic retrieval, reranks candidate passages using a multilingual cross-encoder, and returns the highest-ranked source chunks with metadata and vector-distance information.

### Generate a Grounded Answer

`POST /ask`

Example request:

```json
{
  "question": "What factors affect UK house prices?",
  "top_k": 4
}
```

The workflow is:

```text
Question
   ↓
Multilingual Embedding
   ↓
Chroma Candidate Retrieval
   ↓
Multilingual Cross-Encoder Reranking
   ↓
Top Relevant Source Passages
   ↓
Grounded LLM Generation
   ↓
Answer + Supporting Sources
```

The response contains:

- the original question
- the generated answer
- the retrieved source chunks used as supporting evidence

## Grounding Strategy

The generation layer is instructed to:

- answer using only the retrieved source passages
- avoid filling information gaps using unsupported outside knowledge
- cite retrieved passages using numbered references
- state when the available sources do not contain enough information
- respond in the same language as the user's question where possible
- avoid personalised mortgage, legal, financial, investment, or property-valuation advice

This design aims to reduce unsupported generation and make responses easier to inspect.

## Multilingual Retrieval

The project uses a multilingual Sentence Transformer embedding model so that questions written in different languages can be mapped into the same semantic vector space as the indexed documents.

A multilingual cross-encoder is then used as a second-stage reranker to improve the ordering of retrieved candidate passages.

The initial multilingual evaluation focuses on:

- English
- Hindi
- German

The purpose is to test whether non-English questions can retrieve relevant information from primarily English-language UK property sources.

For example, equivalent questions in English, Hindi, and German should ideally retrieve similar supporting passages when they express the same underlying meaning.

The multilingual capability is therefore focused on cross-lingual information retrieval rather than requiring a separate document collection for every supported language.

## Preliminary Retrieval Validation

A preliminary cross-lingual retrieval check was performed using equivalent questions in English, Hindi, and German against primarily English-language source documents.

For a test question asking for the average UK house price in May 2026, the correct ONS passage containing the £271,000 figure was initially ranked fifth by semantic retrieval.

After introducing second-stage multilingual cross-encoder reranking, the correct passage was returned at rank 2 for the equivalent English, Hindi, and German queries.

This is an initial functional check rather than a full evaluation. A larger multilingual evaluation set and formal retrieval metrics are planned.

## Responsible AI

The system is designed as an information-retrieval and question-answering demonstration rather than a professional advisory system.

Key risks considered include:

- hallucinated answers
- irrelevant retrieval
- incomplete source coverage
- multilingual performance differences
- misleading citations
- poor-quality source documents
- sensitive or private document ingestion
- inappropriate reliance on generated property or financial information

Current mitigations include:

- source-grounded prompting
- visible retrieved evidence
- unsupported-answer handling
- multilingual reranking
- restricted advisory behaviour
- documented limitations
- planned multilingual and retrieval evaluation

See:

```text
docs/responsible_ai.md
```

for the detailed risk and mitigation framework.

## Development Status

### Stage 1 — Completed

- project structure
- multilingual embedding model
- document loading
- deterministic chunking
- persistent Chroma vector database
- document ingestion pipeline
- FastAPI retrieval endpoint
- Streamlit retrieval interface
- initial multilingual retrieval questions
- Responsible AI documentation

### Stage 2 — Completed

- LLM answer-generation layer
- source-grounded generation prompt
- inline source references
- unsupported-answer handling
- same-language response instruction
- multilingual cross-encoder reranking
- second-stage retrieval refinement
- `/ask` REST endpoint
- conversational Streamlit interface
- supporting-source display

### Stage3 Future Engineering Enhancements

- expanded English, Hindi, and German evaluation dataset
- cross-lingual retrieval comparison
- retrieval Recall@K
- Mean Reciprocal Rank (MRR)
- answer-faithfulness evaluation
- citation-correctness checks
- unsupported-question testing
- latency measurements
- multilingual performance comparison
- systematic error analysis

### Stage 4 — Future Engineering Enhancements

- expanded automated test coverage
- final architecture diagram
- API examples and screenshots
- model/system card
- deployment configuration
- final UI improvements
- reproducible evaluation report

## Limitations

The current system is a portfolio prototype rather than a production property-information service.

Current limitations include:

- multilingual evaluation is still being expanded
- retrieval quality depends on the documents indexed
- retrieval performance may differ between English, Hindi, and German
- citation generation is prompt-controlled rather than independently verified
- the LLM may still produce incorrect or incomplete responses
- the application has not yet been optimised for production-scale traffic
- the system does not provide personalised professional advice

These limitations will be investigated through the planned evaluation and testing stages.

## Responsible Use

This project is intended for technical demonstration, information retrieval, and experimentation.

It should not be used as a substitute for professional:

- mortgage advice
- financial advice
- investment advice
- legal advice
- property valuation

Users should verify important information against the original source documents.
