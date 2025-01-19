from enum import StrEnum


class TinyPIICategories(StrEnum):
    """Enumeration of possible PII categories that can be detected."""

    NAME = "name"
    EMAIL = "email"
    PHONE = "phone"
    NRIC = "nric"
    ADDRESS = "address"
    # The followings are internal categories
    _LOCATION = "_location"  # detected location from NER model
    _POSTCODE = "_postcode"
    _ADDRESS_COMPONENT = "_address component"  # building


class TinyPIIDetectors(StrEnum):
    """Enumeration of available PII detectors."""

    HUGGINGFACE_BERT = "HuggingFaceBertDetector"
    REGEX = "RegexDetector"
