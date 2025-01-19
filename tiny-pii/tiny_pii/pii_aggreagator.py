from typing import List, Tuple
from copy import deepcopy
from tiny_pii.types import TinyPIIDetection, TinyPIICategories, AggregatedDetection


class PIIAggregator:
    ADDRESS_COMPONENTS = {
        TinyPIICategories._LOCATION,
        TinyPIICategories._ADDRESS_COMPONENT,
        TinyPIICategories._POSTCODE,
        TinyPIICategories.ADDRESS,
    }
    MAX_DISTANCE = 4

    @staticmethod
    def _convert_to_aggregated(detection: TinyPIIDetection) -> AggregatedDetection:
        return AggregatedDetection(
            detected_class=detection.detected_class,
            text=detection.text,
            confidence=detection.confidence,
            position=detection.position,
            detector=detection.detector,
        )

    @staticmethod
    def _can_combine_detections(det1: TinyPIIDetection, det2: TinyPIIDetection) -> bool:
        # Check if detections are close enough
        end_pos_1 = det1.position[1]
        start_pos_2 = det2.position[0]
        distance = start_pos_2 - end_pos_1

        if distance > PIIAggregator.MAX_DISTANCE:
            return False

        # Check if both are address components
        if (
            det1.detected_class in PIIAggregator.ADDRESS_COMPONENTS
            and det2.detected_class in PIIAggregator.ADDRESS_COMPONENTS
        ):
            return True

        return False

    @staticmethod
    def _merge_detections(
        det1: AggregatedDetection, det2: AggregatedDetection
    ) -> AggregatedDetection:
        # Get the text between the detections
        gap_text = " " if det2.position[0] - det1.position[1] > 0 else ""

        # Create merged detection
        return AggregatedDetection(
            detected_class=PIIAggregator._get_merged_class(
                det1.detected_class, det2.detected_class
            ),
            text=det1.text + gap_text + det2.text,
            confidence=min(det1.confidence, det2.confidence),
            position=(det1.position[0], det2.position[1]),
            detector=f"{det1.detector},{det2.detector}",
        )

    @staticmethod
    def _get_merged_class(class1: str, class2: str) -> str:
        if (
            class1 in PIIAggregator.ADDRESS_COMPONENTS
            and class2 in PIIAggregator.ADDRESS_COMPONENTS
        ):
            return TinyPIICategories.ADDRESS
        raise ValueError(f"The classses {class1} - {class2} can't be merged yet.")

    @staticmethod
    def aggregate(detections: List[TinyPIIDetection]) -> List[AggregatedDetection]:
        if not detections:
            return []

        # Sort detections by start position
        sorted_detections = sorted(detections, key=lambda x: x.position[0])
        aggregated = []
        current = sorted_detections[0]

        for next_detection in sorted_detections[1:]:
            if PIIAggregator._can_combine_detections(current, next_detection):
                current = PIIAggregator._merge_detections(
                    PIIAggregator._convert_to_aggregated(current),
                    PIIAggregator._convert_to_aggregated(next_detection),
                )
            else:
                aggregated.append(PIIAggregator._convert_to_aggregated(current))
                current = next_detection

        aggregated.append(PIIAggregator._convert_to_aggregated(current))
        return aggregated
