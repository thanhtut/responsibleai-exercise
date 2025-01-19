import pytest
from tiny_pii.types import TinyPIICategories, TinyPIIDetectors, TinyPIIDetection
from tiny_pii.detectors import HuggingFaceBertDetector, RegexDetector


@pytest.fixture
def huggingface_bert_detector():
    """Create a real detector instance."""
    return HuggingFaceBertDetector()


@pytest.fixture
def regex_detector():
    """Create a real detector instance."""
    return RegexDetector()


@pytest.fixture
def sample_text_jt():
    return (
        "Write me a response to this email: 'Dear Sir/Mdm, this is John Tan (NRIC: S1234567E). "
        "I am writing in to appeal for my parking offence which occurred at 30 Pasir Panjang Road Rd "
        "S118497. Please reach me at john_tan@gmail.com or at +65 91234567."
    )


@pytest.fixture
def list_before_aggregation():
    return [
        TinyPIIDetection(
            detected_class=TinyPIICategories.NAME,
            text="John Tan",
            confidence=0.9994800090789795,
            position=(58, 66),
            detector=TinyPIIDetectors.HUGGINGFACE_BERT,
        ),
        TinyPIIDetection(
            detected_class=TinyPIICategories.NRIC,
            text="S1234567E",
            confidence=1.0,
            position=(74, 83),
            detector=TinyPIIDetectors.REGEX,
        ),
        TinyPIIDetection(
            detected_class=TinyPIICategories._ADDRESS_COMPONENT,
            text="30",
            confidence=1.0,
            position=(153, 155),
            detector=TinyPIIDetectors.REGEX,
        ),
        TinyPIIDetection(
            detected_class=TinyPIICategories._LOCATION,
            text="Pasir Panjang Road Rd",
            confidence=0.9739446043968201,
            position=(156, 177),
            detector=TinyPIIDetectors.HUGGINGFACE_BERT,
        ),
        TinyPIIDetection(
            detected_class=TinyPIICategories._POSTCODE,
            text="S118497",
            confidence=1.0,
            position=(178, 185),
            detector=TinyPIIDetectors.REGEX,
        ),
        TinyPIIDetection(
            detected_class=TinyPIICategories.EMAIL,
            text="john_tan@gmail.com",
            confidence=1.0,
            position=(206, 224),
            detector=TinyPIIDetectors.REGEX,
        ),
        TinyPIIDetection(
            detected_class=TinyPIICategories.PHONE,
            text="+65 91234567",
            confidence=1.0,
            position=(231, 243),
            detector=TinyPIIDetectors.REGEX,
        ),
        TinyPIIDetection(
            detected_class=TinyPIICategories._ADDRESS_COMPONENT,
            text="65",
            confidence=1.0,
            position=(232, 234),
            detector=TinyPIIDetectors.REGEX,
        ),
    ]
