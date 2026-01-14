from .log import logger_instance as logger, LoggerConfig, _default_config

__version__ = "1.0.0"
__all__ = ["logger", "LoggerConfig", "set_timezone", "set_level"]


def set_timezone(timezone):
    """Set the timezone for logging.
    
    Args:
        timezone (str): Timezone string (e.g., 'Asia/Shanghai', 'UTC', 'America/New_York')
    """
    _default_config.set_timezone(timezone)


def set_level(level):
    """Set the minimum log level.
    
    Args:
        level (str): Log level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    """
    _default_config.set_level(level)