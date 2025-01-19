from tiny_pii.types import TinyPIIDetection, TinyPIICategories, TinyPIIDetectors


def test_detect_name_address(huggingface_bert_detector):
    text = (
        "Write me a response to this email: 'Dear Sir/Mdm, this is John Tan (NRIC: S1234567E). "
        "I am writing in to appeal for my parking offence which occurred at 30 Pasir Panjang Road Rd "
        "S118497. Please reach me at john_tan@gmail.com or at +65 91234567."
    )
    detections = huggingface_bert_detector.detect(text)

    name_detection: TinyPIIDetection = detections[0]
    address_detection: TinyPIIDetection = detections[1]

    assert name_detection.detected_class == TinyPIICategories.NAME
    assert name_detection.detector == TinyPIIDetectors.HUGGINGFACE_BERT
    assert name_detection.text == "John Tan"
    assert name_detection.position == (58, 66)

    assert address_detection.detected_class == TinyPIICategories.ADDRESS
    assert address_detection.detector == TinyPIIDetectors.HUGGINGFACE_BERT
    assert address_detection.text == "Pasir Panjang Road Rd"
    assert address_detection.position == (156, 177)
