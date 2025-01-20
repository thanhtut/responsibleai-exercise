from pydantic import BaseModel, Field
from tiny_pii.types import TinyPIICategories, TinyPIIDetectors
from typing import List, Tuple, Literal, Union


class TinyPIIDetection(BaseModel):
    """Model representing a single PII detection instance."""

    detected_class: TinyPIICategories
    text: str
    confidence: float = Field(ge=0.0, le=1.0)  # Ensures confidence is between 0 and 1
    position: Tuple[int, int]
    detector: Union[TinyPIIDetectors | str]

    class Config:
        from_attributes = True


class AggregatedDetection(TinyPIIDetection):
    detector: str  # a str since all labels will be combined


class TinyPIIOutput(BaseModel):
    """Model representing the complete output of PII detection."""

    text: str
    name: Literal[0, 1]
    email: Literal[0, 1]
    phone: Literal[0, 1]
    nric: Literal[0, 1]
    address: Literal[0, 1]
    detections: List[TinyPIIDetection] = Field(default_factory=list)  # default is empty list
    redacted_text: str

    class Config:
        from_attributes = True
