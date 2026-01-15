import datetime
import logging
from looqbox_commons.src.main.logger.formatters.base_formatter import BaseFormatter


class StdoutRecord(logging.Formatter):
    def __init__(self, *,
                 # keys passing in config.json. This attribute must be keep with the same name as the key in simple
                 # handler in the config file, given that is the variable called by the logging.Formatter super class
                 default_log_keys: dict[str, str] | None = None,
                 ):
        super().__init__()
        self.default_log_keys = default_log_keys if default_log_keys is not None else {}
        self.base_record_template = "%(timestamp) %(level) --- [threadId:%(thread_name)] [logger:%(logger)]: %(message)"

    def format(self, record: logging.LogRecord) -> str:
        # Method called by the RootLogger, and so, it must be named 'format'
        message = self._prepare_log_dict(record)
        return message

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

        record_as_dict["message"] = BaseFormatter.fill_log_template_message(record.getMessage(),
                                                                            BaseFormatter.remove_built_in_fields(record,
                                                                                                         record_as_dict)
                                                                            )

        filled_template = BaseFormatter.fill_log_template_message(self.base_record_template, record_as_dict)
        return filled_template
