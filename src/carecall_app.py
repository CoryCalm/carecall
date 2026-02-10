"""
CareCall Application
Integrates all services together
"""
import asyncio
from typing import Optional, Dict
from datetime import time

from .models.user import User, Contact
from .services.voice_agent import CareCallVoiceAgent
from .services.medication_service import MedicationService, create_demo_medications
from .services.emergency_service import EmergencyService


class CareCallApp:
    """Main CareCall application"""

    def __init__(self, demo_mode: bool = True):
        """
        Initialize CareCall

        Args:
            demo_mode: If True, runs without API keys for testing
        """
        self.demo_mode = demo_mode

        # Initialize services
        self.voice_agent = CareCallVoiceAgent(demo_mode=demo_mode)
        self.medication_service = MedicationService()
        self.emergency_service = EmergencyService()

        # Set up voice agent callbacks
        self.voice_agent.on_transcript = self._handle_transcript
        self.voice_agent.on_command = self._handle_command
        self.voice_agent.on_emergency = self._handle_emergency

        # Current user (in production, would be from database)
        self.current_user = self._create_demo_user()

        # Create demo medications
        create_demo_medications(self.medication_service)

        print("✅ CareCall initialized")

    def _create_demo_user(self) -> User:
        """Create demo user with contacts"""
        user = User(
            id="user_123",
            name="Margaret",
            age=78,
            contacts=[
                Contact(
                    name="Sarah",
                    relationship="daughter",
                    phone="+1-555-0123",
                    email="sarah@example.com",
                    is_emergency=True
                ),
                Contact(
                    name="Dr. Johnson",
                    relationship="doctor",
                    phone="+1-555-0456",
                    email="dr.johnson@clinic.com",
                    is_emergency=True
                ),
                Contact(
                    name="Robert",
                    relationship="son",
                    phone="+1-555-0789",
                    email="robert@example.com",
                    is_emergency=False
                )
            ]
        )
        return user

    async def start(self):
        """Start CareCall"""
        print(f"\n🩺 Starting CareCall for {self.current_user.name}...")
        await self.voice_agent.start_listening()

        # Check for due medications
        self._check_medication_reminders()

    async def stop(self):
        """Stop CareCall"""
        await self.voice_agent.stop_listening()
        print("🛑 CareCall stopped")

    def _handle_transcript(self, transcript: str):
        """Handle voice transcript"""
        print(f"💬 {self.current_user.name}: {transcript}")

    def _handle_command(self, command: Dict):
        """Handle parsed voice command"""
        cmd_type = command["type"]

        if cmd_type == "medication_taken":
            self._handle_medication_taken(command)

        elif cmd_type == "medication_reminder":
            self._handle_medication_reminder()

        elif cmd_type == "make_call":
            self._handle_make_call(command)

        elif cmd_type == "get_weather":
            self._handle_get_weather()

        elif cmd_type == "get_time":
            self._handle_get_time()

        elif cmd_type == "question":
            self._handle_question(command)

    def _handle_medication_taken(self, command: Dict):
        """Handle medication taken confirmation"""
        # Find most recent due medication
        due_meds = self.medication_service.get_medications_due_now(self.current_user.id)

        if due_meds:
            med = due_meds[0]
            # Log it
            self.medication_service.log_medication_taken(
                medication_id=med.id,
                user_id=self.current_user.id,
                scheduled_time=med.times[0]
            )

            response = f"Great! I've logged your {med.name}. Well done staying on schedule!"
            self.voice_agent.respond(response)
        else:
            response = "I don't see any medications due right now. Which one did you take?"
            self.voice_agent.respond(response)

    def _handle_medication_reminder(self):
        """Handle medication reminder request"""
        due_meds = self.medication_service.get_medications_due_now(self.current_user.id)

        if due_meds:
            med = due_meds[0]
            response = f"Yes, it's time for your {med.name}, {med.dosage}."
            if med.instructions:
                response += f" Remember: {med.instructions}"
            self.voice_agent.respond(response)
        else:
            response = "You're all caught up! No medications due right now."
            self.voice_agent.respond(response)

    def _handle_make_call(self, command: Dict):
        """Handle call request"""
        contact_name = command.get("contact_name", "")
        contact = self.current_user.find_contact_by_name(contact_name)

        if contact:
            response = f"Calling {contact.name} now..."
            self.voice_agent.respond(response)
            # In production, would use Twilio to make actual call
            print(f"   📞 Would call {contact.name} at {contact.phone}")
        else:
            response = f"I don't have a contact named {contact_name}. Who would you like to call?"
            self.voice_agent.respond(response)

    def _handle_get_weather(self):
        """Handle weather request"""
        # In production, would call weather API
        response = "It's 68 degrees and sunny today. Great weather for a walk!"
        self.voice_agent.respond(response)

    def _handle_get_time(self):
        """Handle time request"""
        from datetime import datetime
        now = datetime.now()
        response = f"It's {now.strftime('%I:%M %p')}"
        self.voice_agent.respond(response)

    def _handle_question(self, command: Dict):
        """Handle general question"""
        # In production, would use AI to generate response
        response = "I'm not sure about that. Would you like me to call someone who can help?"
        self.voice_agent.respond(response)

    def _handle_emergency(self, transcript: str):
        """Handle emergency detection"""
        # Detect emergency type
        emergency = self.emergency_service.detect_emergency(
            user_id=self.current_user.id,
            transcript=transcript
        )

        if emergency:
            # Respond to user
            response = "I've detected an emergency and I'm alerting your emergency contacts right now. Help is on the way!"
            self.voice_agent.respond(response)

            # Send alerts
            emergency_contacts = self.current_user.get_emergency_contacts()
            self.emergency_service.send_emergency_alert(
                emergency=emergency,
                contacts=emergency_contacts,
                user_name=self.current_user.name
            )

    def _check_medication_reminders(self):
        """Check if any medications are due"""
        due_meds = self.medication_service.get_medications_due_now(self.current_user.id)

        if due_meds:
            for med in due_meds:
                print(f"💊 Reminder: Time to take {med.name} ({med.dosage})")

    def get_status(self) -> Dict:
        """Get current CareCall status"""
        return {
            "user": self.current_user.name,
            "listening": self.voice_agent.is_listening,
            "demo_mode": self.demo_mode,
            "medications_due": len(self.medication_service.get_medications_due_now(self.current_user.id)),
            "active_emergencies": len(self.emergency_service.get_active_emergencies(self.current_user.id)),
            "adherence_rate": f"{self.medication_service.get_adherence_rate(self.current_user.id):.1f}%"
        }


async def demo():
    """Run CareCall demo"""
    app = CareCallApp(demo_mode=True)

    await app.start()

    print("\n" + "="*60)
    print("CARECALL DEMO - Simulated Conversation")
    print("="*60)

    # Morning routine
    await app.voice_agent.simulate_voice_input("Hey CareCall, good morning!")
    await asyncio.sleep(1)

    await app.voice_agent.simulate_voice_input("What time is it?")
    await asyncio.sleep(1)

    await app.voice_agent.simulate_voice_input("Did I take my medicine?")
    await asyncio.sleep(1)

    await app.voice_agent.simulate_voice_input("Yes, I just took my blood pressure pill")
    await asyncio.sleep(1)

    await app.voice_agent.simulate_voice_input("What's the weather?")
    await asyncio.sleep(1)

    # Call someone
    await app.voice_agent.simulate_voice_input("Call my daughter Sarah")
    await asyncio.sleep(1)

    # Emergency scenario
    print("\n" + "="*60)
    print("EMERGENCY SCENARIO")
    print("="*60)

    await app.voice_agent.simulate_voice_input("Help! I fell in the bathroom!")
    await asyncio.sleep(2)

    # Show status
    print("\n" + "="*60)
    print("CARECALL STATUS")
    print("="*60)
    status = app.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    await app.stop()


if __name__ == "__main__":
    asyncio.run(demo())
