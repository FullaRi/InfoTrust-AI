from flask import flash, request
from flaskr.core import bp
from transformers_interpret import SequenceClassificationExplainer
import logging
from marshmallow import ValidationError
from setup import settings
from . import schemas
from utils import ml

logger = logging.getLogger(__name__)

model_path = settings.MODEL_PATH



# For Prediction
classifier, c_model, c_tokenizer = ml.get_tools()
cls_explainer = SequenceClassificationExplainer(c_model, c_tokenizer)



@bp.route('/')
def home():
    return {"service": "online"}, 200


@bp.route('/predict', methods=['POST'])
def predict():
    if not request.is_json:
        return {"message": "Impossible de traiter la requête"}, 400

    try:
        schema = schemas.PredictionSchema(many=False)
        validated_data = schema.load(request.get_json())
    except ValidationError as err:
        return {"message": "invalid form"}, 400
    except Exception as e:
        logger.exception("API / prediction error : ")
        return {"message": "Impossible de traiter la requête"}, 500


    # 'prediction_full' : [[{'label': 'Fake', 'score': 0.02}, {'label': 'Real', 'score': 0.98}]]
    # prediction_full = classifier(
    #     request.form['text'],
    #     truncation=True,
    #     max_length=512,
    #     top_k=None
    # )

    # prediction exemple : [{'label': 'Fake', 'score': 0.9854}]
    prediction = classifier(
        validated_data['user_input'],
        truncation=True
    )

    word_attributions = cls_explainer(validated_data['user_input'])
    keywords = ml.extract_keywords(word_attributions)
    explanation_message = ml.generate_explanation(prediction[0]['label'].lower(), keywords)

    return {
        "user_input": validated_data['user_input'],
        "verdict": prediction[0]['label'].lower(),
        "score": round(prediction[0]['score'] * 100, 2),
        "explanation": {
            "xai_word_attributions": word_attributions,
            "keywords": keywords,
            "message": explanation_message
        }
    }