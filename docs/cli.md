# CLI Usage

The Financial Report Analysis Agent is operated through a command-line interface.

---

## Ingest documents

```bash
fra ingest path/to/document.pdf
```
Parses the document, builds indices, and stores artifacts locally.

```bash
fra analyze <doc_id> --output report.md
```
Generates:
	•	Executive summary
	•	Key financial metrics
	•	Risks and guidance
	•	Evidence-backed insights

```bash
fra ask <doc_id> "Why did operating margin decline?"
```

Strict mode:

```bash
fra ask <doc_id> "What is the FY guidance?" --strict
```

Strict mode refuses to answer if evidence is insufficient.

```bash
fra compare <doc_id_1> <doc_id_2>
```

Used for:
	•	Quarter-over-quarter comparisons
	•	Company-to-company analysis
