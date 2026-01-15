import unittest
from typing import List

from dynamic_response_package.src.main.objects.context.response_column import ResponsePartition
from looqbox_commons.src.main.object_mapper.object_mapper import ObjectMapper
from dynamic_response_package.src.main.utils.utils import load_test_json_from_root_path


class TestObjectMapper(unittest.TestCase):
    def setUp(self) -> None:
        self.object_mapper = ObjectMapper()
        self.dict_0 = load_test_json_from_root_path("resources/context_info_test.json")

    def test_partition_reading(self):
        partitions = self.dict_0.get("partitions")
        partitions_obj = self.object_mapper.map(partitions, List[ResponsePartition])
        first_obj = partitions_obj[0]
        self.assertIsInstance(first_obj, ResponsePartition)
