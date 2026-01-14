# LogFtz - Timezone-Configurable Logging Package

A Python logging package based on loguru with configurable timezone support. Defaults to Shanghai timezone (Asia/Shanghai) but allows users to set any timezone.

## Features

- 🕐 Configurable timezone support (defaults to Asia/Shanghai)
- 📊 Configurable minimum log level (defaults to INFO)
- 📁 Configurable log file rotation (defaults to 1 day)
- 🗂️ Configurable log file retention (defaults to 3 days)
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

### Set Rotation (File Size or Time)

```python
from logftz import logger

# Rotate by file size
logger.set_rotation("100 MB")
logger.set_rotation("500 KB")

# Rotate by time
logger.set_rotation("1 day")
logger.set_rotation("12 hours")
```

### Set Retention (Days to Keep)

```python
from logftz import logger

# Keep last 7 days of log files
logger.set_retention(7)

# Keep last 30 days
logger.set_retention(30)
```

### Log Output Example

```
12-25 14:30:15|INFO|This is an info message
12-25 14:30:16|WARNING|This is a warning message
12-25 14:30:17|ERROR|This is an error message
```

## Default Configuration

- **Timezone**: Asia/Shanghai
- **Log Level**: INFO
- **Rotation**: 1 day
- **Retention**: 3 days
- **File Path**: `logs/YYYY-MM-DD.log`
- **Format**: `MM-DD HH:mm:ss|LEVEL|MESSAGE`

## API Reference

### Methods

- `logger.set_level(level: str)`: Set minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logger.set_timezone(timezone: str)`: Set timezone for logging
- `logger.set_rotation(rotation: str)`: Set log file rotation (e.g., "100 MB", "1 day", "12 hours")
- `logger.set_retention(retention: int)`: Set number of days to keep log files

## License

MIT License
