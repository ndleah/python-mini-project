<!--Please do not remove this part-->
![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# LoggerLibrary

## Description

A simple Python logging utility with console/file output and automatic log cleanup. This library provides an easy-to-use interface for setting up logging in your Python projects with minimal configuration.

**Key Features:**
- Simple setup with one function call
- Session tracking with auto-generated UUID to trace logs from the same execution
- Dual output: log to console for debugging and file for persistent records
- Auto cleanup: keep only recent logs (default: 3 days), no manual deletion needed

## Languages or Frameworks Used

This project uses Python 3.x with only standard library modules (no external dependencies required).

## How to run

### Quick Start

1. create `demo.py`

2. Import the logger setup function:
```python
from logger import setup_logger
```

3. Choose your setup method:

**Method 1: Customized Configuration**
```python
logger = setup_logger(
    name=__name__,
    enable_console=True,
    enable_file=True,
    level=logging.INFO,
    dir='./logs'
)
logger.debug('Debug message')
logger.info('Info message')
```

**Method 2: Default Configuration**
```python
logger = setup_logger()
logger.debug('Debug message')
logger.info('Info message')
```

4. Run your Python script:
```bash
python3 demo.py
```

### Log Output Format

```
2025-11-16 00:41:00,951 | demo.py | INFO | 49e1e65d-2734-4807-81de-306ee628d788 | Your message
```

## Demo

See the result of running the logger with both console and file output:
<img src="result.jpg" width=80% height=80%>

## Author

Shyin Lim -> https://github.com/shyinlim