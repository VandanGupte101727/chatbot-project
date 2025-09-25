from transformers import pipeline
from sentence_transformers import SentenceTransformer
from langdetect import detect, LangDetectError

class IntentClassifier:
    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
        self.candidate_labels = [
            "fee deadline", "scholarship form", "exam timetable", 
            "library hours", "admission process", "course registration"
        ]
    
    def classify_intent(self, text):
        try:
            result = self.classifier(
                text,
                candidate_labels=self.candidate_labels,
                hypothesis_template="This text is about {}."
            )
            return result['labels'][0], result['scores'][0]
        except:
            return "general", 0.5

class MultilingualTranslator:
    def detect_language(self, text):
        try:
            return detect(text)
        except LangDetectError:
            return "en"