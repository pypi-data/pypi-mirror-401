"""
Persistence utilities for FlawHunt CLI.
Handles state management and vector store operations.
"""
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

try:
    import faiss  # type: ignore
    import numpy as np
    from sentence_transformers import SentenceTransformer
except ImportError:
    faiss = None
    np = None
    SentenceTransformer = None

APP_DIR = Path.home() / ".ai_terminal"
APP_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = APP_DIR / "state.json"
VECTOR_FILE = APP_DIR / "vector.pkl"
FAISS_FILE = str(APP_DIR / "faiss.index")

def load_state() -> Dict[str, Any]:
    """Load application state from JSON file."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {
        "safe_mode": True,
        "use_faiss": False,
        "model": "moonshotai/kimi-k2-instruct-0905",
        "memory": [],  # list of {user, ai, ts}
    }

def save_state(state: Dict[str, Any]) -> None:
    """Save application state to JSON file."""
    STATE_FILE.write_text(json.dumps(state, indent=2))

@dataclass
class VectorStore:
    """Vector store for semantic memory using FAISS."""
    enabled: bool = False
    model_name: str = "all-MiniLM-L6-v2"
    encoder: Any = None
    index: Any = None
    texts: List[str] = field(default_factory=list)

    def __post_init__(self):
        if faiss is not None and SentenceTransformer is not None:
            try:
                self.encoder = SentenceTransformer(self.model_name)
                dim = self.encoder.get_sentence_embedding_dimension()
                self.index = faiss.IndexFlatL2(dim)
                self.enabled = True
                if Path(FAISS_FILE).exists():
                    try:
                        self.index = faiss.read_index(FAISS_FILE)
                    except Exception:
                        pass
            except Exception:
                self.enabled = False

    def add(self, text: str):
        """Add text to vector store."""
        if not self.enabled:
            return
        vec = self.encoder.encode([text]).astype("float32")
        if self.index.ntotal == 0:
            self.index.add(vec)
        else:
            self.index.add(vec)
        self.texts.append(text)
        try:
            faiss.write_index(self.index, FAISS_FILE)
        except Exception:
            pass

    def search(self, query: str, k: int = 3) -> List[str]:
        """Search for similar texts in vector store."""
        if not self.enabled or self.index is None or self.index.ntotal == 0:
            return []
        q = self.encoder.encode([query]).astype("float32")
        D, I = self.index.search(q, k)
        results = []
        for idx in I[0]:
            if 0 <= idx < len(self.texts):
                results.append(self.texts[idx])
        return results

    def search_with_scores(self, query: str, k: int = 3) -> List[tuple[str, float]]:
        """Search for similar texts with similarity scores."""
        if not self.enabled or self.index is None or self.index.ntotal == 0:
            return []
        q = self.encoder.encode([query]).astype("float32")
        distances, indices = self.index.search(q, k)
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if 0 <= idx < len(self.texts):
                similarity = 1.0 / (1.0 + float(distance))
                results.append((self.texts[idx], similarity))
        return results

    def get_stats(self) -> dict:
        """Get statistics about the vector store."""
        return {
            "total_documents": len(self.texts),
            "index_exists": self.index is not None,
            "vector_size": self.encoder.get_sentence_embedding_dimension() if self.encoder else None,
            "enabled": self.enabled,
            "storage_path": FAISS_FILE
        }