import duckdb
from config import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.db_path = str(settings.DB_PATH)
        self.conn = duckdb.connect(self.db_path)
        self._init_schema()

    def _init_schema(self):
        """Initializes the database schema."""
        self.conn.execute("""
            CREATE SEQUENCE IF NOT EXISTS doc_id_seq;
            CREATE TABLE IF NOT EXISTS documents (
                id VARCHAR PRIMARY KEY,
                filename VARCHAR,
                ingest_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS chunks (
                id VARCHAR PRIMARY KEY,
                doc_id VARCHAR,
                content TEXT,
                page_num INTEGER,
                FOREIGN KEY (doc_id) REFERENCES documents(id)
            );
            
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY,
                doc_id VARCHAR,
                metric_name VARCHAR,
                value VARCHAR,
                unit VARCHAR,
                period VARCHAR,
                FOREIGN KEY (doc_id) REFERENCES documents(id)
            );
        """)
        logger.info("Database schema initialized.")

    def add_document(self, doc_id: str, filename: str):
        self.conn.execute(
            "INSERT INTO documents (id, filename) VALUES (?, ?)", 
            [doc_id, filename]
        )

    def add_chunk(self, chunk_id: str, doc_id: str, content: str, page_num: int):
        self.conn.execute(
            "INSERT INTO chunks (id, doc_id, content, page_num) VALUES (?, ?, ?, ?)",
            [chunk_id, doc_id, content, page_num]
        )
    
    def get_document(self, doc_id: str):
        return self.conn.execute(
            "SELECT * FROM documents WHERE id = ?", [doc_id]
        ).fetchone()

    def get_all_chunks(self, doc_id: str):
        return self.conn.execute(
            "SELECT content, page_num FROM chunks WHERE doc_id = ?", [doc_id]
        ).fetchall()

    def get_context(self, doc_id: str, limit: int = 5):
        """Retrieve full context for a doc."""
        return self.conn.execute(
            "SELECT content FROM chunks WHERE doc_id = ? LIMIT ?", [doc_id, limit]
        ).fetchall()
        
    def close(self):
        self.conn.close()
