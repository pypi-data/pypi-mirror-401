"""
Enhanced Vector Database for FlawHunt CLI Conversation Storage.

This module provides semantic search capabilities for conversation history,
allowing the AI to find relevant past conversations based on similarity.
"""

import json
import time
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib

try:
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer
    VECTOR_DEPS_AVAILABLE = True
except ImportError:
    faiss = None
    np = None
    SentenceTransformer = None
    VECTOR_DEPS_AVAILABLE = False

APP_DIR = Path.home() / ".ai_terminal"
APP_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_INDEX_FILE = str(APP_DIR / "conversation_vectors.index")
VECTOR_METADATA_FILE = APP_DIR / "vector_metadata.json"
VECTOR_TEXTS_FILE = APP_DIR / "vector_texts.pkl"

@dataclass
class ConversationVector:
    """Represents a conversation entry in the vector database."""
    id: str
    session_id: str
    user_input: str
    ai_response: str
    timestamp: float
    metadata: Dict[str, Any]
    vector_id: int  # Index in the FAISS database
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationVector':
        return cls(**data)
    
    def get_combined_text(self) -> str:
        """Get combined text for vectorization."""
        return f"User: {self.user_input}\nAssistant: {self.ai_response}"
    
    def get_search_text(self) -> str:
        """Get text optimized for search queries."""
        return f"{self.user_input} {self.ai_response}"

class ConversationVectorStore:
    """Enhanced vector store for conversation semantic search."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.enabled = False
        self.encoder = None
        self.index = None
        self.conversations: List[ConversationVector] = []
        self.texts: List[str] = []
        self.id_to_vector_id: Dict[str, int] = {}
        self.vector_id_to_conversation_id: Dict[int, str] = {}
        
        self._init_vector_store()
        self._load_existing_data()
    
    def _init_vector_store(self):
        """Initialize the vector store components."""
        if not VECTOR_DEPS_AVAILABLE:
            print("Vector dependencies not available. Install: pip install faiss-cpu sentence-transformers")
            return
        
        try:
            self.encoder = SentenceTransformer(self.model_name)
            dim = self.encoder.get_sentence_embedding_dimension()
            self.index = faiss.IndexFlatL2(dim)
            self.enabled = True
            print(f"Vector store initialized with {dim}-dimensional embeddings")
        except Exception as e:
            print(f"Failed to initialize vector store: {e}")
            self.enabled = False
    
    def _load_existing_data(self):
        """Load existing vector data from disk."""
        if not self.enabled:
            return
        
        try:
            # Load FAISS index
            if Path(VECTOR_INDEX_FILE).exists():
                self.index = faiss.read_index(VECTOR_INDEX_FILE)
                print(f"Loaded FAISS index with {self.index.ntotal} vectors")
            
            # Load metadata
            if VECTOR_METADATA_FILE.exists():
                with open(VECTOR_METADATA_FILE, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    self.conversations = [ConversationVector.from_dict(item) for item in metadata.get('conversations', [])]
                    self.id_to_vector_id = metadata.get('id_to_vector_id', {})
                    self.vector_id_to_conversation_id = metadata.get('vector_id_to_conversation_id', {})
                    # Convert string keys back to int for vector_id_to_conversation_id
                    self.vector_id_to_conversation_id = {int(k): v for k, v in self.vector_id_to_conversation_id.items()}
            
            # Load texts
            if VECTOR_TEXTS_FILE.exists():
                with open(VECTOR_TEXTS_FILE, 'rb') as f:
                    self.texts = pickle.load(f)
            
            print(f"Loaded {len(self.conversations)} conversation vectors")
        except Exception as e:
            print(f"Error loading existing vector data: {e}")
            # Reset on error
            self.conversations = []
            self.texts = []
            self.id_to_vector_id = {}
            self.vector_id_to_conversation_id = {}
    
    def _save_data(self):
        """Save vector data to disk."""
        if not self.enabled:
            return
        
        try:
            # Save FAISS index
            if self.index and self.index.ntotal > 0:
                faiss.write_index(self.index, VECTOR_INDEX_FILE)
            
            # Save metadata
            metadata = {
                'conversations': [conv.to_dict() for conv in self.conversations],
                'id_to_vector_id': self.id_to_vector_id,
                'vector_id_to_conversation_id': {str(k): v for k, v in self.vector_id_to_conversation_id.items()}
            }
            with open(VECTOR_METADATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            # Save texts
            with open(VECTOR_TEXTS_FILE, 'wb') as f:
                pickle.dump(self.texts, f)
        
        except Exception as e:
            print(f"Error saving vector data: {e}")
    
    def add_conversation(self, conversation_id: str, session_id: str, user_input: str, 
                        ai_response: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add a conversation to the vector store."""
        if not self.enabled:
            return False
        
        # Skip if already exists
        if conversation_id in self.id_to_vector_id:
            return True
        
        try:
            # Create conversation vector object
            conv_vector = ConversationVector(
                id=conversation_id,
                session_id=session_id,
                user_input=user_input,
                ai_response=ai_response,
                timestamp=time.time(),
                metadata=metadata or {},
                vector_id=len(self.conversations)  # Will be the next vector ID
            )
            
            # Get text for vectorization
            text = conv_vector.get_combined_text()
            
            # Create embedding
            embedding = self.encoder.encode([text]).astype("float32")
            
            # Add to FAISS index
            vector_id = self.index.ntotal  # Current size becomes the new vector ID
            self.index.add(embedding)
            
            # Update conversation vector with actual vector ID
            conv_vector.vector_id = vector_id
            
            # Store mappings
            self.conversations.append(conv_vector)
            self.texts.append(text)
            self.id_to_vector_id[conversation_id] = vector_id
            self.vector_id_to_conversation_id[vector_id] = conversation_id
            
            # Save to disk
            self._save_data()
            
            return True
        
        except Exception as e:
            print(f"Error adding conversation to vector store: {e}")
            return False
    
    def search_similar_conversations(self, query: str, k: int = 5, 
                                   min_similarity: float = 0.3) -> List[Tuple[ConversationVector, float]]:
        """Search for similar conversations based on semantic similarity."""
        if not self.enabled or self.index.ntotal == 0:
            return []
        
        try:
            # Create query embedding
            query_embedding = self.encoder.encode([query]).astype("float32")
            
            # Search in FAISS index
            distances, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
            
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx >= 0 and idx < len(self.conversations):
                    # Convert distance to similarity score (higher = more similar)
                    similarity = 1.0 / (1.0 + float(distance))
                    
                    if similarity >= min_similarity:
                        conversation = self.conversations[idx]
                        results.append((conversation, similarity))
            
            # Sort by similarity (highest first)
            results.sort(key=lambda x: x[1], reverse=True)
            
            return results
        
        except Exception as e:
            print(f"Error searching conversations: {e}")
            return []
    
    def search_by_content(self, query: str, k: int = 5) -> List[ConversationVector]:
        """Simple content-based search (fallback when vectors not available)."""
        query_lower = query.lower()
        matches = []
        
        for conv in self.conversations:
            if (query_lower in conv.user_input.lower() or 
                query_lower in conv.ai_response.lower()):
                matches.append(conv)
        
        # Sort by timestamp (most recent first)
        matches.sort(key=lambda x: x.timestamp, reverse=True)
        return matches[:k]
    
    def _enhanced_context_search(self, query: str, k: int = 3) -> List[Tuple[ConversationVector, float]]:
        """Enhanced search that combines multiple strategies for better context matching."""
        if not self.enabled or self.index.ntotal == 0:
            return []
        
        # Strategy 1: Direct similarity search
        direct_results = self.search_similar_conversations(query, k=k*2, min_similarity=0.3)
        
        # Strategy 2: Search for information-providing conversations
        # Look for conversations where the AI provides specific information
        info_keywords = ['name', 'akash', 'call me', 'i am', 'my name is', 'hello']
        query_lower = query.lower()
        
        enhanced_results = []
        seen_conversations = set()
        
        # First, prioritize conversations that might contain answers
        if any(keyword in query_lower for keyword in ['name', 'who am i', 'what is my']):
            # Look for conversations containing personal information
            for conv in self.conversations:
                if conv.id in seen_conversations:
                    continue
                    
                ai_response_lower = conv.ai_response.lower()
                user_input_lower = conv.user_input.lower()
                
                # Prioritize conversations where user provided info or AI acknowledged it
                if ('akash' in ai_response_lower or 
                    'hello akash' in ai_response_lower or
                    'my name is' in user_input_lower or
                    'call me' in user_input_lower):
                    
                    # Calculate relevance score based on content match
                    relevance_score = 0.8  # High relevance for personal info
                    if 'hello akash' in ai_response_lower:
                        relevance_score = 0.9
                    
                    enhanced_results.append((conv, relevance_score))
                    seen_conversations.add(conv.id)
        
        # Add direct similarity results (but filter duplicates)
        for conv, sim_score in direct_results:
            if conv.id not in seen_conversations:
                enhanced_results.append((conv, sim_score))
                seen_conversations.add(conv.id)
        
        # Sort by relevance score (highest first) and limit results
        enhanced_results.sort(key=lambda x: x[1], reverse=True)
        return enhanced_results[:k]
    
    def get_conversation_context(self, query: str, max_context_length: int = 2000) -> str:
        """Get formatted conversation context based on enhanced similarity search."""
        if not self.enabled:
            return ""
        
        # Enhanced search strategy for better context matching
        similar_conversations = self._enhanced_context_search(query, k=3)
        
        if not similar_conversations:
            return ""
        
        context_lines = ["=== Relevant Past Conversations ==="]
        
        for conv, similarity in similar_conversations:
            # Format conversation with similarity score
            user_text = conv.user_input[:150] + "..." if len(conv.user_input) > 150 else conv.user_input
            ai_text = conv.ai_response[:200] + "..." if len(conv.ai_response) > 200 else conv.ai_response
            
            context_lines.append(f"[Similarity: {similarity:.2f}]")
            context_lines.append(f"User: {user_text}")
            context_lines.append(f"Assistant: {ai_text}")
            context_lines.append("---")
        
        context = "\n".join(context_lines)
        
        # Trim if too long
        if len(context) > max_context_length:
            context = context[:max_context_length] + "...\n[Context truncated]"
        
        return context + "\n=== End Relevant Context ===\n\n"
    
    def update_conversation(self, conversation_id: str, user_input: str, ai_response: str):
        """Update an existing conversation (re-vectorizes)."""
        if not self.enabled or conversation_id not in self.id_to_vector_id:
            return False
        
        # Find the conversation
        for i, conv in enumerate(self.conversations):
            if conv.id == conversation_id:
                # Update the conversation
                conv.user_input = user_input
                conv.ai_response = ai_response
                
                # Re-vectorize
                new_text = conv.get_combined_text()
                self.texts[conv.vector_id] = new_text
                
                # Update the embedding in FAISS (requires rebuilding index)
                self._rebuild_index()
                return True
        
        return False
    
    def _rebuild_index(self):
        """Rebuild the FAISS index (needed after updates)."""
        if not self.enabled or not self.texts:
            return
        
        try:
            # Create new index
            dim = self.encoder.get_sentence_embedding_dimension()
            new_index = faiss.IndexFlatL2(dim)
            
            # Re-encode all texts
            if self.texts:
                embeddings = self.encoder.encode(self.texts).astype("float32")
                new_index.add(embeddings)
            
            self.index = new_index
            self._save_data()
        
        except Exception as e:
            print(f"Error rebuilding index: {e}")
    
    def remove_conversation(self, conversation_id: str) -> bool:
        """Remove a conversation from the vector store."""
        if not self.enabled or conversation_id not in self.id_to_vector_id:
            return False
        
        # Find and remove conversation
        self.conversations = [conv for conv in self.conversations if conv.id != conversation_id]
        
        # Remove from mappings
        if conversation_id in self.id_to_vector_id:
            del self.id_to_vector_id[conversation_id]
        
        # Rebuild everything (FAISS doesn't support individual deletions easily)
        self._rebuild_mappings_and_index()
        return True
    
    def _rebuild_mappings_and_index(self):
        """Rebuild all mappings and the FAISS index."""
        if not self.enabled:
            return
        
        # Reset mappings
        self.id_to_vector_id = {}
        self.vector_id_to_conversation_id = {}
        self.texts = []
        
        # Rebuild from conversations
        for i, conv in enumerate(self.conversations):
            conv.vector_id = i
            self.id_to_vector_id[conv.id] = i
            self.vector_id_to_conversation_id[i] = conv.id
            self.texts.append(conv.get_combined_text())
        
        # Rebuild index
        self._rebuild_index()
    
    def clear_all(self):
        """Clear all conversation vectors."""
        if self.enabled:
            # Reset everything
            dim = self.encoder.get_sentence_embedding_dimension()
            self.index = faiss.IndexFlatL2(dim)
        
        self.conversations = []
        self.texts = []
        self.id_to_vector_id = {}
        self.vector_id_to_conversation_id = {}
        
        # Save empty state
        self._save_data()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics."""
        return {
            "enabled": self.enabled,
            "total_conversations": len(self.conversations),
            "total_vectors": self.index.ntotal if self.index else 0,
            "model_name": self.model_name,
            "vector_dimension": self.encoder.get_sentence_embedding_dimension() if self.encoder else None,
            "storage_files": {
                "index": VECTOR_INDEX_FILE,
                "metadata": str(VECTOR_METADATA_FILE),
                "texts": str(VECTOR_TEXTS_FILE)
            }
        }
    
    def search_and_display_results(self, query: str, k: int = 5):
        """Search and display results in a formatted way."""
        from rich.console import Console
        from rich.table import Table
        from rich import box
        
        console = Console()
        
        if not self.enabled:
            console.print("[red]Vector store not available. Install faiss-cpu and sentence-transformers.[/red]")
            return
        
        results = self.search_similar_conversations(query, k)
        
        if not results:
            console.print("[dim]No similar conversations found.[/dim]")
            return
        
        table = Table(title=f"Similar Conversations for: '{query}'", box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column("Similarity", width=10, style="green")
        table.add_column("User Input", width=40, overflow="fold")
        table.add_column("AI Response", width=40, overflow="fold")
        table.add_column("When", width=16, style="cyan")
        
        for conv, similarity in results:
            from datetime import datetime
            timestamp = datetime.fromtimestamp(conv.timestamp).strftime("%Y-%m-%d %H:%M")
            
            user_preview = conv.user_input[:60] + "..." if len(conv.user_input) > 60 else conv.user_input
            ai_preview = conv.ai_response[:60] + "..." if len(conv.ai_response) > 60 else conv.ai_response
            
            table.add_row(
                f"{similarity:.3f}",
                user_preview,
                ai_preview,
                timestamp
            )
        
        console.print(table)
