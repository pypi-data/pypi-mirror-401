import dataclasses
import enum
import json
import os
from dataclasses import asdict
from typing import Any, TypeVar, Type, Callable

from pydantic import TypeAdapter

from looqbox_commons.src.main.config.obj_mapper_config import ObjMapperConfig
from looqbox_commons.src.main.ioc.ioc import IoC
from looqbox_commons.src.main.ioc.model.component import Component
from looqbox_commons.src.main.object_mapper.test_model import TestModel
from looqbox_commons.src.main.path_manager.path import InternalPath, Path

T = TypeVar("T")


@Component
class ObjectMapper:
    @classmethod
    def map(cls, source: Any, target_class: Type[T]) -> T:
        return cls.validate_python(source, target_class)

    @staticmethod
    def validate_python(obj: Any, type_: Type[T]) -> T:
        return TypeAdapter(type_).validate_python(obj)

    @staticmethod
    def to_bytes(obj: Any) -> bytes:
        return TypeAdapter(type(obj)).dump_json(obj)

    @classmethod
    def to_dict(cls, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        if issubclass(type(obj), enum.Enum):
            return obj.value
        if isinstance(obj, dict):
            return {cls.to_dict(k): cls.to_dict(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [cls.to_dict(v) for v in obj]
        if dataclasses.is_dataclass(obj):
            return asdict(obj)
        return str(obj)

    @classmethod
    def to_json(cls, obj):
        return json.dumps(cls.to_dict(obj), indent=4, cls=ObjMapperConfig)


def params_to_json(json_path: str):
    mapper = IoC.instance(ObjectMapper)

    def decorator(fun: Callable):
        path_from_root = InternalPath(json_path)

        def wrapper(*args, **kwargs):
            os.makedirs(os.path.dirname(path_from_root), exist_ok=True)
            with open(str(path_from_root), "w") as file:
                file.write(json.dumps(mapper.to_dict(kwargs), indent=4, cls=ObjMapperConfig))
            result = fun(*args, **kwargs)
            return result

        return wrapper

    return decorator


def create_test_json(json_path: str, clz_conversions=None):
    mapper = IoC.instance(ObjectMapper)

    def decorator(fun: Callable):
        path_from_root = Path(str(json_path))

        def wrapper(*args, **kwargs):
            os.makedirs(os.path.dirname(path_from_root), exist_ok=True)
            with open(str(path_from_root), "w") as file:
                try:
                    result = fun(*args, **kwargs)
                except Exception as e:
                    result = e
                simplified_kwargs = {
                    key: clz_conversions.get(key, lambda it: it)(value)
                    for key, value in kwargs.items()
                }
                model = TestModel(
                    input=mapper.to_dict(simplified_kwargs),
                    expected=result
                )
                result_file = json.dumps(mapper.to_dict(model), indent=4, cls=ObjMapperConfig)
                file.write(result_file)
            result = fun(*args, **kwargs)
            return result

        return wrapper

    return decorator
