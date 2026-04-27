"""To-Do List Management Tools"""
import json
from typing import List, Dict, Optional
from datetime import datetime

class TodoTools:
    def __init__(self, storage_file: str = "todos.json"):
        self.storage_file = storage_file
        self.todos = self._load_todos()
    
    def _load_todos(self) -> List[Dict]:
        """Load todos from file"""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_todos(self):
        """Save todos to file"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.todos, f, indent=2)
    
    def add_todo(self, task: str, priority: str = "medium") -> str:
        """Add a new todo item"""
        todo = {
            "id": len(self.todos) + 1,
            "task": task,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.todos.append(todo)
        self._save_todos()
        return f"Added task #{todo['id']}: {task}"
    
    def list_todos(self, filter_completed: Optional[bool] = None) -> str:
        """List all todos"""
        if not self.todos:
            return "No tasks found."
        
        filtered = self.todos
        if filter_completed is not None:
            filtered = [t for t in self.todos if t['completed'] == filter_completed]
        
        if not filtered:
            status = "completed" if filter_completed else "pending"
            return f"No {status} tasks found."
        
        result = []
        for todo in filtered:
            status = "✓" if todo['completed'] else "○"
            result.append(f"{status} #{todo['id']}: {todo['task']} [{todo['priority']}]")
        return "\n".join(result)
    
    def update_todo(self, task_id: int, task: Optional[str] = None, 
                   priority: Optional[str] = None, completed: Optional[bool] = None) -> str:
        """Update a todo item"""
        for todo in self.todos:
            if todo['id'] == task_id:
                if task:
                    todo['task'] = task
                if priority:
                    todo['priority'] = priority
                if completed is not None:
                    todo['completed'] = completed
                self._save_todos()
                return f"Updated task #{task_id}"
        return f"Task #{task_id} not found"
    
    def delete_todo(self, task_id: int) -> str:
        """Delete a todo item"""
        for i, todo in enumerate(self.todos):
            if todo['id'] == task_id:
                deleted = self.todos.pop(i)
                self._save_todos()
                return f"Deleted task #{task_id}: {deleted['task']}"
        return f"Task #{task_id} not found"
    
    def get_tool_definitions(self):
        """Return OpenAI function definitions"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_todo",
                    "description": "Add a new task to the to-do list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task": {"type": "string", "description": "The task description"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Task priority"}
                        },
                        "required": ["task"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_todos",
                    "description": "List all to-do items, optionally filtered by completion status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "filter_completed": {"type": "boolean", "description": "Filter by completion status"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_todo",
                    "description": "Update an existing to-do item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The ID of the task to update"},
                            "task": {"type": "string", "description": "New task description"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                            "completed": {"type": "boolean", "description": "Mark as completed or not"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_todo",
                    "description": "Delete a to-do item by ID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]
