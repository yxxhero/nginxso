import os
from loguru import logger
BASE_LOG_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger.add(os.path.join(BASE_LOG_PATH, "log", "nginxso_{time:YYYY-MM-DD}.log"),
           format="{time:YYYY:MM:DD HH:mm:ss} | {level} | {file}:{line} | {message}", retention="10 days")


if __name__ == "__main__":
    logger.info("test")
