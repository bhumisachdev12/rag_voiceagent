"""Test if everything is set up correctly"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Setup Check")
print("=" * 60)

# Check API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_openai_api_key_here":
    print("❌ OpenAI API key not configured")
    print("\nPlease:")
    print("1. Get an API key from: https://platform.openai.com/api-keys")
    print("2. Edit the .env file")
    print("3. Replace 'your_openai_api_key_here' with your actual key")
else:
    print(f"✅ API key found: {api_key[:8]}...{api_key[-4:]}")
    
    # Test OpenAI connection
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        print("\n🔄 Testing OpenAI connection...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'Hello'"}],
            max_tokens=10
        )
        print("✅ OpenAI connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")

print("\n" + "=" * 60)
print("Dependencies Check")
print("=" * 60)

# Check dependencies
deps = {
    "openai": "OpenAI API client",
    "dotenv": "Environment variables",
    "speech_recognition": "Voice input",
    "pyttsx3": "Text-to-speech",
    "pyaudio": "Microphone access"
}

for module, description in deps.items():
    try:
        __import__(module)
        print(f"✅ {module}: {description}")
    except ImportError:
        print(f"❌ {module}: {description} - NOT INSTALLED")

print("\n" + "=" * 60)
