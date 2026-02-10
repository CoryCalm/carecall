"""Emergency event models"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum

class EmergencyType(Enum):
    """Types of emergency events"""
    FALL = "fall"
    MEDICAL = "medical"
    DISTRESS = "distress"
    HELP_REQUESTED = "help_requested"
    PANIC = "panic"

class EmergencyStatus(Enum):
    """Status of emergency event"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    FALSE_ALARM = "false_alarm"

@dataclass
class Emergency:
    """Emergency event"""
    id: str
    user_id: str
    type: EmergencyType
    status: EmergencyStatus
    detected_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None

    # Voice data
    transcript: Optional[str] = None
    audio_url: Optional[str] = None

    # Detection info
    confidence: float = 1.0  # 0-1, how confident we are this is an emergency
    keywords_detected: list = field(default_factory=list)

    # Response
    contacts_notified: list = field(default_factory=list)
    response_time: Optional[int] = None  # seconds until acknowledged

    def acknowledge(self):
        """Mark emergency as acknowledged"""
        self.status = EmergencyStatus.ACKNOWLEDGED

    def resolve(self):
        """Mark emergency as resolved"""
        self.status = EmergencyStatus.RESOLVED
        self.resolved_at = datetime.now()

    @property
    def is_active(self) -> bool:
        """Check if emergency is still active"""
        return self.status == EmergencyStatus.ACTIVE
