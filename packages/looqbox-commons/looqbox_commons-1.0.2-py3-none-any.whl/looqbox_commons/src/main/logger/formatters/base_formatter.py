import logging

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}

class BaseFormatter:

    @classmethod
    @staticmethod
    def fill_log_template_message(template_message, info):

        for attribute in info:
            template_message = template_message.replace(f"%({attribute})", str(info.get(attribute)))
        return template_message

    @classmethod
    @staticmethod
    def remove_built_in_fields(record:logging.LogRecord, record_as_dict: dict):
        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                record_as_dict[key] = val
        return record_as_dict

    @classmethod
    @staticmethod
    def record_to_dict(default_log_keys, mandatory_fields:dict, record:logging.LogRecord) -> dict:
        record_as_dict = {
            key: msg_val
            if (msg_val := mandatory_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in default_log_keys.items()
        }
        return record_as_dict
