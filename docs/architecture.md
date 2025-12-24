# Architecture Overview

This document describes the internal architecture of the Financial Report Analysis Agent (FRAA).

The system is designed as a local-first analysis engine that can later be exposed through an API and web interface.

---

## High-level flow

1. User provides a financial document (PDF, HTML, or text)
2. Document is parsed and segmented into structured chunks
3. Chunks are indexed for retrieval
4. An AI agent performs extraction, summarization, and Q&A
5. Outputs are generated with citations

---

## Core components

### 1. Ingestion
Responsible for loading and parsing documents.

- PDF parsing (text-based)
- Section detection
- Page-level metadata extraction

Output:
- Clean text
- Section-aware chunks
- Table candidates

---

### 2. Storage
Local persistence layer.

- SQLite or DuckDB for structured metadata
- JSON artifacts for parsed documents
- Filesystem storage for originals

---

### 3. Indexing and retrieval
Supports evidence-based question answering.

- Embedding generation for chunks
- FAISS vector index
- Optional keyword-based retrieval
- Section-aware ranking

---

### 4. Agent orchestrator
Coordinates all analysis steps.

Responsibilities:
- Document classification
- Metric extraction
- Change detection
- Risk identification
- Grounded summarization
- Q&A with citations

---

### 5. Output generation
Produces user-facing artifacts.

- Markdown reports
- JSON structured data
- CLI responses

---

## Future architecture

Later stages will introduce:
- FastAPI backend
- Job queue for long-running analysis
- Web-based UI
- Persistent user sessions

The core services are designed to be reusable without modification.

---

## Local Tool (Now)

```mermaid
flowchart TB
  U[User CLI] -->|PDF / HTML / TXT| ING[Ingestion & Parsing]
  ING --> META[Doc Metadata<br/>company, period, doc type]
  ING --> CHUNK[Section Splitter + Chunker]
  ING --> TAB[Table Extractor]

  CHUNK --> STORE[(Local Doc Store<br/>SQLite/DuckDB + filesystem)]
  TAB --> STORE
  META --> STORE

  STORE --> EMB[Embedding Generator]
  EMB --> VDB[(Vector Index<br/>FAISS)]
  STORE --> BM25[(Optional BM25 Index)]

  U -->|Questions| QA[Q&A Service]
  QA --> RET[Retriever<br/>Vector + BM25 + rerank]
  RET --> VDB
  RET --> BM25
  RET --> STORE

  QA --> LLM[LLM Reasoner<br/>Grounded prompts]
  LLM --> QA

  STORE --> EXT[Structured Extractor<br/>metrics, guidance, risks]
  EXT --> LLM
  EXT --> OUT[Report Builder<br/>Markdown + JSON]
  OUT --> U
