import pytest
from tiny_pii.types import TinyPIICategories, TinyPIIDetectors
from tiny_pii.detectors import HuggingFaceBertDetector


@pytest.fixture
def huggingface_bert_detector():
    """Create a real detector instance."""
    return HuggingFaceBertDetector()
