import logging
from typing import override
from collections.abc import Mapping


class ColorFormatter(logging.Formatter):
    COLORS: Mapping[int, str] = {
        logging.DEBUG: "\033[36m",  # cyan
        logging.INFO: "\033[32m",  # green
        logging.WARNING: "\033[33m",  # yellow
        logging.ERROR: "\033[31m",  # red
        logging.CRITICAL: "\033[41m",  # red background
    }
    RESET: str = "\033[0m"

    def __init__(self, use_color: bool):
        super().__init__("%(levelname)s: %(message)s")
        self.use_color: bool = use_color

    @override
    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        if self.use_color and record.levelno in self.COLORS:
            return f"{self.COLORS[record.levelno]}{msg}{self.RESET}"
        return msg
