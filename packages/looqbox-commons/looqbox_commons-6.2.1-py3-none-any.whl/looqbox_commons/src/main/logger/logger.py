import enum
import json
import logging
import logging.config
import logging.handlers
import os
from datetime import datetime
from typing import Optional


class LogLevel(enum.Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR

    @classmethod
    def from_str(cls, level: str):
        return cls[level.upper()]


class RootLogger:
    logger_configuration: Optional[dict] = None

    def __init__(self):
        self._load_logger_configuration()
        self._set_log_file_name()
        # self.set_log_level()

    def _set_log_configuration(self) -> None:
        try:
            logging.config.dictConfig(self.logger_configuration)
        except Exception:
            logging.basicConfig(level=logging.INFO)

        # queue_handler = logging.getHandlerByName("queue_handler")
        # if queue_handler is not None:
        #     queue_handler.listener.start()
        #     atexit.register(queue_handler.listener.stop)

    def _load_logger_configuration(self) -> None:
        _current_path = os.path.dirname(__file__)
        resources_dir = os.path.join(_current_path, "..", "resources")
        config_path = os.path.join(resources_dir, "logger_config", "base_logger.json")
        with open(config_path, "r") as config:
            self.logger_configuration = json.load(config)
            config.close()

    @property
    def log_dir(self) -> str:
        looqbox_home_dir = os.getenv("LOOQBOX_HOME", "")
        return os.path.join(looqbox_home_dir, "log")

    def _set_log_file_name(self) -> None:
        base_file_name = f"python_log-{str(datetime.today().date())}.jsonl"
        self.logger_configuration["handlers"]["file_json"]["filename"] = os.path.join(self.log_dir, base_file_name)

    def set_log_level(self, log_level: str) -> None:
        level = LogLevel.from_str(log_level)
        self.logger_configuration["loggers"]["root"]["level"] = level

    def get_new_logger(self, logger_name: str, use_stream_handler=True, use_file_handler=True) -> logging.Logger:

        if not use_stream_handler:
            del self.logger_configuration["formatters"]["simple"]

        if not use_file_handler:
            del self.logger_configuration["formatters"]["json"]

        self._set_log_configuration()
        return logging.getLogger(logger_name)
