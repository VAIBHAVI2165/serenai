# emotion/emotion_detector.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
labels = model.config.id2label

def detect_emotion(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    confidence = torch.nn.functional.softmax(logits, dim=1)[0][predicted_class_id].item()
    return labels[predicted_class_id], round(confidence, 2)
