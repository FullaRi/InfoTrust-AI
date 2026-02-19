import logging
from flaskr import create_app
import sys


logger = logging.getLogger(__name__)

flask_app = create_app()

def main():
    #
    try:
        flask_app.run(port=8000, host="0.0.0.0")
        #serve(flask_app, host="0.0.0.0", port=int(config.SERVICE_PORT))
    except Exception as e:
        logger.exception("APP / flask run error : ")
        sys.exit(1)


if __name__ == "__main__":
    logger.info("APP / Starting service")
    main()
