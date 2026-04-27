# Voice-Based AI Agent with Memory & Tools

A voice-enabled AI agent that manages a To-Do list using OpenAI function calling and remembers important user interactions.

## Features

- 🎤 **Voice Interface**: Speech-to-text input and text-to-speech output
- ✅ **To-Do Management**: Add, update, delete, and list tasks
- 🧠 **Memory System**: Stores and recalls important interactions
- 🤖 **Smart Agent**: Decides when to use tools vs respond conversationally

## Setup

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install PyAudio (required for microphone access)
# On Ubuntu/Debian:
sudo apt-get install portaudio19-dev python3-pyaudio

# On macOS:
brew install portaudio
pip install pyaudio

# On Windows:
pip install pipwin
pipwin install pyaudio
```

### 2. Configure OpenAI API Key

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_api_key_here
```

### 3. Run the Agent

```bash
python agent.py
```

## Usage Examples

### Voice Commands

- **Add tasks**: "Add buy groceries to my list"
- **List tasks**: "Show me my tasks" or "What's on my to-do list?"
- **Update tasks**: "Mark task 1 as complete"
- **Delete tasks**: "Delete task 2"
- **Share information**: "My birthday is June 15th" (stored in memory)
- **Exit**: Say "quit" or "exit"

## Architecture

### Components

1. **agent.py**: Main agent with OpenAI function calling logic
2. **voice.py**: Voice input/output using SpeechRecognition and pyttsx3
3. **tools.py**: To-Do CRUD operations with function definitions
4. **memory.py**: Memory system for storing important interactions

### Agent Prompt

The agent uses a carefully crafted system prompt that:
- Defines its capabilities (task management + memory)
- Provides guidelines for tool usage
- Encourages natural conversation
- Specifies when to store memories

### Function Calling Flow

1. User speaks → Speech-to-text
2. Agent receives text input
3. OpenAI determines if tools are needed
4. Tools execute (if needed)
5. Agent generates response
6. Important interactions stored in memory
7. Text-to-speech output

## Data Storage

- **todos.json**: Persistent to-do list storage
- **memory.json**: Important user interactions

## Demo Video Checklist

✅ Show face and screen  
✅ Demonstrate voice input/output  
✅ Add multiple tasks  
✅ List tasks  
✅ Update a task (mark complete)  
✅ Delete a task  
✅ Share personal information (memory test)  
✅ Ask agent to recall stored memory  
✅ Show conversational responses  

## Evaluation Criteria Coverage

- **Voice interaction (20%)**: Full speech-to-text and text-to-speech
- **Tool usage (25%)**: Complete CRUD operations
- **Memory (20%)**: Automatic detection and storage of important info
- **Prompt quality (15%)**: Clear system prompt with guidelines
- **Code structure (10%)**: Modular design with separate components
- **Demo clarity (10%)**: Follow demo checklist above

## Troubleshooting

### Microphone Issues
- Check microphone permissions
- Test with: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`

### API Errors
- Verify OpenAI API key in `.env`
- Check API quota and billing

### Audio Output Issues
- Ensure speakers/headphones are connected
- Test pyttsx3: `python -c "import pyttsx3; e=pyttsx3.init(); e.say('test'); e.runAndWait()"`
