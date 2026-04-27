"""Memory System for storing important user interactions"""
import json
from typing import List, Dict
from datetime import datetime

class MemorySystem:
    def __init__(self, storage_file: str = "memory.json"):
        self.storage_file = storage_file
        self.memories = self._load_memories()
    
    def _load_memories(self) -> List[Dict]:
        """Load memories from file"""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_memories(self):
        """Save memories to file"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.memories, f, indent=2)
    
    def add_memory(self, content: str, category: str = "general"):
        """Store an important interaction"""
        memory = {
            "id": len(self.memories) + 1,
            "content": content,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
        self.memories.append(memory)
        self._save_memories()
    
    def get_recent_memories(self, limit: int = 5) -> List[Dict]:
        """Get recent memories"""
        return self.memories[-limit:] if self.memories else []
    
    def search_memories(self, keyword: str) -> List[Dict]:
        """Search memories by keyword"""
        return [m for m in self.memories if keyword.lower() in m['content'].lower()]
    
    def get_context_summary(self) -> str:
        """Get a summary of recent memories for context"""
        recent = self.get_recent_memories(3)
        if not recent:
            return "No previous interactions stored."
        
        summary = "Recent important interactions:\n"
        for mem in recent:
            summary += f"- {mem['content']}\n"
        return summary
