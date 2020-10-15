# settings.py
import os
import logging

if os.getenv("PY_ENV") == "DEV":
    from dotenv import load_dotenv

    load_dotenv()

logger = logging.getLogger("discord")

DEBUG = os.getenv("DEBUG")
LOG_TO_FILE = os.getenv("LOG_TO_FILE")
if DEBUG is True:
    print("DEBUG")
    # OR, the same with increased verbosity
    load_dotenv(verbose=True)
    logger.setLevel(logging.DEBUG)
else:
    print("NOT DEBIG")
    logger.setLevel(logging.INFO)

if LOG_TO_FILE is True:
    print("LOG_TO_FILE")
    handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)
