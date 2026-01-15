import copy
from typing import TypeVar, Optional, Tuple, List, cast

from looqbox_commons.src.main.data_holder.key_creator import KeyCreator
from looqbox_commons.src.main.logger.logger import RootLogger

T = TypeVar("T")
logger = RootLogger().get_new_logger("looqbox_commons")


class DataHolder:

    def __init__(self):
        self.class_values = dict(self.__dict__)

    def __getitem__(self, item: T, default: Optional[T] = None) -> Optional[T]:
        return self.get(item, default)

    def get(self, item: T, default: Optional[T] = None) -> Optional[T]:
        if default is not None:
            logger.warning("The use of default arguments inside `get` is deprecated. Please use `get_or_default`")

        if not isinstance(item, str):
            raise ValueError("The key to retrieve dataholder items must be of type 'str'")
        return copy.deepcopy(self.class_values.get(item, default))

    def get_or_raise(self, item: T) -> T:
        value = self.get(item)
        if value is None:
            raise KeyError(f"Error: The key '{item}' is not contained inside the dataholder.")
        return copy.deepcopy(value)

    def get_or_default(self, item: T, default: T) -> T:
        result = self.get(item)
        if result is not None:
            return result
        return default

    def append_to_list(self, key: List[T], item: T) -> None:
        current = self.get_or_default(key, [])
        current.append(item)
        self.__setitem__(key, current)

    def offer(self, *pairs: Tuple[T, T]):
        """
        Offer pairs of key and value to the data_holder.

        Example:
         data_holder.offer(
            (DataHolderKeys.CONTEXT_INFO, context_info),
            (DataHolderKeys.SCRIPT_PARAMS, script_params)
        )
        """
        first_child = next(iter(pairs))
        if first_child is None:
            raise ValueError("You cannot offer a None value.")
        if len(first_child) != 2:
            raise IndexError("The tuple you are offering contains length greater then two (it must be two).")

        if not isinstance(first_child, tuple):
            pairs_ = (pairs,)
            pairs = cast(Tuple[Tuple[T, T]], pairs_)

        for current_tuple in pairs:
            key, value = current_tuple
            self.__setitem__(key, value)

    def __setitem__(self, key: T, value: T):
        if not isinstance(key, str):
            raise ValueError("The key to retrieve dataholder items must be of type 'str'")
        key_type = KeyCreator.get_type(key)
        key_type_name = key_type and key_type.__name__ or "None"

        required_type = key_type.lower() if isinstance(key_type, str) else key_type_name.lower()
        if required_type not in {"any", "optional"} and required_type != type(value).__name__.lower():
            raise TypeError(
                f"Value provided for key {key} must be of type {key_type_name} not {type(value).__name__}")
        self.class_values[key] = value
