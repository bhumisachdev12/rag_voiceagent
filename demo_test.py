"""Automated demo of the agent"""
from agent_demo import DemoAgent

agent = DemoAgent()

print("=" * 60)
print("🎬 AUTOMATED DEMO")
print("=" * 60)

# Test cases
test_inputs = [
    "Add buy groceries to my list",
    "Add finish assignment",
    "Add call mom",
    "Show me my tasks",
    "Mark task 1 as complete",
    "Show me my tasks",
    "My birthday is June 15th",
    "My favorite color is blue",
    "Remember what you know",
    "Delete task 2",
    "Show me my tasks"
]

for user_input in test_inputs:
    print(f"\n👤 You: {user_input}")
    response = agent.process_message(user_input)
    print(f"🤖 Agent: {response}")
    print("-" * 60)

print("\n✅ Demo completed!")
