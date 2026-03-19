from setup import settings
from google import genai
import os
import csv
import json
from datetime import datetime

gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

DETECTION_TYPE_DEEP_LEARNING = "DEEP_LEARNING"
DETECTION_TYPE_AI_AGENT= "AGENT"
DETECTION_TYPE_AI_AGENT__DEEP_LEARNING = "AGENT__DEEP_LEARNING"


def get_deep_learning_credibility_score(deep_learning_data):
    return deep_learning_data['score'] if deep_learning_data['verdict'] == "real" else (round(100 - deep_learning_data['score'], 2))


def calculate_unified_credibility_score(deep_learning_data, agent_data):
    # Normalization of the deep learning score
    # If the verdict is 'Fake', the probability of 'Real' is (100 - score)
    score_dl = deep_learning_data['score']
    proba_real_dl = get_deep_learning_credibility_score(deep_learning_data)

    # Agent Score (0.95 -> 95)
    score_agent = agent_data['credibility_score'] * 100

    # Weighting (80% Fact, 20% Style)
    unified_score = (score_agent * settings.AGENT_WEIGHT_SCORE) + (proba_real_dl * settings.DEEP_LEARNING_WEIGHT_SCORE)
    return round(unified_score, 2)


def generate_analysis(deep_learning_data, agent_data, final_score):
    # Extract data from both sub-systems
    verdict_agent = agent_data['final_decision'].lower()
    justification_agent = agent_data['final_justification']

    verdict_deep_learning = deep_learning_data['verdict'].lower()
    keywords = ", ".join(deep_learning_data['explanation']['keywords'])


    # Determine the Global Status based on sub-system alignment
    if verdict_agent == "insufficient_evidence":
        status = "UNCERTAIN / UNVERIFIED"
        style_context = (f"Our factual investigation could not find any external evidence. "
                         f"However, stylistic analysis suggests the text patterns are consistent "
                         f"with '{verdict_deep_learning}' content (keywords: {keywords}).")
    elif verdict_agent == "real" and verdict_deep_learning == "real":
        status = "VERIFIED"
        style_context = "The claim is backed by facts and written in a professional, neutral tone."
    elif verdict_agent == "real" and verdict_deep_learning == "fake":
        status = "MIXED (Sensationalist but True)"
        style_context = f"While the facts are accurate, the language used (keywords: {keywords}) is often associated with clickbait or misleading content."
    elif verdict_agent == "fake" and verdict_deep_learning == "real":
        status = "WARNING (Deceptive Sophistication)"
        style_context = "This is a sophisticated fabrication. It mimics a credible journalistic style to spread false information."
    else: # verdict_agent == "fake" and verdict_deep_learning == "fake"
        status = "FALSE / DISINFORMATION"
        style_context = "Neither the facts nor the linguistic patterns meet credibility standards."

    return {
        "status": status,
        "factual_evidence": justification_agent,
        "stylistic_analysis": style_context,
    }


def generate_human_explanation(final_score, dl_data, agent_data, analysis_data):
    """
    Synthesize factual evidence and stylistic analysis into a
    professional report using Gemini Model.
    """

    verdict_agent = agent_data['final_decision'].lower()
    justification_agent = agent_data['final_justification']
    keywords = ", ".join(dl_data['explanation']['keywords'])
    status = analysis_data['status']
    style_context = analysis_data['stylistic_analysis']

    # Prompt
    prompt_text = f"""
    Write a 3-sentence professional summary for a fact-checking report. 

    PRIMARY DATA (The Factual Truth):
    - Agent Verdict: {verdict_agent}
    - Agent Justification: {justification_agent}

    SYSTEM CONCLUSION:
    - Global Status: {status}
    - Final Score: {final_score}/100
    - Style Context: {style_context}

    INSTRUCTIONS:
    - You MUST base the core of your explanation on the 'Agent Justification'.
    - Start the narrative by addressing the factual reality discovered by the agent.
    - If the status is 'UNCERTAIN', explicitly state that no external evidence was found to confirm or deny the claim.
    - Mention how the writing style (Style Context) confirms or contrasts with the factual truth.
    - Return ONLY the explanation text in professional English.
    """

    # Gemini model call
    response = gemini_client.models.generate_content(
        model=settings.GEMINI_MODEL_NAME,
        contents=prompt_text
    )

    return response.text.strip()


def log_detection_analysis(user_input, detection_type, duration, final_decision, status, credibility_score, explanation, ai_agent_data, deep_learning_data):
    log_file = settings.FACT_CHECK_LOG_PATH
    headers = [
        "date",
        "user_input",
        "detection_type",
        "duration",
        "final_decision",
        "status",
        "credibility_score",
        "explanation",
        "ai_agent_data",
        "deep_learning_data"
    ]
    file_exists = os.path.isfile(log_file)

    row = {
        "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "user_input": user_input,
        "detection_type": detection_type,
        "duration": duration,
        "final_decision": final_decision,
        "status": status,
        "credibility_score": credibility_score,
        "explanation": explanation,
        "ai_agent_data": ai_agent_data,
        "deep_learning_data": deep_learning_data
    }

    with open(log_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)