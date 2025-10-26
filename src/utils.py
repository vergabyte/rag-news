from loguru import logger
from pathlib import Path

Path('logs').mkdir(exist_ok=True)
logger.add('logs/app.log')