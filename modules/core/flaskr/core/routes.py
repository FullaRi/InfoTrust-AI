from flask import send_file, request
from flaskr.core import bp
import logging
import json
import os
from marshmallow import ValidationError
import requests
import time
from datetime import timedelta
from setup import settings
from . import schemas
from utils import ml
from utils.api import DeepLearningServiceApi, AiAgentServiceApi

logger = logging.getLogger(__name__)


@bp.route('/')
def home():
    return {"service infotrustai core": "online"}, 200

@bp.route('/fake-news-detection', methods=['POST'])
def fake_news_detection():
    start_time = time.perf_counter()

    if not request.is_json:
        return {"message": "The request could not be processed. Please try again later."}, 400

    try:
        schema = schemas.FactCheckingSchema(many=False)
        validated_data = schema.load(request.get_json())
    except ValidationError as err:
        return {"message": "invalid form"}, 400
    except Exception as e:
        logger.exception("API / prediction error : ")
        return {"message": "The request could not be processed. Please try again later."}, 500

    detection_type = validated_data['detection_type']
    deep_learning_data = None
    ai_agent_data = None

    if detection_type in [ml.DETECTION_TYPE_DEEP_LEARNING, ml.DETECTION_TYPE_AI_AGENT__DEEP_LEARNING]:
        try:
            deep_learning_data = DeepLearningServiceApi.predict(validated_data['user_input'])
        except requests.exceptions.HTTPError as errh:
            logger.exception("API / deep learning error http")
            content_type = errh.response.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                error_msg = errh.response.json()
                if error_msg['message']:
                    return {"message": error_msg['message']}, 400

            return {"message": "The request could not be processed. Please try again later."}, 400
        except requests.exceptions.Timeout:
            logger.exception("API / deep learning error timeout")
            return {"message": "The request could not be processed. Please try again later."}, 500
        except Exception:
            logger.exception("API / deep learning error : ")
            return {"message": "The request could not be processed. Please try again later."}, 500

    if detection_type in [ml.DETECTION_TYPE_AI_AGENT, ml.DETECTION_TYPE_AI_AGENT__DEEP_LEARNING]:
        try:
            ai_agent_data = AiAgentServiceApi.predict(validated_data['user_input'])
        except requests.exceptions.HTTPError as errh:
            logger.exception("API / ai agent error http")
            content_type = errh.response.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                error_msg = errh.response.json()
                if error_msg:
                    # INVALID_INPUT - LLM_ERROR -
                    error_type = error_msg['type']

                    if error_type == 'INVALID_INPUT':
                        return {"message": "The provided text does not appear to be a news article. Please submit a valid news or informational content. (Max length: 400 characters, Min length: 10 characters)"}, 400

            return {"message": "The request could not be processed. Please try again later."}, 500
        except requests.exceptions.Timeout:
            logger.exception("API / ai agent error timeout")
            return {"message": "The request could not be processed. Please try again later."}, 500
        except Exception:
            logger.exception("API / ai agent error : ")
            return {"message": "The request could not be processed. Please try again later."}, 500

    api_response = {
        "detection_type": "",
        'final_decision': "",
        'credibility_score': "",
        'explanation': "",
        'sources_for_investigation': [],
        'status': "",
        'status_description': "",
    }

    if detection_type == ml.DETECTION_TYPE_DEEP_LEARNING:
        api_response['detection_type'] = detection_type
        api_response['final_decision'] = deep_learning_data['verdict']
        api_response['credibility_score'] = deep_learning_data['credibility_score'] * 100
        api_response['explanation'] = deep_learning_data['explanation']['message']
        api_response['sources_for_investigation'] = []
        api_response['status'] = deep_learning_data['status'] # CREDIBLE - MIXED - NOT CREDIBLE
        api_response['status_description'] = deep_learning_data['status_description']

    elif detection_type == ml.DETECTION_TYPE_AI_AGENT:

        status_data = ml.get_investigation_web_status(ai_agent_data)

        api_response['detection_type'] = detection_type
        api_response['final_decision'] = ai_agent_data['final_decision']
        api_response['credibility_score'] = 100 *  ai_agent_data['credibility_score']
        api_response['explanation'] = ai_agent_data['final_justification']
        api_response['sources_for_investigation'] = ai_agent_data['sources_for_investigation']
        api_response['status'] = status_data[0] #  HIGHLY CREDIBLE - MODERATELY CREDIBLE - LOW CREDIBILITY - VERY LIKELY FAKE - UNVERIFIABLE
        api_response['status_description'] = status_data[1]

    elif detection_type == ml.DETECTION_TYPE_AI_AGENT__DEEP_LEARNING:
        unified_credibility_score = ml.calculate_unified_credibility_score(deep_learning_data, ai_agent_data)
        analysis_data = ml.generate_core_analysis(deep_learning_data, ai_agent_data, unified_credibility_score)
        final_decision = ai_agent_data['final_decision']

        if final_decision == 'insufficient_evidence':
            final_decision = deep_learning_data['verdict']

        try:
            human_explanation = ml.generate_human_explanation(
                unified_credibility_score,
                deep_learning_data,
                ai_agent_data,
                analysis_data
            )
        except Exception:
            logger.exception("API / Gemini error : ")
            return {"message": "The request could not be processed. Please try again later."}, 500

        api_response['detection_type'] = detection_type
        api_response['final_decision'] = final_decision
        api_response['credibility_score'] = unified_credibility_score
        api_response['explanation'] = human_explanation
        api_response['sources_for_investigation'] = ai_agent_data["sources_for_investigation"]
        api_response['status'] = analysis_data["status"] #  VERIFIED - MIXED - WARNING - FALSE - UNCERTAIN
        api_response['status_description'] = analysis_data["status_description"]

    else:
        return {"message": "Invalid detection type."}, 400

    end_time = time.perf_counter()
    duration = end_time - start_time
    # Log analysis in csv file
    try:
        ml.log_detection_analysis(
            user_input=validated_data['user_input'],
            detection_type=detection_type,
            duration=timedelta(seconds=duration).total_seconds(),
            final_decision=api_response['final_decision'],
            status=api_response['status'],
            credibility_score=api_response['credibility_score'],
            explanation=api_response['explanation'],
            ai_agent_data=json.dumps(ai_agent_data, indent=4) if ai_agent_data else "",
            deep_learning_data=json.dumps(deep_learning_data, indent=4) if deep_learning_data else "",
        )
    except Exception:
        logger.exception("API / log detection analysis error : ")

    return api_response, 200


@bp.route('/download-fact-check-logs')
def download_fact_check_log():
    fact_check_log_file = os.path.normpath(settings.FACT_CHECK_LOG_PATH)

    if os.path.exists(fact_check_log_file):
        try:
            return send_file(
                fact_check_log_file,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f"InfoTrust_FactCheck_Logs_{os.getpid()}.csv"
            )
        except Exception as e:
            logger.exception("API / download fact-check-logs error :")
            return {"message": "The request could not be processed. Please try again later."}, 500
    else:
        logger.error("Log file does not exist.", fact_check_log_file)
        return {"message": "The request could not be processed. Please try again later."}, 500


@bp.route('/test', methods=['POST'])
def test():
    deep_learning_data = {
        "explanation": {
            "keywords": [
                "recent",
                "studies",
                "have",
                "confirmed",
                "consuming"
            ],
            "message": "This news as Real because the text contains informative terms such as ( recent, studies, have, confirmed, consuming ), which are commonly found in verified news articles.",
            "xai_word_attributions": [
                [
                    "[CLS]",
                    0.0
                ],
                [
                    "recent",
                    -0.7463117046751451
                ],
                [
                    "clinical",
                    0.013167859644787037
                ],
                [
                    "studies",
                    0.14275011074860858
                ],
                [
                    "have",
                    -0.2051186636269182
                ],
                [
                    "confirmed",
                    0.1110055757911002
                ],
                [
                    "that",
                    0.049248365205265925
                ],
                [
                    "consuming",
                    0.05068875660007753
                ],
                [
                    "high",
                    -0.10919297426088272
                ],
                [
                    "doses",
                    0.0026087407613320976
                ],
                [
                    "of",
                    -0.06916746929307398
                ],
                [
                    "vitamin",
                    0.11841253692686457
                ],
                [
                    "c",
                    0.23376103460622003
                ],
                [
                    "can",
                    -0.1812395752491513
                ],
                [
                    "completely",
                    0.0016356365357540594
                ],
                [
                    "prevent",
                    0.0848360329520229
                ],
                [
                    "the",
                    -0.3421569953029203
                ],
                [
                    "transmission",
                    0.07037606529013252
                ],
                [
                    "of",
                    0.0004282392230694813
                ],
                [
                    "respiratory",
                    0.04510831484745276
                ],
                [
                    "viruses",
                    0.10369631506456838
                ],
                [
                    "like",
                    0.011362676467075382
                ],
                [
                    "co",
                    -0.05856730023212532
                ],
                [
                    "##vid",
                    -0.14136806259058077
                ],
                [
                    "-",
                    -0.032922893634982554
                ],
                [
                    "19",
                    0.13454363207620199
                ],
                [
                    "and",
                    -0.010902634458027312
                ],
                [
                    "influenza",
                    0.07897411260475659
                ],
                [
                    ",",
                    -0.01482536013181913
                ],
                [
                    "making",
                    -0.06939952919478658
                ],
                [
                    "traditional",
                    0.020406966427512493
                ],
                [
                    "vaccines",
                    0.0392371108193462
                ],
                [
                    "unnecessary",
                    -0.017638985594111523
                ],
                [
                    "for",
                    -0.006717841243265907
                ],
                [
                    "healthy",
                    0.111495583017954
                ],
                [
                    "adults",
                    0.05419842232557031
                ],
                [
                    ".",
                    -0.17616692706276965
                ],
                [
                    "[SEP]",
                    0.0
                ]
            ]
        },
        "score": 99.99,
        "user_input": "Recent clinical studies have confirmed that consuming high doses of vitamin C can completely prevent the transmission of respiratory viruses like COVID-19 and influenza, making traditional vaccines unnecessary for healthy adults.",
        "verdict": "real"
    }

    agent_data =  {

        "claim": "Recent clinical studies have confirmed that consuming high doses of vitamin C can completely prevent the transmission of respiratory viruses like COVID-19 and influenza, making traditional vaccines unnecessary for healthy adults.",
        "final_decision": "fake",
        "credibility_score": 0.1,
        "final_justification": "The claim that high doses of vitamin C can completely prevent the transmission of respiratory viruses like COVID-19 and influenza, thereby making traditional vaccines unnecessary, is fake. While COVID-19 and influenza are indeed respiratory viruses, clinical studies do not support the assertion that high doses of vitamin C can completely prevent their transmission. Evidence suggests that vitamin C supplements are unlikely to prevent sickness and do not replace the need for traditional vaccines. Some research indicates that vitamin C may reduce the duration or severity of cold symptoms in specific circumstances or populations, but it does not prevent the spread of airborne pathogens or stop a virus from entering the body.",
        "sources_for_investigation": [
            "https://consultqd.clevelandclinic.org/covid-19-and-supplements-what-we-know-now",
            "https://asm.org/articles/2025/may/can-taking-vitamins-combat-infection",
            "https://nutritionsource.hsph.harvard.edu/2020/04/01/ask-the-expert-the-role-of-diet-and-nutritional-supplements-during-covid-19/",
            "https://www.today.com/health/cold-flu/vitamin-c-supplements-before-travel-rcna245646",
            "https://www.cambridge.org/core/journals/british-journal-of-nutrition/article/nutritional-status-diet-and-viral-respiratory-infections-perspectives-for-severe-acute-respiratory-syndrome-coronavirus-2/9325E3C0FD3D20C5209FF8FEFA93BF3C",
            "https://www.fredhutch.org/en/news/center-news/2015/12/separating-fact-from-fiction-about-colds-and-flu.html",
            "https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2021.674681/full",
            "https://consultqd.clevelandclinic.org/neither-high-dose-ascorbic-acid-nor-zinc-reduces-duration-of-covid-19-symptoms",
            "https://www.health.harvard.edu/blog/do-vitamin-d-zinc-and-other-supplements-help-prevent-covid-19-or-hasten-healing-2021040522310",
            "https://www.verywellhealth.com/airborne-vs-emergen-c-8712182",
            "https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2020.559811/full",
            "https://www.nature.com/articles/s41598-024-62571-5",
            "https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2020.01451/full",
            "https://www.nature.com/articles/s41598-025-91830-2",
            "https://cbs2iowa.com/news/local/iowa-respiratory-virus-activity-stays-high-as-flu-and-rsv-rise-covid-19-continues-to-fall-flu-season-trends-iowa-dhhs",
            "https://www.cdc.gov/respiratory-viruses/php/toolkit/index.html",
            "https://www.cidrap.umn.edu/covid-19/us-respiratory-virus-activity-rises-arkansas-reports-record-pertussis-year",
            "https://www.rush.edu/news/fall-respiratory-virus-update-covid-19-flu-rsv",
            "https://www.slocounty.ca.gov/departments/health-agency/public-health/department-news/slo-county-public-health-launches-enhanced-dashboard-to-track-respiratory-virus-season",
            "https://journals.asm.org/doi/10.1128/mbio.03376-25",
            "https://www.michigan.gov/mdhhs/keep-mi-healthy/infectious-diseases/seasonal-respiratory-viruses",
            "https://www.cdc.gov/respiratory-viruses/prevention/testing.html",
            "https://www.who.int/news-room/fact-sheets/detail/middle-east-respiratory-syndrome-coronavirus-(mers-cov)",
            "https://www.frontiersin.org/journals/cellular-and-infection-microbiology/articles/10.3389/fcimb.2025.1645333/full",
            "https://www.nature.com/articles/s41415-025-8888-8",
            "https://www.nature.com/articles/s41598-025-21722-y",
            "https://www.thelancet.com/journals/eclinm/article/PIIS2589-5370(23)00428-5/fulltext",
            "https://medicalxpress.com/news/2026-03-severe-covid-flu-lung-cancer.html",
            "https://www.discovermagazine.com/severe-covid-or-severe-flu-may-raise-risk-of-lung-cancer-but-vaccines-helped-in-animal-tests-48803",
            "https://www.cidrap.umn.edu/covid-19/babies-covid-19-develop-more-serious-disease-those-rsv-us-data-reveal",
            "https://www.cdc.gov/flu/hcp/clinical-guidance/testing-guidance-for-outpatient.html",
            "https://www.mayoclinic.org/diseases-conditions/flu/symptoms-causes/syc-20351719",
            "https://www.cidrap.umn.edu/misc-emerging-topics/study-describes-impact-human-metapneumovirus-outpatients",
            "https://www.washingtonpost.com/health/2026/03/04/flu-covid-differences-variants/",
            "https://health.ny.gov/diseases/communicable/respiratory_viruses/",
            "https://www.dartmouth-hitchcock.org/stories/article/how-do-you-know-if-you-have-covid-19-flu-or-rsv",
            "https://www.floridahealth.gov/diseases-and-conditions/disease/influenza-flu/",
            "https://www.britannica.com/science/swine-flu",
            "https://www.cdc.gov/yellow-book/hcp/travel-associated-infections-diseases/influenza.html",
            "https://www.abc27.com/news/health/whats-going-around/whats-going-around-flu-rsv-strep-throat-2/",
            "https://www.everydayhealth.com/diet-nutrition-products/best-vitamin-c-supplement/",
            "https://www.nytimes.com/2025/03/25/health/measles-kennedy-vitamin-a.html",
            "https://www.mayoclinichealthsystem.org/hometown-health/featured-topic/covid-19-vaccine-myths-debunked",
            "https://www.verywellhealth.com/airborne-supplement-770675"
        ],
        "subclaim_results": [
            {
                "subclaim": "Confirmed_by_studies(Consuming_high_doses_of_vitamin_C_prevents_transmission_of_respiratory_viruses) ::: Verify that recent clinical studies have confirmed that consuming high doses of vitamin C can completely prevent the transmission of respiratory viruses.",
                "classification": "not_supported",
                "justification": "Recent clinical studies do not confirm that consuming high doses of vitamin C can completely prevent the transmission of respiratory viruses. Evidence suggests it may decrease susceptibility or reduce the duration and severity of symptoms in specific populations (e.g., those under physical stress or with deficiencies), but it does not prevent the spread of airborne pathogens or stop a virus from entering the body."
            },
            {
                "subclaim": "Prevents_Transmission(High_doses_of_vitamin_C, Respiratory_viruses) ::: Verify that consuming high doses of vitamin C can completely prevent the transmission of respiratory viruses.",
                "classification": "not_supported",
                "justification": "Multiple sources indicate that high doses of vitamin C do not completely prevent the transmission of respiratory viruses, with some explicitly stating it won't stop a virus from entering the body. While some studies suggest it may reduce the incidence or duration of colds in specific populations, this does not equate to complete prevention of transmission."
            },
            {
                "subclaim": "Is_A(COVID-19, Respiratory_virus) ::: Verify that COVID-19 is a respiratory virus.",
                "classification": "supported",
                "justification": "Numerous public health organizations and scientific studies consistently classify COVID-19 (caused by SARS-CoV-2) as a respiratory virus, often grouping it with influenza and RSV as common respiratory illnesses."
            },
            {
                "subclaim": "Is_A(Influenza, Respiratory_virus) ::: Verify that influenza is a respiratory virus.",
                "classification": "supported",
                "justification": "Multiple sources, including medical and public health organizations, define influenza (flu) as a viral infection primarily affecting the respiratory system (nose, throat, and lungs), classifying it as a respiratory virus."
            },
            {
                "subclaim": "Makes_Unnecessary(High_doses_of_vitamin_C, Traditional_vaccines_for_healthy_adults) ::: Verify that consuming high doses of vitamin C makes traditional vaccines unnecessary for healthy adults.",
                "classification": "not_supported",
                "justification": "No evidence supports the claim that consuming high doses of vitamin C makes traditional vaccines unnecessary for healthy adults. Conversely, sources indicate that vitamin C supplements are unlikely to prevent sickness, which contradicts the idea of them replacing vaccines."
            }
        ]
    }

    if not request.is_json:
        return {"error": "Impossible de traiter la requête"}, 400

    try:
        schema = schemas.FactCheckingSchema(many=False)
        validated_data = schema.load(request.get_json())
    except ValidationError as err:
        return {"message": "invalid form"}, 400
    except Exception as e:
        logger.exception("API / prediction error : ")
        return {"error": "Impossible de traiter la requête"}, 500

    unified_credibility_score = ml.calculate_unified_credibility_score(deep_learning_data, agent_data)
    analysis_data = ml.generate_core_analysis(deep_learning_data, agent_data, unified_credibility_score)

    try:
        human_explanation = ml.generate_human_explanation(unified_credibility_score, deep_learning_data, agent_data, analysis_data)
    except Exception:
        logger.exception("Gemini error : ")
        return {"error": "Impossible de traiter la requête"}, 500

    return {
        "final_decision": agent_data["final_decision"],
        "status": analysis_data["status"],
        "unified_credibility_score": unified_credibility_score,
        "explanation": human_explanation,
        "sources_for_investigation": agent_data["sources_for_investigation"],
    }