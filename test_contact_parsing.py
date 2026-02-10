"""
Test contact name parsing fix
"""
from src.services.voice_agent import CareCallVoiceAgent

def test_contact_parsing():
    """Test that contact name extraction works correctly"""
    agent = CareCallVoiceAgent(demo_mode=True)

    test_cases = [
        ("call Sarah", "sarah"),
        ("call my daughter Sarah", "sarah"),
        ("call my son Robert", "robert"),
        ("call Dr. Johnson", "johnson"),
        ("call doctor Smith", "smith"),
        ("call my mom", "mom"),
        ("please call Sarah", "sarah"),  # Won't work - "call" not found
        ("can you call my daughter", ""),  # No name after relationship
    ]

    print("🧪 Testing Contact Name Parsing\n")

    passed = 0
    failed = 0

    for transcript, expected in test_cases:
        command = agent._parse_command(transcript)

        if command and command["type"] == "make_call":
            extracted = command["contact_name"].lower().strip()
            success = expected in extracted if expected else False

            if success or (not expected and not extracted):
                print(f"✅ PASS: '{transcript}'")
                print(f"   Extracted: '{command['contact_name']}'")
                passed += 1
            else:
                print(f"❌ FAIL: '{transcript}'")
                print(f"   Expected: '{expected}'")
                print(f"   Got: '{command['contact_name']}'")
                failed += 1
        else:
            if expected:
                print(f"❌ FAIL: '{transcript}' - No call command detected")
                failed += 1
            else:
                print(f"✅ PASS: '{transcript}' - Correctly rejected")
                passed += 1

        print()

    print(f"\n📊 Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    success = test_contact_parsing()
    exit(0 if success else 1)
