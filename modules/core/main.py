import logging
from flaskr import create_app
import sys
import os
from setup import settings

logger = logging.getLogger(__name__)


def main():
    # Vérification du dossier et du fichier de configuration
    #
    print("DEEP LEARNING API URL ", settings.DEEP_LEARNING_API_URL)
    print("AI AGENT API URL ", settings.AI_AGENT_API_URL)
    try:
        flask_app = create_app()
        flask_app.run(port=int(settings.APP_PORT), host="0.0.0.0")
        #serve(flask_app, host="0.0.0.0", port=int(config.SERVICE_PORT))
    except Exception as e:
        logger.exception("APP / flask run error : ")
        sys.exit(1)


if __name__ == "__main__":
    logger.info("APP / Starting service")
    main()
