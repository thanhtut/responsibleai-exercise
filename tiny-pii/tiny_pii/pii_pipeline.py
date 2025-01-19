from tiny_pii.detectors import HuggingFaceBertDetector, RegexDetector
from tiny_pii.types import TinyPIIOutput, TinyPIICategories
from tiny_pii.pii_aggreagator import PIIAggregator
from tiny_pii.pii_filter import PIIFilter
from tiny_pii.pii_mask import PIIMasker


class PIIPipeline:
    def __init__(self):
        # TODO: do some clean up and dependency injection
        self.detectors = [HuggingFaceBertDetector(), RegexDetector()]

    def process(self, text: str) -> TinyPIIOutput:
        # run all detectors
        all_detections = []
        for detector in self.detectors:
            all_detections.extend(detector.detect(text))

        aggregated_detections = PIIAggregator.aggregate(all_detections)

        filtered_detections = PIIFilter.filter_and_resolve_overlaps(aggregated_detections)

        masked_text = PIIMasker.mask_text(text, filtered_detections)

        c_name = c_email = c_phone = c_nric = c_address = 0
        for detection in filtered_detections:
            if detection.detected_class == TinyPIICategories.NAME:
                c_name = 1
            elif detection.detected_class == TinyPIICategories.EMAIL:
                c_email = 1
            elif detection.detected_class == TinyPIICategories.PHONE:
                c_phone = 1
            elif detection.detected_class == TinyPIICategories.NRIC:
                c_nric = 1
            elif detection.detected_class == TinyPIICategories.ADDRESS:
                c_address = 1

        return TinyPIIOutput(
            text=text,
            name=c_name,
            email=c_email,
            phone=c_phone,
            nric=c_nric,
            address=c_address,
            detections=filtered_detections,
            redacted_text=masked_text,
        )
