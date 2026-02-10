"""User and Contact models"""
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class Contact:
    """Emergency contact information"""
    name: str
    relationship: str  # "daughter", "son", "doctor", etc.
    phone: str
    email: Optional[str] = None
    is_emergency: bool = False

@dataclass
class User:
    """Elderly user profile"""
    id: str
    name: str
    age: int
    contacts: List[Contact] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def get_emergency_contacts(self) -> List[Contact]:
        """Get all emergency contacts"""
        return [c for c in self.contacts if c.is_emergency]

    def find_contact_by_name(self, name: str) -> Optional[Contact]:
        """Find contact by name (case-insensitive)"""
        name_lower = name.lower()
        for contact in self.contacts:
            if name_lower in contact.name.lower():
                return contact
        return None
