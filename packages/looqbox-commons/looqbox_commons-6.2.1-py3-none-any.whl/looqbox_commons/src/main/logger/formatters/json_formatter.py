import datetime
import json
import logging
from looqbox_commons.src.main.logger.formatters.base_formatter import BaseFormatter


class LogJsonRecord(logging.Formatter):
    def __init__(self, *,
                 # keys passing in config.json. This attribute must be keep with the same name as the key in json
                 # handler in the config file, given that is the variable called by the logging.Formatter super class
        default_log_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.default_log_keys = default_log_keys if default_log_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        #Method called by the RootLogger, and so, it must be named 'format'
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):

        mandatory_fields = {
            "message": record.getMessage(),
            "timestamp": datetime.datetime.fromtimestamp(
                record.created, tz=datetime.timezone.utc
            ).isoformat(),
        }

        if record.exc_info is not None:
            mandatory_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            mandatory_fields["stack_info"] = self.formatStack(record.stack_info)

        record_as_dict = BaseFormatter.record_to_dict(self.default_log_keys ,mandatory_fields, record)
        record_as_dict.update(mandatory_fields)

        record_as_dict =  BaseFormatter.remove_built_in_fields(record, record_as_dict)
        record_as_dict["message"] = BaseFormatter.fill_log_template_message(record.getMessage(), record_as_dict)

        return record_as_dict
