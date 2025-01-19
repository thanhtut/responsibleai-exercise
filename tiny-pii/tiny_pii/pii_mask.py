from typing import List
from tiny_pii.types import AggregatedDetection, TinyPIICategories


class PIIMasker:
    # Mapping of PII categories to their mask labels
    MASK_LABELS = {
        TinyPIICategories.NAME: "[NAME]",
        TinyPIICategories.EMAIL: "[EMAIL]",
        TinyPIICategories.PHONE: "[PHONE]",
        TinyPIICategories.NRIC: "[NRIC]",
        TinyPIICategories.ADDRESS: "[ADDRESS]",
    }

    @staticmethod
    def mask_text(text: str, detections: List[AggregatedDetection]) -> str:
        """
        Mask PII in text by replacing detected items with their category labels.

        Args:
            text: Original text containing PII
            detections: List of AggregatedDetection objects

        Returns:
            Masked text with PII replaced by category labels
        """
        if not text or not detections:
            return text

        # Sort detections by start position in reverse order
        # This ensures we replace from end to start to maintain position integrity
        sorted_detections = sorted(detections, key=lambda x: x.position[0], reverse=True)

        # Create a list of characters that we can modify
        chars = list(text)

        # Replace each detection with its mask
        for detection in sorted_detections:
            start, end = detection.position
            mask = PIIMasker.MASK_LABELS.get(detection.detected_class)

            if mask:
                # Replace the characters in the detection range with the mask
                chars[start:end] = list(mask)

        return "".join(chars)

    @staticmethod
    def create_masked_pairs(text: str, detections: List[AggregatedDetection]) -> List[tuple]:
        """
        Create pairs of original and masked values for each detection.

        Args:
            text: Original text containing PII
            detections: List of AggregatedDetection objects

        Returns:
            List of tuples containing (original_text, masked_text) for each detection
        """
        pairs = []
        for detection in detections:
            start, end = detection.position
            original = text[start:end]
            masked = PIIMasker.MASK_LABELS.get(detection.detected_class, "[UNKNOWN]")
            pairs.append((original, masked))
        return pairs
