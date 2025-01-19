import re
from typing import List, Dict, Pattern
from tiny_pii.types import TinyPIIDetection, TinyPIICategories, TinyPIIDetectors


class RegexDetector:
    """
    PII detector using regex patterns for Singapore-specific identifiers.
    """

    def __init__(self):
        """
        Initialize the detector with regex patterns.

        Args:
            confidence: Confidence score to assign to regex matches (default: 1.0)
        """
        self.confidence = 1  # regex confidence is always 1

        # Compile regex patterns
        self.patterns: Dict[TinyPIICategories, Pattern] = {
            # NRIC pattern: S/T/F/G followed by 7 digits and a letter
            TinyPIICategories.NRIC: re.compile(r"\b[STFG]\d{7}[A-Z]\b", re.IGNORECASE),
            # Singapore phone numbers
            TinyPIICategories.PHONE: re.compile(
                r"(?:(?:\+\s*65|65)[-\s]?)?"  # Optional country code with space after +
                r"(?:[689]\d{3}[-\s]?\d{4})"  # 8 digits with optional separator
                r"\b"
            ),
            # Singapore postal code (6 digits)
            TinyPIICategories._POSTCODE: re.compile(
                r"\b[Ss]?[0-9]{6}\b"
            ),  # with optional S in post code
            # Building/Block numbers
            TinyPIICategories._ADDRESS_COMPONENT: re.compile(
                r"\b(?:(?:BLK|BLOCK|BK)\s*\d+[A-Z]?)|"  # Block number
                r"(?:#?\d{1,2}-\d{1,3}[A-Z]?)|"  # Unit number
                r"(?:B\d{1,2}-\d{1,3}[A-Z]?)"  # Basement unit
                r"\b",
                re.IGNORECASE,
            ),
            TinyPIICategories._ADDRESS_COMPONENT: re.compile(
                r"\b\d{1,4}\b"  # for detecting house number before street name
            ),
            TinyPIICategories.EMAIL: re.compile(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                re.IGNORECASE,
            ),
        }

    def detect(self, text: str) -> List[TinyPIIDetection]:
        """
        Detect PII entities in the given text using regex patterns.

        Args:
            text: Input text to analyze

        Returns:
            List of TinyPIIDetection instances for each detected PII entity
        """
        detections = []

        # Search for each pattern
        for category, pattern in self.patterns.items():
            # Find all matches
            for match in pattern.finditer(text):
                start, end = match.span()
                detection = TinyPIIDetection(
                    detected_class=category,
                    text=match.group(),
                    confidence=self.confidence,
                    position=(start, end),
                    detector=TinyPIIDetectors.REGEX,
                )
                detections.append(detection)

        return sorted(detections, key=lambda x: x.position[0])

    def detect_async(self, text: str) -> List[TinyPIIDetection]:
        """Async version of detect - currently just calls sync version."""
        return self.detect(text)
