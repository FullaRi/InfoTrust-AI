import requests
import logging
from setup import settings

logger = logging.getLogger(__name__)

class DeepLearningServiceApi:

    @staticmethod
    def predict(user_input: str):
        payload = {'user_input': user_input}

        # try:
        response = requests.post(
            url=settings.DEEP_LEARNING_API_URL,
            json=payload,
            timeout=(5 * 60)
        )
        response.raise_for_status()
        # except requests.exceptions.HTTPError as errh:
        #     logger.exception(errh)
        #     raise Exception("API Error")
        # except requests.exceptions.Timeout as errt:
        #     logger.exception(errt)
        #     raise Exception("API Error")
        # except requests.exceptions.RequestException as err:
        #     logger.exception(err)
        #     raise Exception("API Error")

        """
        Exemple of response :
        {
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
                        "[SEP]",
                        0.0
                    ]
                ]
            },
            "prediction_score": 1.0,
            "credibility_score": 1.0,
            "status": "CREDIBLE",
            "status_description": "Verified Style Markers : nasa, recently, admitted, in, leaked",
            "user_input": "NASA recently admitted in a leaked internal memo that the 1969 moon landing was filmed in a high-security studio in Nevada because the radiation belts were too deadly for astronauts to survive the journey through deep space.",
            "verdict": "real"
        }
        """
        deep_learning_data = response.json()

        return {
            "explanation": deep_learning_data["explanation"],
            "credibility_score": deep_learning_data["credibility_score"],
            "prediction_score": deep_learning_data["prediction_score"],
            "verdict": deep_learning_data["verdict"],
            "status": deep_learning_data["status"],
            "status_description": deep_learning_data["status_description"]
        }

class AiAgentServiceApi:

    @staticmethod
    def predict(user_input: str):
        payload = {'user_input': user_input}


        response = requests.post(
            url=settings.AI_AGENT_API_URL,
            json=payload,
            timeout=(30 * 60)
        )
        response.raise_for_status()



        """
        Exemple of response :
        {
            "output": {
                "claim": "A new diplomatic treaty signed in Brussels aims to standardize international carbon tax credits among 50 nations, creating a unified framework to penalize major industrial emitters while subsidizing renewable energy startups.",
                "final_decision": "fake",
                "credibility_score": 0.1,
                "final_justification": "Evidence does not support the existence of a new diplomatic treaty signed in Brussels with the specific aims outlined in the claim. While there are discussions and agreements related to carbon credit standardization (e.g., COP29 outcomes), these are not linked to a single new treaty signed in Brussels involving 50 nations. Furthermore, the evidence does not confirm that any such unified framework aims to penalize major industrial emitters or subsidize renewable energy startups in the manner described. Many aspects of the claim lack supporting evidence or are contradicted by the provided information.",
                "sources_for_investigation": [
                    "https://thediplomat.com/2025/09/date-set-for-uzbekistan-to-sign-enhance-partnership-agreement-with-the-european-union/",
                ],
                "subclaim_results": [
                    {
                        "subclaim": "Signed(New_Diplomatic_Treaty, Brussels) ::: Verify a new diplomatic treaty was signed in Brussels.",
                        "classification": "not_supported",
                        "justification": "The evidence indicates that an Enhanced Partnership and Cooperation Agreement between the EU and Uzbekistan is *set to be signed* in Brussels in October 2025, which is a future event, not a past signing. Another diplomatic agreement was signed in Washington, not Brussels."
                    },
                    {
                        "subclaim": "Aims(New_Diplomatic_Treaty, Standardize_International_Carbon_Tax_Credits) ::: Verify the new diplomatic treaty aims to standardize international carbon tax credits.",
                        "classification": "supported",
                        "justification": "Evidence from COP29 and discussions around a \"carbon club\" indicate ongoing efforts and agreements to establish rules and frameworks for a global market to buy and sell carbon credits, which aligns with the aim of standardizing international carbon tax credits."
                    }
                ]
            }
        }
        
        
        ----
        
         {
            "output": {
                "final_decision": "fake_insufficient_evidence",
                "credibility_score": 0,
                "final_justification": "The claim is classified as fake_insufficient_evidence because no supporting evidence was provided for the subclaim. The provided input contained null values for the subclaim, question, and source link, and explicitly stated \"None\" for evidence extraction. Without any verifiable information or sources, the claim cannot be supported.",
                "sources_for_investigation": [],
                "subclaim_results": [
                ]
            }
        }
        """
        agent_data = response.json()

        return {
            "final_decision": agent_data["output"]["final_decision"],
            "credibility_score": agent_data["output"]["credibility_score"],
            "final_justification": agent_data["output"]["final_justification"],
            "sources_for_investigation": agent_data["output"]["sources_for_investigation"],
            "subclaim_results": agent_data["output"]["subclaim_results"],
        }