import logging
from flaskr import create_app
import sys
import os
from setup import settings

logger = logging.getLogger(__name__)


def main():
    # Vérification du dossier et du fichier de configuration
    model_path = settings.MODEL_PATH
    if not (os.path.isdir(model_path) and os.path.exists(os.path.join(model_path, "config.json"))):
        logger.error(f" Erreur critique : Modèle introuvable à {model_path}")
        sys.exit(1)

    print("LOADED MODEL PATH", model_path)

    #
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
