"""Voice Input/Output Handler"""
import speech_recognition as sr
import pyttsx3
import threading

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self._setup_voice()
    
    def _setup_voice(self):
        """Configure text-to-speech settings"""
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
    
    def listen(self) -> str:
        """Listen to microphone and convert speech to text"""
        with sr.Microphone() as source:
            print("\n🎤 Listening... (speak now)")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("🔄 Processing...")
                
                text = self.recognizer.recognize_google(audio)
                print(f"📝 You said: {text}")
                return text
            
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"❌ Error: {e}")
                return ""
    
    def speak(self, text: str):
        """Convert text to speech"""
        print(f"\n🤖 Agent: {text}")
        
        # Run TTS in separate thread to avoid blocking
        def _speak():
            self.engine.say(text)
            self.engine.runAndWait()
        
        thread = threading.Thread(target=_speak)
        thread.start()
        thread.join(timeout=10)
