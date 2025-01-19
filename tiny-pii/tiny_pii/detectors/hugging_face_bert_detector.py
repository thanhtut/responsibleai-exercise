from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from typing import List
from tiny_pii.types import TinyPIIDetection, TinyPIICategories, TinyPIIDetectors


class HuggingFaceBertDetector:
    """
    PII detector using dslim/bert-base-NER model for detecting names and addresses.
    """

    def __init__(self, model_name: str = "dslim/bert-base-NER", confidence_threshold: float = 0.5):
        """
        Initialize the detector with the specified model.

        Args:
            model_name: Name of the pretrained model to use
            confidence_threshold: Minimum confidence score to consider a detection valid
        """
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold

        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)

        # Create NER pipeline
        self.ner_pipeline = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple",  # Merge subwords
        )

        # Map NER labels to PII categories
        self.label_to_category = {
            "PER": TinyPIICategories.NAME,
            "LOC": TinyPIICategories.ADDRESS,
            "ORG": None,  # We don't use organization detections
        }

    def detect(self, text: str) -> List[TinyPIIDetection]:
        """
        Detect PII entities in the given text.

        Args:
            text: Input text to analyze

        Returns:
            List of TinyPIIDetection instances for each detected PII entity
        """
        # Get NER predictions
        predictions = self.ner_pipeline(text)

        detections = []

        for pred in predictions:
            # Only process if confidence meets threshold and label is mapped
            if (
                pred["score"] >= self.confidence_threshold
                and pred["entity_group"] in self.label_to_category
                and self.label_to_category[pred["entity_group"]] is not None
            ):
                detection = TinyPIIDetection(
                    detected_class=self.label_to_category[pred["entity_group"]],
                    text=pred["word"],
                    confidence=float(pred["score"]),
                    position=(pred["start"], pred["end"]),
                    detector=TinyPIIDetectors.HUGGINGFACE_BERT,
                )
                detections.append(detection)

        return detections

    def detect_async(self, text: str) -> List[TinyPIIDetection]:
        """
        TODO: make it async later on for efficiency.
        """
        return self.detect(text)
