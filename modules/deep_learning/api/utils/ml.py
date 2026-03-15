from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from setup import settings


model_path = settings.MODEL_PATH
mapping = {"LABEL_0": "Fake", "LABEL_1": "Real"}


def get_tools():
    classifier = pipeline(
        "text-classification",
        model=model_path,
        tokenizer=model_path
    )

    # For XAI
    model = AutoModelForSequenceClassification.from_pretrained(model_path)

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    return classifier, model, tokenizer


def extract_keywords(explanation, threshold=0.05, top_k=5):
    words = [
        word for word, score in explanation
        if abs(score) > threshold and word not in ["[CLS]", "[SEP]"]
    ]
    return words[:top_k]


def generate_explanation(prediction, keywords):
    words = ", ".join(keywords)

    if prediction == "REAL":
        return f"This news as REAL because the text contains informative terms such as ( {words} ), which are commonly found in verified news articles."
    else:
        return f"This news as FAKE because certain expressions such as ( {words} ) resemble patterns often found in misleading or unreliable content."