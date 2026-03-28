from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from setup import settings


model_path = settings.MODEL_PATH
mapping = {"LABEL_0": "Fake", "LABEL_1": "Real"}


def calculate_credibility_score(verdict, prediction_score):
    return round(prediction_score, 2) if verdict == "real" else (round(1 - prediction_score, 2))


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


def generate_analyst(prediction, keywords, credibility_score):
    words = ", ".join(keywords)

    if credibility_score > 0.80:
        status = "CREDIBLE"
        explanation = (f"The text structure is consistent and professional. "
                f"The neutral tone detected is a strong indicator of verified reporting.")

        status_desc = f"Verified Style Markers : {words}"
    elif 0.40 <= credibility_score <= 0.80:
        status = "MIXED"
        explanation = (f"This text blends factual reporting with a subjective or emotional style. "
                f"There is a risk that the information is biased. ")

        status_desc = f"Terms causing hesitation : {words}"
    else:
        status = "NOT CREDIBLE"
        explanation = (f"The system detected a linguistic signature typical of misinformation, "
                f"often designed to trigger a strong emotional reaction ")

        status_desc = f"Suspicious Keywords Identified : {words}"

    return explanation, status, status_desc