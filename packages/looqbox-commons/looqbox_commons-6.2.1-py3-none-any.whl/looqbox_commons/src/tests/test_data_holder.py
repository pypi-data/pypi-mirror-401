import unittest

from looqbox_commons.src.main.data_holder.key import KeyCreator

from looqbox_commons.src.main.data_holder.data_holder import DataHolder


@KeyCreator.delegate
class DelegationsTest:
    MY_KEY: str


class TestDataHolder(unittest.TestCase):
    def setUp(self) -> None:
        self.message = DataHolder()

    def test_offer_accepted(self):
        try:
            self.message[DelegationsTest.MY_KEY] = "test"
        except TypeError as e:
            self.fail("Typechecking failed: " + str(e))

    def test_offer_failed(self):
        self.assertRaises(TypeError, self.message.__setitem__, DelegationsTest.MY_KEY, 1)

    def test_key_querying(self):
        self.message[DelegationsTest.MY_KEY] = "test"
        my_key = self.message.get(DelegationsTest.MY_KEY)
        self.assertEqual(my_key, "test")
