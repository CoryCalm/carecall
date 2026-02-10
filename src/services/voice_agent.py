"""
Deepgram Voice Agent Integration
Handles real-time voice conversation with elderly users
"""
import os
import json
from typing import Optional, Callable, Dict, Any
from datetime import datetime
import asyncio

try:
    from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
    DEEPGRAM_AVAILABLE = True
except ImportError:
    DEEPGRAM_AVAILABLE = False
    print("⚠️  Deepgram SDK not available - running in demo mode")


class CareCallVoiceAgent:
    """Voice agent for CareCall using Deepgram"""

    def __init__(self, api_key: Optional[str] = None, demo_mode: bool = False):
        """
        Initialize voice agent

        Args:
            api_key: Deepgram API key (or set DEEPGRAM_API_KEY env var)
            demo_mode: If True, runs without API key for testing
        """
        self.api_key = api_key or os.getenv('DEEPGRAM_API_KEY')
        self.demo_mode = demo_mode or not self.api_key or not DEEPGRAM_AVAILABLE

        if not self.demo_mode and DEEPGRAM_AVAILABLE:
            self.client = DeepgramClient(self.api_key)
        else:
            self.client = None

        self.connection = None
        self.is_listening = False

        # Callbacks
        self.on_transcript: Optional[Callable] = None
        self.on_command: Optional[Callable] = None
        self.on_emergency: Optional[Callable] = None

    async def start_listening(self):
        """Start listening for voice input"""
        if self.demo_mode:
            print("🎤 [DEMO MODE] Voice agent started")
            self.is_listening = True
            return

        if not DEEPGRAM_AVAILABLE:
            raise RuntimeError("Deepgram SDK not available")

        try:
            # Configure live transcription
            options = LiveOptions(
                model="nova-2",
                language="en-US",
                smart_format=True,
                interim_results=True,
                punctuate=True,
                diarize=False,
            )

            # Create connection
            self.connection = self.client.listen.live.v("1")

            # Set up event handlers
            self.connection.on(LiveTranscriptionEvents.Transcript, self._on_message)
            self.connection.on(LiveTranscriptionEvents.Error, self._on_error)

            # Start connection
            if self.connection.start(options):
                self.is_listening = True
                print("🎤 Voice agent listening...")
            else:
                print("❌ Failed to start voice agent")

        except Exception as e:
            print(f"❌ Error starting voice agent: {e}")
            raise

    async def stop_listening(self):
        """Stop listening"""
        self.is_listening = False

        if self.demo_mode:
            print("🛑 [DEMO MODE] Voice agent stopped")
            return

        if self.connection:
            try:
                self.connection.finish()
            except Exception as e:
                print(f"Error stopping voice agent: {e}")

    def _on_message(self, result, **kwargs):
        """Handle transcription result"""
        try:
            transcript = result.channel.alternatives[0].transcript

            if transcript:
                print(f"💬 Transcript: {transcript}")

                # Call transcript callback
                if self.on_transcript:
                    self.on_transcript(transcript)

                # Check for commands
                command = self._parse_command(transcript)
                if command and self.on_command:
                    self.on_command(command)

                # Check for emergency
                if self._is_emergency(transcript):
                    if self.on_emergency:
                        self.on_emergency(transcript)

        except Exception as e:
            print(f"Error processing message: {e}")

    def _on_error(self, error, **kwargs):
        """Handle errors"""
        print(f"❌ Voice agent error: {error}")

    def _parse_command(self, transcript: str) -> Optional[Dict[str, Any]]:
        """
        Parse voice commands from transcript

        Returns command dict with 'type' and 'params'
        """
        text = transcript.lower().strip()

        # Medication commands
        if "medicine" in text or "medication" in text or "pill" in text:
            if "take" in text or "took" in text:
                return {"type": "medication_taken", "transcript": transcript}
            elif "remind" in text or "time" in text:
                return {"type": "medication_reminder", "transcript": transcript}

        # Call commands
        if "call" in text:
            # Extract name after "call", handling "my [relationship] [name]"
            words = text.split()
            if "call" in words:
                idx = words.index("call")
                if idx + 1 < len(words):
                    # Get everything after "call"
                    remaining = " ".join(words[idx+1:])

                    # Remove common prefixes like "my daughter", "my son", etc.
                    # But keep the relationship if no name follows
                    prefixes_to_remove = [
                        ("my daughter", "daughter"), ("my son", "son"),
                        ("my mom", "mom"), ("my dad", "dad"),
                        ("my wife", "wife"), ("my husband", "husband"),
                        ("my sister", "sister"), ("my brother", "brother"),
                        ("my doctor", "doctor"), ("dr.", ""), ("doctor", "doctor")
                    ]

                    name = remaining
                    for prefix, fallback in prefixes_to_remove:
                        if name.lower().startswith(prefix):
                            extracted = name[len(prefix):].strip()
                            # If nothing after prefix, use the relationship as name
                            name = extracted if extracted else fallback
                            break

                    return {"type": "make_call", "contact_name": name}

        # Weather/time
        if "weather" in text:
            return {"type": "get_weather", "transcript": transcript}

        if "time" in text and "what" in text:
            return {"type": "get_time", "transcript": transcript}

        # General question
        if any(q in text for q in ["what", "when", "where", "who", "how", "why"]):
            return {"type": "question", "transcript": transcript}

        return None

    def _is_emergency(self, transcript: str) -> bool:
        """Detect emergency keywords in transcript"""
        text = transcript.lower()

        emergency_keywords = [
            "help", "emergency", "fell", "fall", "hurt", "pain",
            "can't breathe", "chest pain", "dizzy", "sick",
            "ambulance", "911", "doctor", "hospital"
        ]

        return any(keyword in text for keyword in emergency_keywords)

    async def simulate_voice_input(self, text: str):
        """Simulate voice input for testing (demo mode)"""
        if not self.demo_mode:
            print("⚠️  simulate_voice_input only works in demo mode")
            return

        print(f"🎤 [SIMULATED] User said: \"{text}\"")

        # Simulate transcript callback
        if self.on_transcript:
            self.on_transcript(text)

        # Parse command
        command = self._parse_command(text)
        if command and self.on_command:
            print(f"🎯 Command detected: {command['type']}")
            self.on_command(command)

        # Check emergency
        if self._is_emergency(text):
            print("🚨 EMERGENCY DETECTED!")
            if self.on_emergency:
                self.on_emergency(text)

    def respond(self, message: str):
        """
        Speak response to user (text-to-speech)

        In full implementation, this would use Deepgram TTS
        For now, just prints the response
        """
        print(f"🤖 CareCall: {message}")
        # TODO: Implement Deepgram TTS


# Demo/testing helper
async def demo_conversation():
    """Demo conversation showing CareCall capabilities"""
    agent = CareCallVoiceAgent(demo_mode=True)

    def on_transcript(text):
        print(f"  📝 Transcript: {text}")

    def on_command(cmd):
        print(f"  ✅ Command: {cmd}")

    def on_emergency(text):
        print(f"  🚨 EMERGENCY: {text}")

    agent.on_transcript = on_transcript
    agent.on_command = on_command
    agent.on_emergency = on_emergency

    await agent.start_listening()

    # Simulate conversation
    print("\n" + "="*60)
    print("DEMO CONVERSATION")
    print("="*60 + "\n")

    await agent.simulate_voice_input("Hey CareCall, good morning!")
    await asyncio.sleep(1)

    await agent.simulate_voice_input("Did I take my blood pressure medicine?")
    await asyncio.sleep(1)

    await agent.simulate_voice_input("Yes, I took it just now")
    await asyncio.sleep(1)

    await agent.simulate_voice_input("What's the weather today?")
    await asyncio.sleep(1)

    await agent.simulate_voice_input("Call my daughter Sarah")
    await asyncio.sleep(1)

    await agent.simulate_voice_input("Help! I fell in the bathroom!")
    await asyncio.sleep(1)

    await agent.stop_listening()


if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_conversation())
