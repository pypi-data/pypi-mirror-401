"""
Enhanced Conversation History Management for FlawHunt CLI.

This module provides advanced conversation history functionality including:
- Structured conversation storage with metadata
- Context injection for better agent responses
- Search and filtering capabilities
- Session management
- Export/import functionality
"""

import json
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from .vector_store import ConversationVectorStore

APP_DIR = Path.home() / ".ai_terminal"
APP_DIR.mkdir(parents=True, exist_ok=True)
CONVERSATIONS_FILE = APP_DIR / "conversations.json"
SESSIONS_FILE = APP_DIR / "sessions.json"

console = Console()

@dataclass
class ConversationEntry:
    """Represents a single conversation turn."""
    id: str
    session_id: str
    user_input: str
    ai_response: str
    timestamp: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationEntry':
        return cls(**data)
    
    def get_formatted_time(self) -> str:
        """Get human-readable timestamp."""
        dt = datetime.fromtimestamp(self.timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    def is_recent(self, hours: int = 24) -> bool:
        """Check if entry is within the specified number of hours."""
        cutoff = time.time() - (hours * 3600)
        return self.timestamp >= cutoff

@dataclass 
class ConversationSession:
    """Represents a conversation session."""
    id: str
    name: str
    created_at: float
    last_activity: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationSession':
        return cls(**data)
    
    def get_formatted_created_time(self) -> str:
        dt = datetime.fromtimestamp(self.created_at)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

class ConversationHistoryManager:
    """Advanced conversation history management with vector search."""
    
    def __init__(self):
        self.conversations: List[ConversationEntry] = []
        self.sessions: Dict[str, ConversationSession] = {}
        self.current_session_id: Optional[str] = None
        self.vector_store = ConversationVectorStore()
        self.load_history()
        self.load_sessions()
        self._sync_with_vector_store()
    
    def load_history(self):
        """Load conversation history from file."""
        if CONVERSATIONS_FILE.exists():
            try:
                with open(CONVERSATIONS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversations = [ConversationEntry.from_dict(entry) for entry in data]
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load conversation history: {e}[/yellow]")
                self.conversations = []
    
    def load_sessions(self):
        """Load session data from file."""
        if SESSIONS_FILE.exists():
            try:
                with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.sessions = {k: ConversationSession.from_dict(v) for k, v in data.items()}
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load sessions: {e}[/yellow]")
                self.sessions = {}
    
    def save_history(self):
        """Save conversation history to file."""
        try:
            with open(CONVERSATIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump([entry.to_dict() for entry in self.conversations], f, indent=2, ensure_ascii=False)
        except Exception as e:
            console.print(f"[red]Error saving conversation history: {e}[/red]")
    
    def save_sessions(self):
        """Save session data to file."""
        try:
            with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump({k: v.to_dict() for k, v in self.sessions.items()}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            console.print(f"[red]Error saving sessions: {e}[/red]")
    
    def create_session(self, name: Optional[str] = None) -> str:
        """Create a new conversation session."""
        session_id = str(uuid.uuid4())
        if not name:
            name = f"Session {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        session = ConversationSession(
            id=session_id,
            name=name,
            created_at=time.time(),
            last_activity=time.time(),
            metadata={}
        )
        
        self.sessions[session_id] = session
        self.current_session_id = session_id
        self.save_sessions()
        return session_id
    
    def get_or_create_current_session(self) -> str:
        """Get current session or create one if none exists."""
        if not self.current_session_id or self.current_session_id not in self.sessions:
            return self.create_session()
        return self.current_session_id
    
    def switch_session(self, session_id: str) -> bool:
        """Switch to a different session."""
        if session_id in self.sessions:
            self.current_session_id = session_id
            return True
        return False
    
    def add_conversation(self, user_input: str, ai_response: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a conversation entry to current session and vector store."""
        session_id = self.get_or_create_current_session()
        entry_id = str(uuid.uuid4())
        
        entry = ConversationEntry(
            id=entry_id,
            session_id=session_id,
            user_input=user_input,
            ai_response=ai_response,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        
        self.conversations.append(entry)
        
        # Add to vector store for semantic search
        self.vector_store.add_conversation(
            conversation_id=entry_id,
            session_id=session_id,
            user_input=user_input,
            ai_response=ai_response,
            metadata=metadata or {}
        )
        
        # Update session activity
        if session_id in self.sessions:
            self.sessions[session_id].last_activity = time.time()
        
        # Trim old conversations to prevent unbounded growth
        self._trim_conversations()
        
        self.save_history()
        self.save_sessions()
        return entry_id
    
    def _trim_conversations(self, max_conversations: int = 1000):
        """Trim conversations to prevent memory issues."""
        if len(self.conversations) > max_conversations:
            # Keep the most recent conversations
            self.conversations = sorted(self.conversations, key=lambda x: x.timestamp)[-max_conversations:]
    
    def get_recent_context(self, max_entries: int = 5, hours: int = 24) -> List[ConversationEntry]:
        """Get recent conversation context for the current session."""
        if not self.current_session_id:
            return []
        
        # Get conversations from current session within time limit
        recent = [
            entry for entry in self.conversations
            if entry.session_id == self.current_session_id and entry.is_recent(hours)
        ]
        
        # Sort by timestamp and return most recent
        recent.sort(key=lambda x: x.timestamp, reverse=True)
        return recent[:max_entries]
    
    def search_conversations(self, query: str, limit: int = 10) -> List[ConversationEntry]:
        """Search conversations by content."""
        query_lower = query.lower()
        matches = []
        
        for entry in self.conversations:
            if (query_lower in entry.user_input.lower() or 
                query_lower in entry.ai_response.lower()):
                matches.append(entry)
        
        # Sort by relevance (most recent first)
        matches.sort(key=lambda x: x.timestamp, reverse=True)
        return matches[:limit]
    
    def get_session_conversations(self, session_id: str) -> List[ConversationEntry]:
        """Get all conversations for a specific session."""
        return [entry for entry in self.conversations if entry.session_id == session_id]
    
    def clear_history(self, session_id: Optional[str] = None):
        """Clear conversation history."""
        if session_id:
            # Clear specific session
            self.conversations = [entry for entry in self.conversations if entry.session_id != session_id]
            if session_id in self.sessions:
                del self.sessions[session_id]
        else:
            # Clear all history
            self.conversations = []
            self.sessions = {}
            self.current_session_id = None
        
        self.save_history()
        self.save_sessions()
    
    def export_history(self, filepath: str, session_id: Optional[str] = None) -> bool:
        """Export conversation history to a file."""
        try:
            if session_id:
                conversations = self.get_session_conversations(session_id)
                session_info = self.sessions.get(session_id)
            else:
                conversations = self.conversations
                session_info = None
            
            export_data = {
                "export_timestamp": time.time(),
                "session_info": session_info.to_dict() if session_info else None,
                "conversations": [entry.to_dict() for entry in conversations]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            console.print(f"[red]Error exporting history: {e}[/red]")
            return False
    
    def format_context_for_agent(self, user_input: str, max_context_length: int = 2000) -> str:
        """Format conversation context using semantic similarity search."""
        # First try semantic similarity search
        semantic_context = self.vector_store.get_conversation_context(user_input, max_context_length // 2)
        
        # Also get recent chronological context
        recent_conversations = self.get_recent_context(max_entries=2, hours=1)
        chronological_context = ""
        
        if recent_conversations:
            context_lines = ["=== Recent Conversation Context ==="]
            
            for entry in reversed(recent_conversations):  # Chronological order
                user_text = entry.user_input[:150] + "..." if len(entry.user_input) > 150 else entry.user_input
                ai_text = entry.ai_response[:200] + "..." if len(entry.ai_response) > 200 else entry.ai_response
                
                context_lines.append(f"User: {user_text}")
                context_lines.append(f"Assistant: {ai_text}")
                context_lines.append("---")
            
            chronological_context = "\n".join(context_lines) + "\n=== End Recent Context ===\n\n"
        
        # Combine both contexts
        combined_context = semantic_context + chronological_context
        
        # Trim if too long
        if len(combined_context) > max_context_length:
            combined_context = combined_context[:max_context_length] + "...\n[Context truncated]"
        
        return combined_context
    
    def display_history(self, limit: int = 10, session_id: Optional[str] = None):
        """Display conversation history in a formatted table."""
        if session_id:
            conversations = self.get_session_conversations(session_id)
            title = f"Conversation History - {self.sessions[session_id].name}"
        else:
            conversations = self.conversations
            title = "Conversation History - All Sessions"
        
        if not conversations:
            console.print("[dim]No conversation history found.[/dim]")
            return
        
        # Sort by timestamp (most recent first)
        conversations.sort(key=lambda x: x.timestamp, reverse=True)
        conversations = conversations[:limit]
        
        table = Table(title=title, box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column("Time", style="cyan", width=19)
        table.add_column("Session", style="yellow", width=15)
        table.add_column("User Input", overflow="fold", width=35)
        table.add_column("AI Response", overflow="fold", width=35)
        
        for entry in conversations:
            session_name = self.sessions.get(entry.session_id, {}).name if entry.session_id in self.sessions else "Unknown"
            user_preview = entry.user_input[:60] + "..." if len(entry.user_input) > 60 else entry.user_input
            ai_preview = entry.ai_response[:60] + "..." if len(entry.ai_response) > 60 else entry.ai_response
            
            table.add_row(
                entry.get_formatted_time(),
                session_name[:15],
                user_preview,
                ai_preview
            )
        
        console.print(table)
    
    def display_sessions(self):
        """Display all conversation sessions."""
        if not self.sessions:
            console.print("[dim]No sessions found.[/dim]")
            return
        
        table = Table(title="Conversation Sessions", box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column("ID", style="cyan", width=8)
        table.add_column("Name", style="yellow")
        table.add_column("Created", style="green", width=19)
        table.add_column("Last Activity", style="blue", width=19)
        table.add_column("Current", style="red", width=7)
        
        # Sort by last activity (most recent first)
        sorted_sessions = sorted(self.sessions.values(), key=lambda x: x.last_activity, reverse=True)
        
        for session in sorted_sessions:
            is_current = "Yes" if session.id == self.current_session_id else "No"
            table.add_row(
                session.id[:8],
                session.name,
                session.get_formatted_created_time(),
                datetime.fromtimestamp(session.last_activity).strftime("%Y-%m-%d %H:%M:%S"),
                is_current
            )
        
        console.print(table)
    
    def _sync_with_vector_store(self):
        """Sync existing conversations with vector store."""
        if not self.vector_store.enabled:
            return
        
        # Check if we need to add existing conversations to vector store
        existing_vector_conversations = len(self.vector_store.conversations)
        total_conversations = len(self.conversations)
        
        if existing_vector_conversations < total_conversations:
            console.print(f"[yellow]Syncing {total_conversations - existing_vector_conversations} conversations with vector store...[/yellow]")
            
            for conversation in self.conversations:
                # Only add if not already in vector store
                if conversation.id not in self.vector_store.id_to_vector_id:
                    self.vector_store.add_conversation(
                        conversation_id=conversation.id,
                        session_id=conversation.session_id,
                        user_input=conversation.user_input,
                        ai_response=conversation.ai_response,
                        metadata=conversation.metadata
                    )
            
            console.print("[green]Vector store sync completed![/green]")
    
    def search_similar_conversations(self, query: str, k: int = 5):
        """Search for similar conversations using vector similarity."""
        if not self.vector_store.enabled:
            console.print("[red]Vector search not available. Install: pip install faiss-cpu sentence-transformers[/red]")
            return []
        
        return self.vector_store.search_similar_conversations(query, k)
    
    def display_similar_conversations(self, query: str, k: int = 5):
        """Display similar conversations in a formatted table."""
        self.vector_store.search_and_display_results(query, k)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get conversation history statistics including vector store."""
        total_conversations = len(self.conversations)
        total_sessions = len(self.sessions)
        recent_conversations = len([c for c in self.conversations if c.is_recent(24)])
        
        if self.conversations:
            oldest = min(self.conversations, key=lambda x: x.timestamp)
            newest = max(self.conversations, key=lambda x: x.timestamp)
            oldest_time = datetime.fromtimestamp(oldest.timestamp).strftime("%Y-%m-%d")
            newest_time = datetime.fromtimestamp(newest.timestamp).strftime("%Y-%m-%d")
        else:
            oldest_time = newest_time = "N/A"
        
        # Get vector store stats
        vector_stats = self.vector_store.get_stats()
        
        return {
            "total_conversations": total_conversations,
            "total_sessions": total_sessions,
            "recent_conversations_24h": recent_conversations,
            "oldest_conversation": oldest_time,
            "newest_conversation": newest_time,
            "current_session": self.current_session_id,
            "vector_store": vector_stats
        }
    
    def get_all_conversations(self) -> List[Dict[str, Any]]:
        """Get all conversations as dictionaries for backup purposes."""
        return [entry.to_dict() for entry in self.conversations]
    
    def get_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get all sessions as dictionaries for backup purposes."""
        return {session_id: session.to_dict() for session_id, session in self.sessions.items()}
