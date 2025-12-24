# Financial Report Analysis Agent (FRAA)

A local, citation-grounded AI agent that analyzes financial documents such as earnings reports, 10-Ks, 10-Qs, and transcripts.  
It extracts key financial metrics, identifies changes and risks, and answers questions with evidence.

This tool is designed to solve real finance problems around speed, accuracy, and information overload.

---

## What this tool does

Given one or more financial documents, FRAA can:

- Extract key financial metrics (revenue, margins, cash flow, debt, etc.)
- Generate an analyst-style executive summary
- Highlight what changed and why
- Identify risks, guidance, and watch items
- Answer natural language questions with citations
- Export structured outputs for reuse

All insights are grounded in the source documents.  
If evidence is missing, the agent will say so.

---

## Current scope (local backend tool)

This repository implements a **local Python CLI tool** that acts as the backend analysis engine.

Planned evolution:
1. Local Python tool (this repo)
2. Backend API (FastAPI)
3. Web application (React / Next.js)

---

## Supported inputs

- PDF (text-based PDFs)
- HTML files
- Plain text files

Planned later:
- Scanned PDFs (OCR)
- Excel financials
- Multi-company comparisons

---

## Outputs

- Markdown report (`.md`)
- Structured JSON output
- CLI-based Q&A with citations

Example sections in a Markdown report:
- Executive summary
- Key financial metrics
- Drivers and changes
- Guidance and outlook
- Risks and watch items
- Evidence appendix

Planned later:
- Detailed Dashbords

---

## Key design principles

- **Citations are mandatory**  
  Every non-trivial claim is tied to document evidence.

- **No guessing**  
  If a number or answer is not in the document, the agent refuses.

- **Finance-aware structure**  
  Understands sections like MD&A, guidance, non-GAAP adjustments, and risk factors.

- **Local-first**  
  Works on your machine without a web UI.

---

## Architecture overview (local tool)
