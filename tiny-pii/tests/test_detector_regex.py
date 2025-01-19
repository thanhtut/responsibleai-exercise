from tiny_pii.types import TinyPIIDetection, TinyPIICategories, TinyPIIDetectors


def test_detect_phone_building_post(regex_detector, sample_text_jt):
    detections = regex_detector.detect(sample_text_jt)

    print(detections)
    nric_detection = detections[0]
    building_detection = detections[1]
    postcode_detection = detections[2]
    email_detection = detections[3]

    assert nric_detection.detected_class == TinyPIICategories.NRIC
    assert nric_detection.detector == TinyPIIDetectors.REGEX
    assert nric_detection.text == "S1234567E"
    assert nric_detection.position == (74, 83)

    assert building_detection.detected_class == TinyPIICategories._ADDRESS_COMPONENT
    assert building_detection.text == "30"
    assert building_detection.position == (153, 155)

    assert postcode_detection.detected_class == TinyPIICategories._POSTCODE
    assert postcode_detection.text == "S118497"
    assert postcode_detection.position == (178, 185)

    assert email_detection.detected_class == TinyPIICategories.EMAIL
    assert email_detection.text == "john_tan@gmail.com"
    assert email_detection.position == (206, 224)
