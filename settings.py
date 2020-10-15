# settings.py
import os
import sys
import logging

if os.getenv("PY_ENV") == "DEV":
    from dotenv import load_dotenv

    load_dotenv(verbose=True)

logger = logging.getLogger("discord")

DEBUG = os.getenv("DEBUG")
LOG_TO_FILE = os.getenv("LOG_TO_FILE")

if LOG_TO_FILE is True:
    handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)
    logger.info("LOG_TO_FILE")
else:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)
    logger.info("LOG to STDOUT")

if DEBUG == "True":
    # OR, the same with increased verbosity
    logger.setLevel(logging.DEBUG)
    logger.info("DEBUG")
else:
    logger.setLevel(logging.INFO)
    logger.info("NOT DEBUG")
