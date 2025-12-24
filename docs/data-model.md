# Data Model

This document describes the core data structures used by FRAA.

---

## Document

Represents a single financial document.

Fields:
- doc_id
- source_path
- document_type
- company_name
- fiscal_period
- created_at

---

## Chunk

A section-aware unit of text used for retrieval.

Fields:
- chunk_id
- doc_id
- section_path
- page_start
- page_end
- text
- embedding_reference

---

## Table

Represents extracted tabular financial data.

Fields:
- table_id
- doc_id
- page_number
- title_guess
- raw_rows
- raw_text

---

## Extracted Metric

Normalized financial metric extracted from the document.

Fields:
- metric_name
- value
- unit_scale
- currency
- period_label
- citation

---

## Citation

Tracks evidence for every claim.

Fields:
- doc_id
- page_number
- section_path
- text_snippet

---

## Design principles

- Every metric must have a citation
- Units must be normalized
- Missing data is explicitly marked
- No inferred values
