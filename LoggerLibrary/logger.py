import logging
import os
import re
import sys
import uuid as uuid_module
from datetime import datetime, timedelta

# === Configuration ===
ENABLE_CONSOLE = True
ENABLE_FILE = True
LOG_LEVEL = logging.DEBUG
LOG_DIR = './.log'
KEEP_DAYS = 3


def setup_logger(
    name: str = None,
    enable_console: bool = ENABLE_CONSOLE,
    enable_file: bool = ENABLE_FILE,
    level: int = LOG_LEVEL,
    dir: str = LOG_DIR
    ) -> logging.Logger:
    """Setup logger with console and file handlers

    Args:
        name: Logger name (use __name__ to get current file), default None (root logger)
        enable_console: Enable console output, default True
        enable_file: Enable file output, default True
        level: Logging level, default DEBUG
        dir: Log file directory, default './.log'

    Returns:
        Configured logger instance

    Example:
        from logger import setup_logger

        logger = setup_logger(name=__name__, enable_console=True, enable_file=False)
        logger.info('Test message')
    """
    # Setup logger
    logger = logging.getLogger(name=name if name else '')
    logger.setLevel(level=level)


    logger.handlers.clear() # Clear existing handlers to prevent duplicate logs

    session_uuid = uuid_module.uuid4()
    formatter = logging.Formatter(
        f'%(asctime)s | %(filename)s | %(levelname)s | {session_uuid} | %(message)s'
    )

    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(stream=sys.stderr)
        console_handler.setLevel(level=level)
        console_handler.setFormatter(fmt=formatter)
        logger.addHandler(hdlr=console_handler)

    # File handler
    if enable_file:
        os.makedirs(name=dir, mode=0o777, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d')
        file_path = os.path.join(dir, f'{timestamp}.log')

        file_handler = logging.FileHandler(filename=file_path, encoding='utf-8')
        file_handler.setLevel(level=level)
        file_handler.setFormatter(fmt=formatter)
        logger.addHandler(hdlr=file_handler)

        logger.info(f'Log file created: {file_path}')

        # Clean old log files
        cleanup_old_logs(directory=dir, keep_days=KEEP_DAYS, logger=logger)

    return logger


def cleanup_old_logs(directory: str, keep_days: int = 3, logger: logging.Logger = None) -> None:
    """Clean up log files older than specified days

    Args:
        directory: Directory containing log files
        keep_days: Number of days to keep log files, default 3
        logger: Logger instance for logging cleanup results
    """
    now = datetime.now()
    pattern = re.compile(r'(\d{8})_\d{6}\.log')

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            date_str = match.group(1)
            try:
                file_date = datetime.strptime(date_str, '%Y%m%d')
                if now - file_date > timedelta(days=keep_days):
                    os.remove(path=os.path.join(directory, filename))
                    if logger:
                        logger.info(f'Deleted old log: {filename}')
            except Exception as e:
                if logger:
                    logger.warning(f'Failed to delete log: {filename}; {e}')
