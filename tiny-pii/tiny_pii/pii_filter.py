from typing import List
from tiny_pii.types import TinyPIIDetection, TinyPIICategories


class PIIFilter:
    FINAL_CLASSES = [
        TinyPIICategories.NAME,
        TinyPIICategories.EMAIL,
        TinyPIICategories.PHONE,
        TinyPIICategories.NRIC,
        TinyPIICategories.ADDRESS,
    ]

    @staticmethod
    def filter_and_resolve_overlaps(detections: List[TinyPIIDetection]) -> List[TinyPIIDetection]:
        """
        Filter detections to keep only final classes and resolve position overlaps
        by keeping the detection with longer text.

        Args:
            detections: List of TinyPIIDetection objects

        Returns:
            Filtered list of TinyPIIDetection objects
        """
        # First filter to keep only final classes
        filtered_detections = [d for d in detections if d.detected_class in PIIFilter.FINAL_CLASSES]

        if not filtered_detections:
            return []

        # Sort by start position and then by length (longer text first for same position)
        sorted_detections = sorted(filtered_detections, key=lambda x: (x.position[0], -len(x.text)))

        # Resolve overlaps
        result = []
        current = sorted_detections[0]

        for next_detection in sorted_detections[1:]:
            # Check if there's an overlap
            if PIIFilter._has_overlap(current, next_detection):
                # Keep the one with longer text
                if len(next_detection.text) > len(current.text):
                    current = next_detection
            else:
                result.append(current)
                current = next_detection

        # Add the last detection
        result.append(current)
        return result

    @staticmethod
    def _has_overlap(det1: TinyPIIDetection, det2: TinyPIIDetection) -> bool:
        """
        Check if two detections have overlapping positions.

        Returns:
            bool: True if positions overlap, False otherwise
        """
        return det1.position[0] <= det2.position[1] and det2.position[0] <= det1.position[1]
