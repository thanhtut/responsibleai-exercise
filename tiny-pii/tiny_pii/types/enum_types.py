from enum import Enum


class TinyPIICategories(str, Enum):
    """Enumeration of possible PII categories that can be detected."""

    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    NRIC = "nric"
    ADDRESS = "address"


class TinyPIIDetectors(str, Enum):
    """Enumeration of available PII detectors."""

    HUGGINGFACE_BERT = "HuggingFaceBertDetector"
    REGEX = "RegexDetector"
