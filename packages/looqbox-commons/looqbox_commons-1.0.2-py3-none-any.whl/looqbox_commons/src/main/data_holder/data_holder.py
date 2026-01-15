import copy
from typing import TypeVar

from looqbox_commons.src.main.data_holder.key_creator import KeyCreator

T = TypeVar("T")


class DataHolder:
    def __getitem__(self, item: T, default: T = None) -> T:
        return copy.deepcopy(self.__dict__.get(item, default))

    def get(self, item: T, default: T = None) -> T:
        return copy.deepcopy(self.__dict__.get(item, default))

    def offer(self, *pairs: tuple[T, T]):
        """
        Offer pairs of key and value to the data_holder.

        Example:
         data_holder.offer(
            (DataHolderKeys.CONTEXT_INFO, context_info),
            (DataHolderKeys.SCRIPT_PARAMS, script_params)
        )
        """
        if not isinstance(next(iter(pairs)), tuple):
            pairs = (pairs,)
        for key, value in pairs:
            self.__setitem__(key, value)

    def __setitem__(self, key: T, value: T):
        key_type = KeyCreator.get_type(key)
        required_type = key_type.lower() if isinstance(key_type, str) else key_type.__name__.lower()
        if required_type not in {"any", "optional"} and required_type != type(value).__name__.lower():
            raise TypeError(
                f"Value provided for key {key} must be of type {key_type.__name__} not {type(value).__name__}")
        self.__dict__[key] = value
