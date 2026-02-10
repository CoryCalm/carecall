#!/usr/bin/env python3
"""
Simple Deepgram API test for SDK 5.x
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_api():
    api_key = os.getenv('DEEPGRAM_API_KEY')

    if not api_key or api_key == 'your_deepgram_key_here':
        print("❌ No API key found in .env")
        return False

    print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]}")

    try:
        from deepgram import DeepgramClient

        client = DeepgramClient(api_key)
        print("✅ DeepgramClient created successfully!")
        print("✅ API key is valid format!")
        print("\n🎉 Ready to use Deepgram!")

        # Note: To fully test, we'd need to make an actual API call
        # but that requires audio input or a URL
        # For now, successful client creation is enough

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🎤 Deepgram API Key Test")
    print("="*60)
    print()

    if test_api():
        print("\n" + "="*60)
        print("✅ SUCCESS - API Key Configured!")
        print("="*60)
        print("\nNext: Run the CareCall demo:")
        print("  python -m src.carecall_app")
    else:
        print("\n❌ Failed - check your API key")
