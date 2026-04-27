"""Main AI Agent with Function Calling"""
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from voice import VoiceHandler
from tools import TodoTools
from memory import MemorySystem

load_dotenv()

class VoiceAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.voice = VoiceHandler()
        self.tools = TodoTools()
        self.memory = MemorySystem()
        self.conversation_history = []
        
        # System prompt defining agent behavior
        self.system_prompt = """You are a helpful voice-based AI assistant that manages to-do lists and remembers important user interactions.

Your capabilities:
1. Manage to-do items (add, update, delete, list)
2. Remember important events and information the user shares
3. Have natural conversations

Guidelines:
- Use tools when the user wants to manage tasks
- Store important personal information in memory (birthdays, preferences, events)
- Be conversational and friendly
- Keep responses concise for voice interaction
- When listing tasks, summarize if there are many

When the user shares something important (like "my birthday is June 15" or "I love pizza"), acknowledge it and remember it."""
    
    def _execute_function(self, function_name: str, arguments: dict) -> str:
        """Execute the requested function"""
        if function_name == "add_todo":
            return self.tools.add_todo(**arguments)
        elif function_name == "list_todos":
            return self.tools.list_todos(**arguments)
        elif function_name == "update_todo":
            return self.tools.update_todo(**arguments)
        elif function_name == "delete_todo":
            return self.tools.delete_todo(**arguments)
        else:
            return f"Unknown function: {function_name}"
    
    def _should_remember(self, user_input: str, assistant_response: str) -> bool:
        """Determine if this interaction should be stored in memory"""
        memory_keywords = [
            "birthday", "anniversary", "favorite", "love", "hate", "prefer",
            "remember", "important", "meeting", "appointment", "event"
        ]
        combined = (user_input + " " + assistant_response).lower()
        return any(keyword in combined for keyword in memory_keywords)
    
    def process_message(self, user_input: str) -> str:
        """Process user message with function calling"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Prepare messages with system prompt and memory context
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"Memory context: {self.memory.get_context_summary()}"}
        ] + self.conversation_history[-10:]  # Keep last 10 messages
        
        # Call OpenAI with function calling
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=self.tools.get_tool_definitions(),
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # Handle function calls
        if assistant_message.tool_calls:
            # Add assistant message with tool calls to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in assistant_message.tool_calls
                ]
            })
            
            # Execute each function call
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                print(f"🔧 Calling function: {function_name}({arguments})")
                result = self._execute_function(function_name, arguments)
                
                # Add function result to history
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Get final response after function execution
            final_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt}
                ] + self.conversation_history[-10:]
            )
            
            final_text = final_response.choices[0].message.content
        else:
            final_text = assistant_message.content
        
        # Add final response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": final_text
        })
        
        # Check if we should remember this interaction
        if self._should_remember(user_input, final_text):
            memory_content = f"User: {user_input} | Agent: {final_text}"
            self.memory.add_memory(memory_content)
            print("💾 Stored in memory")
        
        return final_text
    
    def run(self):
        """Main agent loop"""
        print("=" * 60)
        print("🎙️  Voice-Based AI Agent with Memory & Tools")
        print("=" * 60)
        print("\nCommands:")
        print("  - Speak naturally to manage tasks")
        print("  - Say 'quit' or 'exit' to stop")
        print("  - Press Ctrl+C to force quit")
        print("\nExamples:")
        print("  - 'Add buy groceries to my list'")
        print("  - 'Show me my tasks'")
        print("  - 'Mark task 1 as complete'")
        print("  - 'My birthday is June 15th'")
        print("=" * 60)
        
        self.voice.speak("Hello! I'm your AI assistant. How can I help you today?")
        
        while True:
            try:
                # Listen for voice input
                user_input = self.voice.listen()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'goodbye', 'bye']:
                    self.voice.speak("Goodbye! Have a great day!")
                    break
                
                # Process the message
                response = self.process_message(user_input)
                
                # Speak the response
                self.voice.speak(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                self.voice.speak("Sorry, I encountered an error. Please try again.")

if __name__ == "__main__":
    agent = VoiceAgent()
    agent.run()
