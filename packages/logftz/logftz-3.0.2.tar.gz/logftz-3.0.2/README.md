# LogFtz - Timezone-Configurable Logging Package

A Python logging package based on loguru with configurable timezone support. Defaults to Shanghai timezone (Asia/Shanghai) but allows users to set any timezone.

## Features

- 🕐 Configurable timezone support (defaults to Asia/Shanghai)
- 📊 Configurable minimum log level (defaults to INFO)
- 📝 Clean log format: `MM-DD HH:mm:ss|LEVEL|MESSAGE`
- 📁 Automatic daily log file rotation
- 🗂️ Automatic retention of last 3 days of log files
- 🚀 Built on high-performance loguru library
- 🌍 International support with English interface

## Installation

### Install dependencies

```bash
pip install logftz
```

## Usage

### Basic Usage

```python
from logftz import logger

# Log with different levels
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.debug("This is a debug message")
```

### Timezone Configuration

```python
from logftz import logger, set_timezone

# Set timezone globally
set_timezone('UTC')
logger.info("This message uses UTC timezone")

# Set to New York timezone
set_timezone('America/New_York')
logger.info("This message uses New York timezone")

# Back to Shanghai timezone (default)
set_timezone('Asia/Shanghai')
logger.info("This message uses Shanghai timezone")
```

### Log Level Configuration

```python
from logftz import logger, set_level

# Set minimum log level to DEBUG (show all logs)
set_level('DEBUG')
logger.debug("This debug message will now be shown")

# Set minimum log level to WARNING (hide INFO and DEBUG)
set_level('WARNING')
logger.info("This info message will be hidden")
logger.warning("This warning message will be shown")
```

### Advanced Usage with Custom Configuration

```python
from logftz import LoggerConfig

# Create a custom logger configuration with timezone and level
config = LoggerConfig(timezone='Europe/London', level='DEBUG')

# Change timezone or level later
config.set_timezone('Asia/Tokyo')
config.set_level('WARNING')
```

### Log Output Example

```
12-25 14:30:15|INFO|This is an info message
12-25 14:30:16|WARNING|This is a warning message
12-25 14:30:17|ERROR|This is an error message
```

## Configuration

- **Default Timezone**: Asia/Shanghai
- **Log Level**: INFO and above
- **File Path**: `logs/YYYY-MM-DD.log`
- **Rotation**: Daily rotation
- **Retention**: Keep last 3 days of log files
- **Format**: `MM-DD HH:mm:ss|LEVEL|MESSAGE`

## Supported Timezones

You can use any timezone supported by pytz, including:

- `UTC`
- `Asia/Shanghai`
- `Asia/Tokyo`
- `Europe/London`
- `America/New_York`
- `America/Los_Angeles`
- And many more...

## Project Structure

```
logftz/
├── logftz/
│   ├── __init__.py    # Package initialization and public API
│   └── log.py         # Core logging configuration
├── setup.py           # Installation configuration
├── requirements.txt   # Dependencies
└── README.md         # Documentation
```

## Dependencies

- loguru >= 0.6.0
- pytz >= 2021.1

## API Reference

### Functions

- `set_timezone(timezone: str)`: Set the global timezone for logging
- `set_level(level: str)`: Set the minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### Classes

- `LoggerConfig(timezone: str = 'Asia/Shanghai', level: str = 'INFO')`: Create a custom logger configuration
  - `set_timezone(timezone: str)`: Change the timezone for this configuration
  - `set_level(level: str)`: Change the minimum log level for this configuration

### Variables

- `logger`: The main logger instance (loguru logger)

## License

MIT License