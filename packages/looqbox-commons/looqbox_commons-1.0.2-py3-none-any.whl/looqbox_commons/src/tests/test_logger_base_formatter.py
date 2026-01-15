import logging
import unittest

from looqbox_commons.src.main.logger.formatters.base_formatter import BaseFormatter, LOG_RECORD_BUILTIN_ATTRS

class TestBaseFormatter(unittest.TestCase):

    def setUp(self) -> None:
        self.base_record_template = "%(timestamp) %(level) --- [threadId:%(thread_name)] [logger:%(logger)]: %(message)"
        self.default_log_keys = {
        "level": "levelname",
        "message": "message",
        "timestamp": "timestamp",
        "logger": "name",
        "module": "module",
        "function": "funcName",
        "thread_name": "thread"
        }
        self.mandatory_fields = {
            "message": "msg",
            "timestamp": "2024-01-01 18:00:00"
        }
        self.record = logging.LogRecord(name="testLogger",
                                        level=1,
                                        pathname="",
                                        lineno=1,
                                        msg="",
                                        args="",
                                        exc_info="")

    def test_fill_simple_template(self):

        template = "template message for %(test_value)"
        fill_in = {"test_value" : "unittest"}
        filled_template = BaseFormatter.fill_log_template_message(template, fill_in)
        self.assertEqual("template message for unittest",
                         filled_template)

    def test_fill_multiple_template(self):

        template = "template message for %(first_value) and %(second_value)"
        fill_in = {"first_value": "first",
                   "second_value": "second"}
        filled_template = BaseFormatter.fill_log_template_message(template, fill_in)

        self.assertEqual("template message for first and second",
                         filled_template)

    def test_record_to_dict(self):

        self.assertTrue(isinstance(BaseFormatter.record_to_dict(self.default_log_keys,
                                                                self.mandatory_fields,
                                                                self.record) ,
                                   dict)
                        )

    def test_removal_of_built_in_fields(self):

        record_as_dict = BaseFormatter.record_to_dict(self.default_log_keys, self.mandatory_fields, self.record)
        record_as_dict["extra_field"] = "new_field"

        clean_record_dict = BaseFormatter.remove_built_in_fields(self.record, record_as_dict)
        self.assertTrue(any(["extra_field" in clean_record_dict.keys()]))
        self.assertTrue(all([original_key in clean_record_dict.keys()
                             for original_key in record_as_dict.keys()])
                        )