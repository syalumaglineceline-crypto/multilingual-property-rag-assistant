# Responsible AI and System Risk Notes

## Intended Use

The assistant is intended as a portfolio demonstration of multilingual, source-grounded information retrieval and Retrieval-Augmented Generation (RAG) for UK property-market information.

It is designed to retrieve information from indexed source documents and generate answers grounded in the retrieved evidence.

It is not intended to provide:

* financial advice
* investment advice
* mortgage advice
* legal advice
* automated property valuations
* eligibility decisions
* lending decisions

## Core Risks

### Hallucination

An LLM may generate claims that are not fully supported by the retrieved documents.

Current mitigations:

* instruct the LLM to answer only from retrieved context
* require numbered source references for factual claims
* return retrieved source passages alongside the generated answer
* instruct the model to state when available evidence is insufficient
* restrict personalised financial, mortgage, legal, investment, and property-valuation advice

Further evaluation of answer faithfulness and citation correctness would be required before production use.

### Retrieval Failure

Semantic vector search may retrieve passages that are relevant to the general topic but do not contain the most precise evidence required to answer a question.

Current mitigations:

* retrieve a wider candidate set from Chroma
* apply second-stage multilingual cross-encoder reranking
* return multiple supporting passages rather than relying on a single retrieved chunk
* expose retrieved evidence for user inspection
* perform manual retrieval checks during development

During preliminary testing, the correct passage for a UK house-price question was initially ranked fifth by semantic retrieval. After introducing multilingual cross-encoder reranking, the correct passage was returned at rank 2 for equivalent English, Hindi, and German questions.

This represents an initial functional check rather than a comprehensive benchmark.

### Multilingual Quality Differences

Retrieval and answer-generation quality may vary between languages.

The initial multilingual testing focuses on:

* English
* Hindi
* German

Current mitigations:

* use a multilingual Sentence Transformer for semantic retrieval
* use a multilingual cross-encoder for second-stage reranking
* test equivalent questions across the selected languages
* preserve original source passages for inspection
* avoid claiming equivalent multilingual performance without broader evaluation

The current multilingual functionality is primarily intended to demonstrate cross-lingual retrieval from predominantly English-language source documents.

### Unsupported Questions

A user may ask a question for which the indexed documents contain insufficient information.

Current mitigations:

* instruct the generation layer not to fill gaps using unsupported outside knowledge
* return an insufficient-evidence response when appropriate
* expose supporting retrieved passages so the user can inspect the evidence

The effectiveness of this behaviour should be evaluated across a larger unsupported-question test set before production deployment.

### Out-of-Date Information

Property-market information changes over time, meaning answers may become outdated even when they are accurately grounded in the indexed documents.

Current mitigations:

* retain source filenames and metadata
* preserve publication and reference information contained in source documents
* display supporting source passages with generated answers
* use authoritative documents with identifiable publication dates

Users should verify time-sensitive information against the latest official sources.

### Source Quality

RAG output quality depends directly on the quality and coverage of the documents included in the knowledge base.

Current mitigations:

* prioritise official and authoritative sources
* use identifiable source documents
* retain document provenance through source metadata
* avoid unattributed web content
* allow users to inspect retrieved evidence

The current portfolio knowledge base uses public UK property-market material from authoritative sources.

### Citation Reliability

Generated citation numbers may appear plausible even when a cited passage does not fully support a claim.

Current mitigations:

* restrict citations to passages actually supplied to the LLM
* return the underlying retrieved passages alongside the answer
* allow users to compare generated claims directly with their supporting evidence

Citation correctness has not yet been independently verified through a formal automated evaluation.

### Privacy and Confidential Data

Document-ingestion systems may create privacy or confidentiality risks if sensitive information is indexed or transmitted to external services.

Current mitigations:

* use public documents for the portfolio version
* do not ingest confidential employer or personal data
* do not commit API keys or other secrets to GitHub
* exclude `.env` through `.gitignore`
* keep the OpenAI API key in the local environment only

## Human Oversight

Users should be able to inspect the retrieved source passages supporting generated answers.

Generated responses should not be relied upon without source verification for decisions involving financial, mortgage, legal, investment, property-valuation, or other high-impact matters.

The system is therefore designed as an information-access demonstration rather than an autonomous decision-making system.

## Current Evaluation Status

Initial functional testing has confirmed:

* successful ingestion and indexing of authoritative UK property documents
* semantic retrieval from the indexed knowledge base
* second-stage multilingual cross-encoder reranking
* cross-lingual retrieval using equivalent English, Hindi, and German questions
* retrieval of the expected ONS evidence within the top results after reranking
* end-to-end grounded answer generation through the `/ask` endpoint

These checks demonstrate that the core RAG workflow functions as intended, but they do not constitute a comprehensive performance evaluation.

## Future Evaluation Enhancements

A production-oriented evaluation could additionally measure:

* retrieval Recall@K
* Mean Reciprocal Rank (MRR)
* citation correctness
* answer faithfulness
* unsupported-question behaviour
* multilingual performance by language
* latency
* top-k sensitivity
* known failure cases
* systematic error analysis

These measures would be required before making broader claims about system accuracy, reliability, or production readiness.
