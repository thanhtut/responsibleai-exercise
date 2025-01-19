from tiny_pii.pii_aggreagator import PIIAggregator


def test_print(huggingface_bert_detector, regex_detector, sample_text_jt):
    bert_detections = huggingface_bert_detector.detect(sample_text_jt)
    regex_detections = regex_detector.detect(sample_text_jt)

    # all_detections = sorted(bert_detections + regex_detections, key=lambda x: x.position[0])
    all_detection = bert_detections + regex_detections
    aggregated_detections = PIIAggregator.aggregate(all_detection)

    for detection in aggregated_detections:
        print(detection.model_dump_json(indent=2))

    # Filter to make sure only valid labels made it into the final detection and remove overlaps

    aggregated_detections
