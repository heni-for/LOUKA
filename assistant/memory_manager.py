#!/usr/bin/env python3
"""
Memory and Context Management for Luca
Handles conversation memory, context persistence, and state management
"""

import json
import sqlite3
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from .config import PROJECT_ROOT

@dataclass
class MemoryItem:
    """Represents a memory item with metadata."""
    id: str
    content: str
    memory_type: str  # 'conversation', 'email', 'draft', 'reminder', 'preference'
    timestamp: float
    metadata: Dict[str, Any]
    importance: float  # 0.0 to 1.0

@dataclass
class ConversationState:
    """Represents current conversation state."""
    current_email: Optional[Dict[str, Any]] = None
    current_draft: Optional[str] = None
    current_sender: Optional[str] = None
    current_subject: Optional[str] = None
    email_list: List[Dict[str, Any]] = None
    current_email_index: int = 0
    last_action: Optional[str] = None
    last_intent: Optional[str] = None
    session_start: float = 0.0
    user_preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.email_list is None:
            self.email_list = []
        if self.user_preferences is None:
            self.user_preferences = {}
        if self.session_start == 0.0:
            self.session_start = time.time()

class MemoryManager:
    """Manages memory and context for Luca."""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or str(PROJECT_ROOT / "luca_memory.db")
        self.conversation_state = ConversationState()
        self.short_term_memory: List[MemoryItem] = []
        self.max_short_term = 50  # Keep last 50 items in memory
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for persistent memory."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create memory table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memory (
                        id TEXT PRIMARY KEY,
                        content TEXT NOT NULL,
                        memory_type TEXT NOT NULL,
                        timestamp REAL NOT NULL,
                        metadata TEXT NOT NULL,
                        importance REAL NOT NULL
                    )
                """)
                
                # Create conversation state table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS conversation_state (
                        id INTEGER PRIMARY KEY,
                        state_data TEXT NOT NULL,
                        timestamp REAL NOT NULL
                    )
                """)
                
                # Create user preferences table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_preferences (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        timestamp REAL NOT NULL
                    )
                """)
                
                conn.commit()
                
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def add_memory(self, content: str, memory_type: str, metadata: Dict[str, Any] = None, importance: float = 0.5) -> str:
        """Add a memory item."""
        memory_id = f"{memory_type}_{int(time.time() * 1000)}"
        
        if metadata is None:
            metadata = {}
        
        memory_item = MemoryItem(
            id=memory_id,
            content=content,
            memory_type=memory_type,
            timestamp=time.time(),
            metadata=metadata,
            importance=importance
        )
        
        # Add to short-term memory
        self.short_term_memory.append(memory_item)
        
        # Keep only recent items in short-term memory
        if len(self.short_term_memory) > self.max_short_term:
            self.short_term_memory = self.short_term_memory[-self.max_short_term:]
        
        # Save to database
        self._save_memory_to_db(memory_item)
        
        return memory_id
    
    def _save_memory_to_db(self, memory_item: MemoryItem):
        """Save memory item to database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO memory 
                    (id, content, memory_type, timestamp, metadata, importance)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    memory_item.id,
                    memory_item.content,
                    memory_item.memory_type,
                    memory_item.timestamp,
                    json.dumps(memory_item.metadata),
                    memory_item.importance
                ))
                conn.commit()
        except Exception as e:
            print(f"Error saving memory to database: {e}")
    
    def get_memories(self, memory_type: Optional[str] = None, limit: int = 10) -> List[MemoryItem]:
        """Get memories from database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if memory_type:
                    cursor.execute("""
                        SELECT id, content, memory_type, timestamp, metadata, importance
                        FROM memory 
                        WHERE memory_type = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """, (memory_type, limit))
                else:
                    cursor.execute("""
                        SELECT id, content, memory_type, timestamp, metadata, importance
                        FROM memory 
                        ORDER BY timestamp DESC
                        LIMIT ?
                    """, (limit,))
                
                memories = []
                for row in cursor.fetchall():
                    memory_item = MemoryItem(
                        id=row[0],
                        content=row[1],
                        memory_type=row[2],
                        timestamp=row[3],
                        metadata=json.loads(row[4]),
                        importance=row[5]
                    )
                    memories.append(memory_item)
                
                return memories
                
        except Exception as e:
            print(f"Error getting memories from database: {e}")
            return []
    
    def search_memories(self, query: str, memory_type: Optional[str] = None, limit: int = 5) -> List[MemoryItem]:
        """Search memories by content."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if memory_type:
                    cursor.execute("""
                        SELECT id, content, memory_type, timestamp, metadata, importance
                        FROM memory 
                        WHERE memory_type = ? AND content LIKE ?
                        ORDER BY importance DESC, timestamp DESC
                        LIMIT ?
                    """, (memory_type, f"%{query}%", limit))
                else:
                    cursor.execute("""
                        SELECT id, content, memory_type, timestamp, metadata, importance
                        FROM memory 
                        WHERE content LIKE ?
                        ORDER BY importance DESC, timestamp DESC
                        LIMIT ?
                    """, (f"%{query}%", limit))
                
                memories = []
                for row in cursor.fetchall():
                    memory_item = MemoryItem(
                        id=row[0],
                        content=row[1],
                        memory_type=row[2],
                        timestamp=row[3],
                        metadata=json.loads(row[4]),
                        importance=row[5]
                    )
                    memories.append(memory_item)
                
                return memories
                
        except Exception as e:
            print(f"Error searching memories: {e}")
            return []
    
    def update_conversation_state(self, state: ConversationState):
        """Update conversation state."""
        self.conversation_state = state
        self._save_conversation_state()
    
    def _save_conversation_state(self):
        """Save conversation state to database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO conversation_state 
                    (id, state_data, timestamp)
                    VALUES (?, ?, ?)
                """, (
                    1,  # Single state record
                    json.dumps(asdict(self.conversation_state)),
                    time.time()
                ))
                conn.commit()
        except Exception as e:
            print(f"Error saving conversation state: {e}")
    
    def load_conversation_state(self) -> ConversationState:
        """Load conversation state from database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT state_data FROM conversation_state 
                    WHERE id = 1
                    ORDER BY timestamp DESC
                    LIMIT 1
                """)
                
                row = cursor.fetchone()
                if row:
                    state_data = json.loads(row[0])
                    self.conversation_state = ConversationState(**state_data)
                else:
                    self.conversation_state = ConversationState()
                
                return self.conversation_state
                
        except Exception as e:
            print(f"Error loading conversation state: {e}")
            return ConversationState()
    
    def set_user_preference(self, key: str, value: Any):
        """Set user preference."""
        self.conversation_state.user_preferences[key] = value
        self._save_user_preference(key, value)
    
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference."""
        return self.conversation_state.user_preferences.get(key, default)
    
    def _save_user_preference(self, key: str, value: Any):
        """Save user preference to database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO user_preferences 
                    (key, value, timestamp)
                    VALUES (?, ?, ?)
                """, (key, json.dumps(value), time.time()))
                conn.commit()
        except Exception as e:
            print(f"Error saving user preference: {e}")
    
    def load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences from database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT key, value FROM user_preferences")
                
                preferences = {}
                for row in cursor.fetchall():
                    preferences[row[0]] = json.loads(row[1])
                
                self.conversation_state.user_preferences = preferences
                return preferences
                
        except Exception as e:
            print(f"Error loading user preferences: {e}")
            return {}
    
    def add_conversation_memory(self, user_input: str, assistant_response: str, intent: str = None):
        """Add conversation to memory."""
        conversation_content = f"User: {user_input}\nAssistant: {assistant_response}"
        metadata = {
            "intent": intent,
            "user_input": user_input,
            "assistant_response": assistant_response
        }
        
        self.add_memory(
            content=conversation_content,
            memory_type="conversation",
            metadata=metadata,
            importance=0.7
        )
    
    def add_email_memory(self, email_data: Dict[str, Any], action: str = None):
        """Add email-related memory."""
        content = f"Email: {email_data.get('subject', 'No subject')} from {email_data.get('sender', 'Unknown')}"
        metadata = {
            "email_data": email_data,
            "action": action,
            "sender": email_data.get("sender"),
            "subject": email_data.get("subject")
        }
        
        self.add_memory(
            content=content,
            memory_type="email",
            metadata=metadata,
            importance=0.8
        )
    
    def add_draft_memory(self, draft_content: str, original_email: Dict[str, Any] = None):
        """Add draft memory."""
        metadata = {
            "original_email": original_email,
            "draft_length": len(draft_content)
        }
        
        self.add_memory(
            content=f"Draft: {draft_content[:100]}...",
            memory_type="draft",
            metadata=metadata,
            importance=0.6
        )
    
    def get_recent_conversations(self, limit: int = 5) -> List[MemoryItem]:
        """Get recent conversations."""
        return self.get_memories("conversation", limit)
    
    def get_recent_emails(self, limit: int = 5) -> List[MemoryItem]:
        """Get recent email memories."""
        return self.get_memories("email", limit)
    
    def get_context_summary(self) -> str:
        """Get a summary of current context."""
        summary = f"Session started: {time.ctime(self.conversation_state.session_start)}\n"
        summary += f"Last action: {self.conversation_state.last_action or 'None'}\n"
        summary += f"Current email: {self.conversation_state.current_subject or 'None'}\n"
        summary += f"Emails in context: {len(self.conversation_state.email_list)}\n"
        summary += f"Recent memories: {len(self.short_term_memory)}\n"
        
        return summary
    
    def clear_old_memories(self, days: int = 30):
        """Clear memories older than specified days."""
        try:
            cutoff_time = time.time() - (days * 24 * 60 * 60)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM memory WHERE timestamp < ?", (cutoff_time,))
                deleted_count = cursor.rowcount
                conn.commit()
                
                print(f"Cleared {deleted_count} old memories")
                return deleted_count
                
        except Exception as e:
            print(f"Error clearing old memories: {e}")
            return 0
    
    def export_memories(self, file_path: str):
        """Export memories to JSON file."""
        try:
            memories = self.get_memories(limit=1000)
            memory_data = [asdict(memory) for memory in memories]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
            
            print(f"Exported {len(memory_data)} memories to {file_path}")
            
        except Exception as e:
            print(f"Error exporting memories: {e}")
    
    def import_memories(self, file_path: str):
        """Import memories from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            imported_count = 0
            for memory_dict in memory_data:
                memory_item = MemoryItem(**memory_dict)
                self._save_memory_to_db(memory_item)
                imported_count += 1
            
            print(f"Imported {imported_count} memories from {file_path}")
            
        except Exception as e:
            print(f"Error importing memories: {e}")


# Global instance
memory_manager = MemoryManager()

def get_memory_manager() -> MemoryManager:
    """Get global memory manager instance."""
    return memory_manager

def add_conversation_memory(user_input: str, assistant_response: str, intent: str = None):
    """Convenience function to add conversation memory."""
    memory_manager.add_conversation_memory(user_input, assistant_response, intent)

def get_recent_context() -> str:
    """Get recent context summary."""
    return memory_manager.get_context_summary()
