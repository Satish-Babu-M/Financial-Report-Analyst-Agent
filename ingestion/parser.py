import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentParser:
    def __init__(self):
        pass

    def parse_file(self, file_path: str) -> List[Dict]:
        """
        Parses a file and returns a list of chunks/pages.
        
        Returns:
            List[Dict]: {'page': int, 'content': str, 'tables': List}
        """
        path = Path(file_path)
        if path.suffix.lower() == ".pdf":
            return self._parse_pdf(path)
        elif path.suffix.lower() in [".txt", ".md"]:
            return self._parse_text(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

    def _parse_pdf(self, path: Path) -> List[Dict]:
        logger.info(f"Parsing PDF: {path}")
        results = []
        doc = fitz.open(path)
        
        for page_num, page in enumerate(doc):
            text = page.get_text()
            # Basic chunking: Page level for now. 
            # Advanced agents would semantic chunk here.
            
            # Simple cleanup
            text = text.strip()
            
            if text:
                results.append({
                    "page": page_num + 1,
                    "content": text,
                    "tables": [] # Placeholder for table extraction logic
                })
        return results

    def _parse_text(self, path: Path) -> List[Dict]:
        logger.info(f"Parsing Text: {path}")
        text = path.read_text(encoding="utf-8")
        # Split by double newline as basic paragraph chunking
        chunks = text.split("\n\n")
        
        return [
            {"page": i+1, "content": chunk.strip(), "tables": []}
            for i, chunk in enumerate(chunks) if chunk.strip()
        ]
