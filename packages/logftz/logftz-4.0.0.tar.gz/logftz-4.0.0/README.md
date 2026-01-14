# LogFtz - Timezone-Configurable Logging Package

A Python logging package based on loguru with configurable timezone support. Defaults to Shanghai timezone (Asia/Shanghai) but allows users to set any timezone.

## Features

- 🕐 Configurable timezone support (defaults to Asia/Shanghai)
- 📊 Configurable minimum log level (defaults to INFO)
- 📝 Clean log format: `MM-DD HH:mm:ss|LEVEL|MESSAGE`
- 📁 Automatic daily log file rotation
- 🗂️ Automatic retention of last 3 days of log files
- 🚀 Built on high-performance loguru library

## Installation

```bash
pip install logftz
```

## Usage

### Basic Usage

```python
from logftz import logger

logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.debug("This is a debug message")
```

### Set Log Level

```python
from logftz import logger

# Set minimum log level to DEBUG (show all logs)
logger.set_level('DEBUG')
logger.debug("This debug message will now be shown")

# Set minimum log level to WARNING (hide INFO and DEBUG)
logger.set_level('WARNING')
```

### Set Timezone

```python
from logftz import logger

logger.set_timezone('UTC')
logger.set_timezone('America/New_York')
logger.set_timezone('Asia/Shanghai')
```

### Log Output Example

```
12-25 14:30:15|INFO|This is an info message
12-25 14:30:16|WARNING|This is a warning message
12-25 14:30:17|ERROR|This is an error message
```

## Configuration

- **Default Timezone**: Asia/Shanghai
- **Default Log Level**: INFO
- **File Path**: `logs/YYYY-MM-DD.log`
- **Rotation**: Daily rotation
- **Retention**: Keep last 3 days of log files
- **Format**: `MM-DD HH:mm:ss|LEVEL|MESSAGE`

## API Reference

### Methods

- `logger.set_level(level: str)`: Set minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logger.set_timezone(timezone: str)`: Set timezone for logging

## License

MIT License
