"""
Medication Tracking Service
Manages medications, reminders, and logging
"""
from datetime import datetime, time, timedelta
from typing import List, Optional, Dict
from collections import defaultdict
import uuid

from ..models.medication import Medication, MedicationLog, MedicationFrequency


class MedicationService:
    """Service for managing medications"""

    def __init__(self):
        # In-memory storage (would be database in production)
        self.medications: Dict[str, Medication] = {}
        self.logs: List[MedicationLog] = []

    def add_medication(
        self,
        name: str,
        dosage: str,
        frequency: MedicationFrequency,
        times: List[time],
        instructions: Optional[str] = None
    ) -> Medication:
        """Add a new medication"""
        med_id = str(uuid.uuid4())
        medication = Medication(
            id=med_id,
            name=name,
            dosage=dosage,
            frequency=frequency,
            times=times,
            instructions=instructions
        )
        self.medications[med_id] = medication
        return medication

    def get_medication(self, med_id: str) -> Optional[Medication]:
        """Get medication by ID"""
        return self.medications.get(med_id)

    def list_medications(self) -> List[Medication]:
        """Get all medications"""
        return list(self.medications.values())

    def log_medication_taken(
        self,
        medication_id: str,
        user_id: str,
        scheduled_time: time,
        notes: Optional[str] = None
    ) -> MedicationLog:
        """Log that medication was taken"""
        log_id = str(uuid.uuid4())
        log = MedicationLog(
            id=log_id,
            medication_id=medication_id,
            user_id=user_id,
            taken_at=datetime.now(),
            scheduled_time=scheduled_time,
            confirmed=True,
            notes=notes
        )
        self.logs.append(log)
        return log

    def log_medication_missed(
        self,
        medication_id: str,
        user_id: str,
        scheduled_time: time
    ) -> MedicationLog:
        """Log that medication was missed"""
        log_id = str(uuid.uuid4())
        log = MedicationLog(
            id=log_id,
            medication_id=medication_id,
            user_id=user_id,
            taken_at=datetime.now(),
            scheduled_time=scheduled_time,
            confirmed=False,
            notes="Missed dose"
        )
        self.logs.append(log)
        return log

    def get_medications_due_now(self, user_id: str) -> List[Medication]:
        """Get medications that should be taken soon"""
        now = datetime.now().time()
        current_time_minutes = now.hour * 60 + now.minute

        due_meds = []
        for med in self.medications.values():
            for scheduled_time in med.times:
                scheduled_minutes = scheduled_time.hour * 60 + scheduled_time.minute

                # Within 30 minutes of scheduled time
                if abs(current_time_minutes - scheduled_minutes) <= 30:
                    # Check if already taken today
                    if not self._was_taken_today(med.id, user_id, scheduled_time):
                        due_meds.append(med)
                        break

        return due_meds

    def _was_taken_today(
        self,
        medication_id: str,
        user_id: str,
        scheduled_time: time
    ) -> bool:
        """Check if medication was taken today at scheduled time"""
        today = datetime.now().date()

        for log in reversed(self.logs):  # Check recent logs first
            if (log.medication_id == medication_id and
                log.user_id == user_id and
                log.taken_at.date() == today and
                log.scheduled_time == scheduled_time and
                log.confirmed):
                return True

        return False

    def get_adherence_rate(self, user_id: str, days: int = 7) -> float:
        """
        Calculate medication adherence rate

        Returns percentage (0-100) of medications taken on time
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        total_scheduled = 0
        total_taken = 0

        # Count how many doses were scheduled
        for med in self.medications.values():
            doses_per_day = len(med.times)
            total_scheduled += doses_per_day * days

        # Count how many were actually taken
        for log in self.logs:
            if log.user_id == user_id and log.taken_at >= cutoff_date:
                if log.confirmed:
                    total_taken += 1

        if total_scheduled == 0:
            return 100.0

        return (total_taken / total_scheduled) * 100

    def get_medication_history(
        self,
        user_id: str,
        medication_id: Optional[str] = None,
        days: int = 7
    ) -> List[MedicationLog]:
        """Get medication history"""
        cutoff_date = datetime.now() - timedelta(days=days)

        history = [
            log for log in self.logs
            if log.user_id == user_id and log.taken_at >= cutoff_date
        ]

        if medication_id:
            history = [log for log in history if log.medication_id == medication_id]

        return sorted(history, key=lambda x: x.taken_at, reverse=True)

    def check_missed_medications(self, user_id: str) -> List[Dict]:
        """
        Check for medications that were missed today

        Returns list of missed medications with details
        """
        today = datetime.now().date()
        current_time = datetime.now().time()

        missed = []

        for med in self.medications.values():
            for scheduled_time in med.times:
                # Only check times that have already passed today
                if scheduled_time > current_time:
                    continue

                # Check if it was taken
                if not self._was_taken_today(med.id, user_id, scheduled_time):
                    missed.append({
                        "medication": med,
                        "scheduled_time": scheduled_time,
                        "hours_overdue": self._hours_overdue(scheduled_time)
                    })

        return missed

    def _hours_overdue(self, scheduled_time: time) -> float:
        """Calculate how many hours overdue a medication is"""
        now = datetime.now()
        scheduled_today = datetime.combine(now.date(), scheduled_time)

        if now < scheduled_today:
            return 0.0

        delta = now - scheduled_today
        return delta.total_seconds() / 3600


# Demo data helper
def create_demo_medications(service: MedicationService) -> List[Medication]:
    """Create demo medications for testing"""

    meds = []

    # Blood pressure medication - morning
    meds.append(service.add_medication(
        name="Lisinopril",
        dosage="10mg",
        frequency=MedicationFrequency.ONCE_DAILY,
        times=[time(hour=8, minute=0)],
        instructions="Take with food in the morning"
    ))

    # Blood thinner - morning and evening
    meds.append(service.add_medication(
        name="Warfarin",
        dosage="5mg",
        frequency=MedicationFrequency.TWICE_DAILY,
        times=[time(hour=9, minute=0), time(hour=21, minute=0)],
        instructions="Take at same time each day"
    ))

    # Vitamin D - morning
    meds.append(service.add_medication(
        name="Vitamin D",
        dosage="1000 IU",
        frequency=MedicationFrequency.ONCE_DAILY,
        times=[time(hour=8, minute=30)],
        instructions="Take with breakfast"
    ))

    # Pain reliever - as needed
    meds.append(service.add_medication(
        name="Acetaminophen",
        dosage="500mg",
        frequency=MedicationFrequency.AS_NEEDED,
        times=[time(hour=12, minute=0)],  # Default time
        instructions="Take as needed for pain, max 4 times daily"
    ))

    return meds


if __name__ == "__main__":
    # Demo
    print("🩺 Medication Service Demo\n")

    service = MedicationService()

    # Create demo medications
    meds = create_demo_medications(service)
    print(f"✅ Created {len(meds)} medications")

    # Log some taken
    user_id = "user_123"
    service.log_medication_taken(meds[0].id, user_id, time(8, 0), "Taken with breakfast")
    service.log_medication_taken(meds[1].id, user_id, time(9, 0))
    service.log_medication_missed(meds[2].id, user_id, time(8, 30))

    print(f"\n📊 Adherence Rate: {service.get_adherence_rate(user_id):.1f}%")

    # Check what's due
    due = service.get_medications_due_now(user_id)
    if due:
        print(f"\n💊 Medications due now:")
        for med in due:
            print(f"  - {med.name} ({med.dosage})")
    else:
        print("\n✅ No medications due right now")

    # Check missed
    missed = service.check_missed_medications(user_id)
    if missed:
        print(f"\n⚠️  Missed medications:")
        for item in missed:
            med = item["medication"]
            hours = item["hours_overdue"]
            print(f"  - {med.name}: {hours:.1f} hours overdue")
