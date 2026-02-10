#!/usr/bin/env python3
"""
Test script to verify Deepgram API connection
Run this first to make sure your API key works!
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_deepgram_connection():
    """Test if Deepgram API key is valid and working"""

    # Check if API key exists
    api_key = os.getenv('DEEPGRAM_API_KEY')

    if not api_key or api_key == 'your_api_key_here':
        print("❌ ERROR: DEEPGRAM_API_KEY not set in .env file!")
        print("\n📝 Quick fix:")
        print("1. Copy .env.example to .env")
        print("2. Get your API key from https://console.deepgram.com/")
        print("3. Add it to .env file")
        return False

    print("🔍 Testing Deepgram API connection...")
    print(f"📌 API Key found: {api_key[:8]}...{api_key[-4:]}")

    try:
        from deepgram import DeepgramClient, PrerecordedOptions

        # Initialize client
        deepgram = DeepgramClient(api_key)

        # Test with a simple audio URL
        AUDIO_URL = "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        print("📡 Making test API call...")
        response = deepgram.listen.rest.v("1").transcribe_url(
            {"url": AUDIO_URL},
            options
        )

        # Check if we got a response
        if response and response.results:
            transcript = response.results.channels[0].alternatives[0].transcript
            print("\n✅ SUCCESS! Deepgram API is working!")
            print(f"📝 Test transcription: '{transcript}'")
            print("\n🎉 You're ready to build CareCall!")
            return True
        else:
            print("❌ Got response but no transcription")
            return False

    except ImportError:
        print("❌ ERROR: deepgram-sdk not installed!")
        print("Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("\n🔧 Possible fixes:")
        print("- Check your API key is correct")
        print("- Make sure you have internet connection")
        print("- Verify your Deepgram account is active")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🩺 CareCall - Deepgram API Connection Test")
    print("=" * 60)
    print()

    success = test_deepgram_connection()

    print()
    print("=" * 60)

    if success:
        print("✅ READY TO BUILD!")
        print("\nNext steps:")
        print("1. Run: uvicorn src.main:app --reload")
        print("2. Open: http://localhost:8000/demo")
        print("3. Start coding the voice agent!")
    else:
        print("❌ SETUP INCOMPLETE")
        print("Fix the errors above and try again")

    print("=" * 60)
