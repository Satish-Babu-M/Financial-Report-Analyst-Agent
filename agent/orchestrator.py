from typing import Dict, List, Any
import re
from storage.database import DatabaseManager
from storage.vector import VectorStore
import logging

logger = logging.getLogger(__name__)

class MetricExtractor:
    def __init__(self):
        # Regex patterns from our validated RuleBasedAnalyzer
        self.patterns = {
            "revenue": r"(?i)(?:revenue|sales)(?:\s+of)?\s*[:\-]?\s*[\$]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?)",
            "net_income": r"(?i)(?:net\s+income|profit)(?:\s+of)?\s*[:\-]?\s*[\$]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?)",
            "expenses": r"(?i)(?:expenses|operating\s+costs)(?:\s+of)?\s*[:\-]?\s*[\$]?\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?)",
            "eps": r"(?i)(?:eps|earnings\s+per\s+share)(?:\s+of)?\s*[:\-]?\s*[\$]?\s*(\d+(?:\.\d+)?)",
        }

    def extract(self, text: str) -> Dict[str, Any]:
        metrics = {}
        for key, pattern in self.patterns.items():
            match = re.search(pattern, text)
            if match:
                metrics[key] = match.group(1)
            else:
                metrics[key] = "N/A"
        return metrics

class AgentOrchestrator:
    def __init__(self):
        self.db = DatabaseManager()
        self.vector_store = VectorStore()
        self.metric_extractor = MetricExtractor()

    def generate_report(self, doc_id: str, report_type: str = "summary") -> Dict:
        """
        Orchestrates the creation of a report.
        """
        # 1. Retrieve full content (or chunks)
        # For our scale, we can just grab all chunks for metrics
        chunks = self.db.get_all_chunks(doc_id)
        if not chunks:
            return {"error": f"Document {doc_id} not found."}

        full_text = "\n".join([c[0] for c in chunks])

        report = {
            "doc_id": doc_id,
            "type": report_type,
            "metrics": {},
            "summary": "",
            "risks_and_drivers": []
        }

        # 2. Extract Metrics
        report["metrics"] = self.metric_extractor.extract(full_text)

        # 3. Generate Summary (Heuristic / Extraction)
        # Extract sentences with key terms
        report["summary"] = self._heuristic_summary(full_text)

        # 4. Risks & Drivers
        report["risks_and_drivers"] = self._extract_key_sentences(full_text, ["risk", "growth", "decline", "guidance"])

        return report

    def ask_question(self, query: str, doc_id: str = None) -> Dict:
        """
        Performs RAG to answer a question.
        For Non-LLM mode, this returns the top matching context chunks.
        """
        matches = self.vector_store.search(query, k=3, filter_doc_id=doc_id)
        
        answer = {
            "query": query,
            "answer": "Context retrieved (LLM integration required for synthesis). Top matches:",
            "citations": []
        }
        
        for m in matches:
            citation = f"...{m['content'][:200]}..."
            answer["citations"].append({
                "text": citation,
                "page": m['metadata'].get('page', 'Unknown'),
                "score": m['score']
            })
            
        return answer

    def _heuristic_summary(self, text: str) -> str:
        """
        Basic extractive summarizer.
        """
        # Grab first 500 chars usually contains intro
        intro = text[:500]
        return f"{intro}..."

    def _extract_key_sentences(self, text: str, keywords: List[str]) -> List[str]:
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text.replace('\n', ' '))
        hits = []
        for s in sentences:
            if any(k in s.lower() for k in keywords):
                if len(s) > 20: # Filter short noise
                    hits.append(s.strip())
        return hits[:10] # Top 10
