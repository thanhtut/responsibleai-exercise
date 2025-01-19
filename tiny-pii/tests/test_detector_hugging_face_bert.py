from tiny_pii.types import TinyPIIDetection, TinyPIICategories, TinyPIIDetectors


def test_detect_name_address(huggingface_bert_detector, sample_text_jt):
    detections = huggingface_bert_detector.detect(sample_text_jt)

    name_detection: TinyPIIDetection = detections[0]
    address_detection: TinyPIIDetection = detections[1]

    assert name_detection.detected_class == TinyPIICategories.NAME
    assert name_detection.detector == TinyPIIDetectors.HUGGINGFACE_BERT
    assert name_detection.text == "John Tan"
    assert name_detection.position == (58, 66)

    assert address_detection.detected_class == TinyPIICategories._LOCATION
    assert address_detection.text == "Pasir Panjang Road Rd"
    assert address_detection.position == (156, 177)
