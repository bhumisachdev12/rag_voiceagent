"""Demo AI Agent (works without OpenAI API)"""
import json
from tools import TodoTools
from memory import MemorySystem

class DemoAgent:
    def __init__(self):
        self.tools = TodoTools()
        self.memory = MemorySystem()
    
    def process_message(self, user_input: str) -> str:
        """Process user message with simple pattern matching"""
        user_lower = user_input.lower()
        
        # Add task
        if "add" in user_lower and ("task" in user_lower or "todo" in user_lower or "list" in user_lower or len(user_input.split()) > 1):
            # Extract task description
            parts = user_input.lower().split("add", 1)
            if len(parts) > 1:
                task = parts[1].strip()
                task = task.replace("to my list", "").replace("task", "").replace("todo", "").strip()
                if task:
                    result = self.tools.add_todo(task)
                    return f"Got it! {result}"
            return "What task would you like to add?"
        
        # List tasks
        elif "show" in user_lower or "list" in user_lower or "what" in user_lower:
            if "task" in user_lower or "todo" in user_lower or "list" in user_lower:
                result = self.tools.list_todos()
                return f"Here are your tasks:\n{result}"
        
        # Mark complete
        elif "complete" in user_lower or "done" in user_lower or "finish" in user_lower:
            # Extract task ID
            words = user_input.split()
            task_id = None
            for word in words:
                if word.isdigit():
                    task_id = int(word)
                    break
            
            if task_id:
                result = self.tools.update_todo(task_id, completed=True)
                return f"Great! {result}"
            else:
                return "Which task number should I mark as complete?"
        
        # Delete task
        elif "delete" in user_lower or "remove" in user_lower:
            words = user_input.split()
            task_id = None
            for word in words:
                if word.isdigit():
                    task_id = int(word)
                    break
            
            if task_id:
                result = self.tools.delete_todo(task_id)
                return f"Done! {result}"
            else:
                return "Which task number should I delete?"
        
        # Memory - birthday
        elif "birthday" in user_lower:
            self.memory.add_memory(user_input, "personal")
            return "I'll remember that! Your birthday has been saved."
        
        # Memory - favorites
        elif "favorite" in user_lower or "love" in user_lower:
            self.memory.add_memory(user_input, "preferences")
            return "Noted! I've stored that preference."
        
        # Recall memory
        elif "remember" in user_lower or "recall" in user_lower:
            memories = self.memory.get_recent_memories(5)
            if memories:
                result = "Here's what I remember:\n"
                for mem in memories:
                    result += f"- {mem['content']}\n"
                return result
            else:
                return "I don't have any stored memories yet."
        
        # Default response
        else:
            return "I can help you manage tasks (add, list, complete, delete) and remember important information. What would you like to do?"
    
    def run(self):
        """Main agent loop"""
        print("=" * 60)
        print("🤖 Demo AI Agent (No API Required)")
        print("=" * 60)
        print("\nType your messages (or 'quit' to exit)")
        print("\nExamples:")
        print("  - 'Add buy groceries to my list'")
        print("  - 'Show me my tasks'")
        print("  - 'Mark task 1 as complete'")
        print("  - 'Delete task 2'")
        print("  - 'My birthday is June 15th'")
        print("  - 'Remember what you know'")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🤖 Agent: Goodbye! Have a great day!")
                    break
                
                response = self.process_message(user_input)
                print(f"\n🤖 Agent: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    agent = DemoAgent()
    agent.run()
