from loguru import logger
from datetime import datetime
import pytz
import os, sys

_timezone = pytz.timezone('Asia/Shanghai')
_level = 'INFO'

def _format_time(record):
    record["time"] = record["time"].astimezone(_timezone)
    return True

def _setup_logger():
    logger.remove()
    fmt = '{time:MM-DD HH:mm:ss}|{level}|{message}'
    cur_date = datetime.now(tz=_timezone).strftime('%Y-%m-%d')
    os.makedirs('logs', exist_ok=True)
    logger.add(f'logs/{cur_date}.log', level=_level, format=fmt, filter=_format_time, rotation="1 day", retention=3)
    logger.add(sys.stdout, level=_level, format=fmt, filter=_format_time)

def set_timezone(timezone):
    global _timezone
    _timezone = pytz.timezone(timezone)
    _setup_logger()

def set_level(level):
    global _level
    _level = level
    _setup_logger()

logger.set_timezone = set_timezone
logger.set_level = set_level

_setup_logger()
