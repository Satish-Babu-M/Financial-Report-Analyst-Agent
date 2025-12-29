# Advanced Financial Report Analyst CLI

A powerful, terminal-based financial analysis engine that uses **Deterministic Logic (Regex)** for metric extraction and **Vector Search (RAG)** for contextual question answering.

## 🚀 Features
- **Deterministic Extraction**: Exact parsing of Revenue, Net Income, EPS, and Expenses using specialized regex patterns.
- **RAG-powered Q&A**: Intelligent retrieval of document sections to answer natural language questions with page citations.
- **Local Persistency**: Uses DuckDB for structured metadata and FAISS for fast vector indexing. 
- **Privacy-First**: No data leaves your machine; embeddings are generated locally.

## 📂 Project Structure
- `cli.py`: Main interactive command-line interface.
- `agent/`: Core logic for analysis and metric extraction.
- `ingestion/`: PDF and text parsing using PyMuPDF.
- `storage/`: Database and Vector Index management.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd financial-report-analyst
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage Guide

### 1. Ingest a Report
Processes a PDF, extracts text, and builds the local vector index.
```bash
python3 cli.py ingest path/to/report.pdf --doc-id my-report
```

### 2. Generate Analysis
Produces an instant report with Key Metrics and a Heuristic Summary.
```bash
python3 cli.py analyze my-report
```

### 3. Ask Questions (RAG)
Ask specific questions about the document to get context-aware answers.
```bash
python3 cli.py ask "What was the revenue growth of Google Cloud?" --doc-id my-report
```

## 📦 Requirements
- Python 3.9+
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
- [DuckDB](https://duckdb.org/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Sentence-Transformers](https://www.sbert.net/)

## Documentation
- [Detailed Documentation](docs/documentation.md)

---
