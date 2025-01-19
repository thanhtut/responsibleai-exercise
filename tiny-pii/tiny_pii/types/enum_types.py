from enum import Enum


class TinyPIICategories(str, Enum):
    """Enumeration of possible PII categories that can be detected."""

    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    NRIC = "nric"
    ADDRESS = "address"
    # The followings are internal categories
    _LOCATION = "location"  # detected location from NER model
    _POSTCODE = "postcode"
    _BUILDING = "building"
    _UNIT = "unit"


class TinyPIIDetectors(str, Enum):
    """Enumeration of available PII detectors."""

    HUGGINGFACE_BERT = "HuggingFaceBertDetector"
    REGEX = "RegexDetector"
