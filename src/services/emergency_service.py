"""
Emergency Detection and Alert Service
Detects emergencies and notifies contacts
"""
from datetime import datetime
from typing import List, Optional, Dict
import uuid
import re

from ..models.emergency import Emergency, EmergencyType, EmergencyStatus
from ..models.user import User, Contact


class EmergencyService:
    """Service for handling emergencies"""

    # Keywords that indicate different emergency types
    EMERGENCY_PATTERNS = {
        EmergencyType.FALL: [
            r"\bfell\b", r"\bfall\b", r"\bfalling\b", r"\btrip\b", r"\bslip\b"
        ],
        EmergencyType.MEDICAL: [
            r"\bchest pain\b", r"\bcan'?t breathe\b", r"\bheart\b",
            r"\bdizzy\b", r"\bnausea\b", r"\bvomit\b", r"\bbleeding\b"
        ],
        EmergencyType.DISTRESS: [
            r"\bscared\b", r"\bworried\b", r"\banxious\b", r"\bpanic\b"
        ],
        EmergencyType.HELP_REQUESTED: [
            r"\bhelp\b", r"\bemer gency\b", r"\b911\b", r"\bambulance\b",
            r"\bdoctor\b", r"\bhospital\b"
        ]
    }

    def __init__(self):
        self.emergencies: Dict[str, Emergency] = {}
        self.alert_callbacks = []  # Functions to call when emergency detected

    def detect_emergency(
        self,
        user_id: str,
        transcript: str,
        audio_url: Optional[str] = None
    ) -> Optional[Emergency]:
        """
        Analyze transcript for emergency keywords

        Returns Emergency object if detected, None otherwise
        """
        text = transcript.lower()

        # Check each emergency type
        for emergency_type, patterns in self.EMERGENCY_PATTERNS.items():
            keywords_found = []
            confidence = 0.0

            for pattern in patterns:
                if re.search(pattern, text):
                    keywords_found.append(pattern)
                    confidence += 0.3  # Increase confidence for each match

            # If we found keywords, create emergency
            if keywords_found:
                confidence = min(confidence, 1.0)  # Cap at 1.0

                emergency = self.create_emergency(
                    user_id=user_id,
                    emergency_type=emergency_type,
                    transcript=transcript,
                    audio_url=audio_url,
                    confidence=confidence,
                    keywords=keywords_found
                )

                # Trigger alerts
                self._trigger_alerts(emergency)

                return emergency

        return None

    def create_emergency(
        self,
        user_id: str,
        emergency_type: EmergencyType,
        transcript: Optional[str] = None,
        audio_url: Optional[str] = None,
        confidence: float = 1.0,
        keywords: Optional[List[str]] = None
    ) -> Emergency:
        """Create a new emergency event"""
        emergency_id = str(uuid.uuid4())

        emergency = Emergency(
            id=emergency_id,
            user_id=user_id,
            type=emergency_type,
            status=EmergencyStatus.ACTIVE,
            transcript=transcript,
            audio_url=audio_url,
            confidence=confidence,
            keywords_detected=keywords or []
        )

        self.emergencies[emergency_id] = emergency
        return emergency

    def get_emergency(self, emergency_id: str) -> Optional[Emergency]:
        """Get emergency by ID"""
        return self.emergencies.get(emergency_id)

    def get_active_emergencies(self, user_id: Optional[str] = None) -> List[Emergency]:
        """Get all active emergencies, optionally filtered by user"""
        emergencies = [
            e for e in self.emergencies.values()
            if e.status == EmergencyStatus.ACTIVE
        ]

        if user_id:
            emergencies = [e for e in emergencies if e.user_id == user_id]

        return sorted(emergencies, key=lambda x: x.detected_at, reverse=True)

    def acknowledge_emergency(self, emergency_id: str) -> bool:
        """Acknowledge an emergency (family member responded)"""
        emergency = self.emergencies.get(emergency_id)
        if not emergency:
            return False

        emergency.acknowledge()

        # Calculate response time
        response_delta = datetime.now() - emergency.detected_at
        emergency.response_time = int(response_delta.total_seconds())

        return True

    def resolve_emergency(self, emergency_id: str) -> bool:
        """Mark emergency as resolved"""
        emergency = self.emergencies.get(emergency_id)
        if not emergency:
            return False

        emergency.resolve()
        return True

    def mark_false_alarm(self, emergency_id: str) -> bool:
        """Mark emergency as false alarm"""
        emergency = self.emergencies.get(emergency_id)
        if not emergency:
            return False

        emergency.status = EmergencyStatus.FALSE_ALARM
        return True

    def _trigger_alerts(self, emergency: Emergency):
        """Send alerts to emergency contacts"""
        print(f"\n🚨 EMERGENCY ALERT!")
        print(f"   Type: {emergency.type.value}")
        print(f"   Confidence: {emergency.confidence:.0%}")
        print(f"   Message: {emergency.transcript}")
        print(f"   Time: {emergency.detected_at.strftime('%I:%M %p')}")

        # Call registered callbacks
        for callback in self.alert_callbacks:
            try:
                callback(emergency)
            except Exception as e:
                print(f"   Error in alert callback: {e}")

        # In production, would send SMS/email/push notifications here
        print(f"   📱 Would notify emergency contacts")

    def register_alert_callback(self, callback):
        """Register a function to be called when emergency is detected"""
        self.alert_callbacks.append(callback)

    def send_emergency_alert(
        self,
        emergency: Emergency,
        contacts: List[Contact],
        user_name: str
    ):
        """
        Send emergency alert to contacts

        In production, would use Twilio SMS/calls
        For demo, just logs the alert
        """
        for contact in contacts:
            message = self._create_alert_message(emergency, user_name)
            print(f"\n📱 SMS to {contact.name} ({contact.phone}):")
            print(f"   {message}")

            # Track that contact was notified
            if contact.name not in emergency.contacts_notified:
                emergency.contacts_notified.append(contact.name)

    def _create_alert_message(self, emergency: Emergency, user_name: str) -> str:
        """Create alert message for emergency"""
        type_messages = {
            EmergencyType.FALL: "may have fallen",
            EmergencyType.MEDICAL: "is experiencing a medical emergency",
            EmergencyType.DISTRESS: "is in distress",
            EmergencyType.HELP_REQUESTED: "is requesting help"
        }

        situation = type_messages.get(emergency.type, "needs help")

        message = f"🚨 ALERT: {user_name} {situation}. "

        if emergency.transcript:
            message += f"They said: \"{emergency.transcript[:100]}\""

        message += f" Time: {emergency.detected_at.strftime('%I:%M %p')}. "
        message += "Please check on them immediately."

        return message


# Demo
def demo_emergency_detection():
    """Demo emergency detection"""
    print("🚨 Emergency Detection Demo\n")

    service = EmergencyService()

    # Test different emergency types
    test_cases = [
        "Help! I fell in the bathroom and I can't get up!",
        "I'm having chest pain and can't breathe well",
        "I'm feeling really dizzy and nauseous",
        "Can you call my doctor? I need help",
        "What's the weather like today?",  # Not an emergency
        "I slipped on the floor but I'm okay now"
    ]

    for transcript in test_cases:
        print(f"\n📝 Test: \"{transcript}\"")
        emergency = service.detect_emergency("user_123", transcript)

        if emergency:
            print(f"   🚨 EMERGENCY DETECTED!")
            print(f"   Type: {emergency.type.value}")
            print(f"   Confidence: {emergency.confidence:.0%}")
            print(f"   Keywords: {emergency.keywords_detected[:3]}")
        else:
            print(f"   ✅ No emergency detected")


if __name__ == "__main__":
    demo_emergency_detection()
