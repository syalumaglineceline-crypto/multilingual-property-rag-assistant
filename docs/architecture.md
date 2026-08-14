# Architecture

## Current Stage

```mermaid
flowchart LR
    A[PDF / TXT / Markdown Sources] --> B[Document Loader]
    B --> C[Deterministic Chunking]
    C --> D[Multilingual Sentence Transformer]
    D --> E[(Chroma Vector Store)]
    Q[User Question] --> F[FastAPI]
    F --> G[Query Embedding]
    G --> E
    E --> H[Top-K Source Chunks]
    H --> F
    F --> U[Streamlit UI]
```

## Planned RAG Stage

```mermaid
flowchart LR
    Q[Multilingual Question] --> R[Retriever]
    R --> V[(Chroma)]
    V --> C[Relevant Context]
    C --> P[Grounded Prompt]
    Q --> P
    P --> L[LLM]
    L --> A[Answer in User Language]
    C --> S[Source Citations]
    S --> A
```

## Design Decisions

### Local multilingual embeddings

Embeddings are produced locally using a multilingual Sentence Transformer.

### Persistent vector storage

Chroma is configured as a persistent local vector store so embeddings survive application restarts.

### Explicit API boundary

Retrieval is exposed through FastAPI rather than being embedded only inside the UI.

### Separate UI

Streamlit acts as a client of the REST API.

### Source metadata

Each indexed chunk stores its original filename and chunk index so retrieved evidence can be traced back to its source.
