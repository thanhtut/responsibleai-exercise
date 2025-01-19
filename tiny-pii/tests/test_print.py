from tiny_pii.pii_aggreagator import PIIAggregator
from tiny_pii.pii_filter import PIIFilter
from tiny_pii.pii_mask import PIIMasker


def test_print(huggingface_bert_detector, regex_detector, sample_text_jt):
    bert_detections = huggingface_bert_detector.detect(sample_text_jt)
    regex_detections = regex_detector.detect(sample_text_jt)

    # all_detections = sorted(bert_detections + regex_detections, key=lambda x: x.position[0])
    all_detection = bert_detections + regex_detections
    aggregated_detections = PIIAggregator.aggregate(all_detection)

    aggregated = PIIAggregator.aggregate(list_before_aggregation)
    assert len(aggregated) == 6

    filtered = PIIFilter.filter_and_resolve_overlaps(aggregated)
    assert len(filtered) == 5
    print(filtered)

    masked = PIIMasker.mask_text(sample_text_jt, filtered)
    print(masked)
