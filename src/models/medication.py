"""Medication tracking models"""
from datetime import datetime, time
from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum

class MedicationFrequency(Enum):
    """How often medication should be taken"""
    ONCE_DAILY = "once_daily"
    TWICE_DAILY = "twice_daily"
    THREE_TIMES_DAILY = "three_times_daily"
    AS_NEEDED = "as_needed"
    WEEKLY = "weekly"

@dataclass
class Medication:
    """Medication information"""
    id: str
    name: str
    dosage: str
    frequency: MedicationFrequency
    times: List[time]  # Specific times to take it
    instructions: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class MedicationLog:
    """Record of when medication was taken"""
    id: str
    medication_id: str
    user_id: str
    taken_at: datetime
    scheduled_time: time
    confirmed: bool = True  # False if missed
    notes: Optional[str] = None

    @property
    def was_late(self) -> bool:
        """Check if medication was taken late"""
        scheduled_datetime = datetime.combine(
            self.taken_at.date(),
            self.scheduled_time
        )
        return self.taken_at > scheduled_datetime

    @property
    def minutes_late(self) -> int:
        """How many minutes late was it taken"""
        if not self.was_late:
            return 0
        scheduled_datetime = datetime.combine(
            self.taken_at.date(),
            self.scheduled_time
        )
        delta = self.taken_at - scheduled_datetime
        return int(delta.total_seconds() / 60)
