"""
Data models for PhD positions.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List
from datetime import datetime
import json


@dataclass
class PhDPosition:
    """
    Data class representing a PhD position.
    
    Attributes:
        title: The title of the PhD position
        university: The university/employer offering the position
        location: City and country where the position is based
        country: Country of the position
        city: City of the position
        deadline: Application deadline
        published_date: When the position was published
        job_type: Type of position (PhD, Postdoc, etc.)
        fields: Research fields/disciplines
        description: Full job description
        requirements: List of requirements/qualifications
        benefits: What the position offers
        url: Direct link to the job posting
        apply_url: Direct application link
        employer_url: Link to employer page
        scraped_at: Timestamp when the data was scraped
    """
    title: str
    university: str
    location: str = ""
    country: str = ""
    city: str = ""
    deadline: str = ""
    published_date: str = ""
    job_type: str = "PhD"
    fields: List[str] = field(default_factory=list)
    description: str = ""
    requirements: str = ""
    benefits: str = ""
    url: str = ""
    apply_url: str = ""
    employer_url: str = ""
    scraped_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        """Convert the position to a dictionary."""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """Convert the position to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: dict) -> "PhDPosition":
        """Create a PhDPosition from a dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        parts = [
            f"Title: {self.title}",
            f"University: {self.university}",
            f"Location: {self.location}" if self.location else None,
            f"Deadline: {self.deadline}" if self.deadline else None,
            f"Fields: {', '.join(self.fields)}" if self.fields else None,
            f"URL: {self.url}" if self.url else None,
        ]
        return "\n".join(p for p in parts if p)
    
    def summary(self) -> str:
        """Return a brief summary of the position."""
        deadline_info = f" (Deadline: {self.deadline})" if self.deadline else ""
        return f"{self.title} at {self.university}{deadline_info}"
