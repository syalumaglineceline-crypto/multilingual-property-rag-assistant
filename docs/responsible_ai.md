# Responsible AI and System Risk Notes

## Intended Use

The assistant is intended as a portfolio demonstration of multilingual, source-grounded information retrieval and Retrieval-Augmented Generation for UK property-market information.

It is not intended to provide:

- financial advice
- investment advice
- mortgage advice
- legal advice
- automated property valuations
- eligibility decisions
- lending decisions

## Core Risks

### Hallucination

An LLM may generate claims that are not supported by retrieved documents.

Planned mitigation:

- answer only from retrieved context
- attach citations to factual claims
- refuse when evidence is insufficient
- evaluate answer faithfulness

### Retrieval failure

The vector search may return irrelevant or incomplete passages.

Mitigation:

- retrieval evaluation dataset
- Recall@K and MRR
- top-k sensitivity analysis
- manual error analysis
- future reranking experiment

### Multilingual quality differences

Retrieval and generation quality may vary between languages.

Mitigation:

- separate evaluation questions in English, Hindi and Malayalam
- compare retrieval performance by language
- avoid claiming equivalent quality without evidence
- preserve source text in citations

### Out-of-date information

Property-market information changes over time.

Mitigation:

- retain source metadata
- store publication/reference dates where available
- display source information with answers
- distinguish historical documents from current information

### Source quality

RAG quality depends on the documents included in the knowledge base.

Mitigation:

- prioritise official and authoritative sources
- document provenance
- avoid unattributed web text
- maintain a source manifest

### Privacy and confidential data

Mitigation:

- use public documents for the portfolio version
- do not ingest confidential employer or personal data
- do not commit secrets or API keys to GitHub
- keep `.env` excluded through `.gitignore`

## Human Oversight

Users should be able to inspect retrieved source passages and should not rely on generated answers for high-stakes decisions.

## Evaluation Before Claiming Success

The final project should report:

- retrieval Recall@K
- Mean Reciprocal Rank
- citation correctness
- answer faithfulness
- multilingual performance
- unsupported-question behaviour
- latency
- known failure cases
