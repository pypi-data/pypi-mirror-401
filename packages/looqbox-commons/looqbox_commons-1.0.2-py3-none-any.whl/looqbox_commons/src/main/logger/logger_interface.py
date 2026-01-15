import enum
import functools
import logging.handlers
import shutil
import time
from typing import Callable
import os

from looqbox.global_calling import GlobalCalling
from looqbox_commons.src.main.logger.logger import RootLogger

RESERVED_KEYS=["logger", "timestamp", "level", "message"]

class LogLevel(enum.Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR

    @classmethod
    def from_str(cls, level: str):
        return cls[level.upper()]

class LoggerInterface:

    logger:logging.Logger = None

    def log_info(self, message: str, execution_time: bool = False, time_elapsed: float = 0.0, **user_defined_info):
        """
        Method helper to log an info record.

        Args:
            message (str): message that will be used in log record, a palce holder might be added with the pattern
                           %(valName), given that valName will be passed in user_defined_info field.
            execution_time (bool, optional): set whether a time elapsed will be added to the message.
            time_elapsed (float, optional): the value that will be inserted in the message given
                                            the value of execution_time.
            user_defined_info (any, optional): Any value the user wishes to add to log message or record.

        Examples:
            >>> # simple message
            >>> log_info(message="log an info record")
            >>> # message with template replacement
            >>> log_info(message="log of response %(response_id) for the user %(user_id)", response_id=10, user_id=1)
            ...# the final message will be: "log of response 10 for the user 1"
        """

        user_info = self._prepare_log_record(execution_time, time_elapsed, user_defined_info)
        self._create_log_record("info", message, **user_info)

    def log_error(self, message: str, execution_time: bool = False, time_elapsed: float = 0.0, **user_defined_info):
        """
        Method helper to log an error record.

        Args:
            message (str): message that will be used in log record, a palce holder might be added with the pattern
                           %(valName), given that valName will be passed in user_defined_info field.
            execution_time (bool, optional): set whether a time elapsed will be added to the message.
            time_elapsed (float, optional): the value that will be inserted in the message given
                                            the value of execution_time.
            user_defined_info (any, optional): Any value the user wishes to add to log message or record.

        Examples:
            >>> # simple message
            >>> log_error(message="log an error record")
            >>> # message with template replacement
            >>> log_error(message="error due %(error_msg)", error_msg=str(ZeroDivisionError))
             ...# the final message will be: "error due division by zero"
        """

        user_info = self._prepare_log_record(execution_time, time_elapsed, user_defined_info)
        self._create_log_record("error", message, **user_info)

    def log_warning(self, message: str, execution_time: bool = False, time_elapsed: float = 0.0, **user_defined_info):
        """
        Method helper to log a warning record.

        Args:
            message (str): message that will be used in log record, a palce holder might be added with the pattern
                           %(valName), given that valName will be passed in user_defined_info field.
            execution_time (bool, optional): set whether a time elapsed will be added to the message.
            time_elapsed (float, optional): the value that will be inserted in the message given
                                            the value of execution_time.
            user_defined_info (any, optional): Any value the user wishes to add to log message or record.

        Examples:
            >>> # simple message
            >>> log_warning(message="log a warning record")
            >>> # message with template replacement
            >>> log_warning(message="the file %(target_file) might not exist", target_file="result.csv")
            ...# the final message will be: "the file result.csv might not exist"
        """

        user_info = self._prepare_log_record(execution_time, time_elapsed, user_defined_info)
        self._create_log_record("warning", message, **user_info)

    def log_debug(self, message: str, execution_time: bool = False, time_elapsed: float = 0.0, **user_defined_info):
        """
        Method helper to log a debug record.

        Args:
            message (str): message that will be used in log record, a palce holder might be added with the pattern
                           %(valName), given that valName will be passed in user_defined_info field.
            execution_time (bool, optional): set whether a time elapsed will be added to the message.
            time_elapsed (float, optional): the value that will be inserted in the message given
                                            the value of execution_time.
            user_defined_info (any, optional): Any value the user wishes to add to log message or record.

        Examples:
            >>> # simple message
            >>> log_debug(message="log a debug record")
            >>> # message with template replacement
            >>> log_debug(message="reach test method %(method_name)", method_name="get_user_id")
            # the final message will be: "reach test method get_user_id"
        """
        user_info = self._prepare_log_record(execution_time, time_elapsed, user_defined_info)
        self._create_log_record("debug", message, **user_info)

    @staticmethod
    def _remove_reserved_words(keys_passed_by_the_user: dict) -> dict:

        revised_user_keys = dict()

        for user_keys in keys_passed_by_the_user.keys():
            if user_keys in RESERVED_KEYS:
                revised_user_keys[f"{user_keys}_user"] = keys_passed_by_the_user[user_keys]
            else:
                revised_user_keys[user_keys] = keys_passed_by_the_user[user_keys]

        return revised_user_keys

    def _prepare_log_record(self, execution_time: bool, time_elapsed: float, user_keys: dict):
        user_info = self._remove_reserved_words(user_keys)
        if execution_time:
            user_info["execution_time"] = time_elapsed

        return user_info

    def log_method(self, _func=None, *_func_arguments, level: str= "info", message:str ="",**log_infos):
        """
        Decorator to create a record whenever a given function or method is called.

        Args:
            _func_arguments (any, optional): arguments for the target function execution
            level (str, optional): record severity. Default is info.
            message (str, optional): record template that will be logged along the function exectuion.
            log_infos (any, optional): values to be fill message template.

        Examples:
            >>> @log_method(level="info", message="wait Log for %(wait_time) secs", wait_time=2)
            >>> def wait_fun():
            ...    #let's wait a few
            ...    sleep(2)
            ...    return 0
            ...# the final message will be: "wait Log for 2 secs"
        """
        def decorator_log(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    self._create_log_record(level, f"Starting function %(funName)" + message,
                                            funName = func.__qualname__,
                                            **log_infos)

                    result = func(*args, **kwargs)
                    eval_time = round(time.time() - start_time, 3)

                    self._create_log_record(level, f"Finished function %(funName) elapsed in %(evalTime)",
                                            funName = func.__qualname__,
                                            evalTime = eval_time,
                                            **log_infos)
                    return result

                except Exception as e:
                    eval_time = round(time.time() - start_time, 3)
                    self._create_log_record("error", msg="Error in %(funName): %(errorMsg)",
                                            funName=func.__qualname__,
                                            errorMsg=str(e),
                                            evalTime = eval_time,
                                            **log_infos)
                    raise e
            return wrapper

        if _func is None:
            return decorator_log
        else:
            return decorator_log(_func)

    def log(self, level: str= "info", message:str ="", **log_infos):
        """
        Method to create a log record to a given severity.

            level (str, optional): record severity. Default is info.
            message (str, optional): record template that will be logged along the function exectuion.
            log_infos (any, optional): values to be fill message template.

        Examples:
            >>> log_method(level="info", message="standalone log for the val: %(val)", val=2)
            ...# the final message will be: "standalone log for the val: 2"
        """
        self._create_log_record(level, message, **log_infos)

    def get_log_level_method(self, log_level) -> Callable:

        log_methods = {
            "error": lambda message, infos: self.logger.error(message, extra=infos),
            "info": lambda message, infos: self.logger.info(message, extra=infos),
            "debug": lambda message, infos: self.logger.debug(message, extra=infos),
            "warning": lambda message, infos: self.logger.warning(message, extra=infos)
        }

        return log_methods.get(log_level, log_methods['info'])

    def _create_log_record(self, log_level, msg, **log_infos):

        log_method = self.get_log_level_method(log_level)
        log_method(msg, log_infos)

    def get_log_files_path(self) -> list[str]:
        log_files: list[str] = list()
        log_dir = RootLogger().log_dir
        for file in os.listdir(log_dir):
            if self._is_log_file(file):
                temp_log_path = GlobalCalling.looq.temp_file(file, add_hash=False)
                self._copy_content_to_temp_file(os.path.join(log_dir, file), temp_log_path)
                log_files.append(temp_log_path)

        return log_files

    @staticmethod
    def _is_log_file(file: str) -> bool:
        return not file.startswith('.') and '.jsonl' in file

    @staticmethod
    def _copy_content_to_temp_file(log_file, temp_file) -> None:
            shutil.copy(log_file, temp_file)