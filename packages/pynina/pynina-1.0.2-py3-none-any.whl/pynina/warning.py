from dataclasses import dataclass
from datetime import datetime

@dataclass
class Warning:
    """Dataclass for a warning."""
    id: str
    headline: str
    severity: str
    description: str | None
    sender: str | None
    affected_areas: list[str]
    recommended_actions: list[str]
    web: str | None
    sent: str
    start: str | None
    expires: str | None

    @property
    def is_valid(self) -> bool:
        """Test if warning is valid."""
        if self.expires is not None:
            current_timestamp: float = datetime.now().timestamp()
            expired_timestamp: float = datetime.fromisoformat(self.expires).timestamp()
            return current_timestamp < expired_timestamp
        return True

    def __repr__(self) -> str:
        return (
            f"{self.id} ({self.sent}): [{self.sender}, {self.start} - "
            f"{self.expires} ({self.sent})] {self.headline}, {self.description} - {self.web}"
        )