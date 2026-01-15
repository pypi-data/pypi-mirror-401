import importlib
import inspect
import os
from collections import OrderedDict
from pathlib import Path

from looqbox_commons.src.main.logger.logger import RootLogger

log = RootLogger().get_new_logger("commons")


class IoC:
    beans = dict()
    root_dir = "."
    possible_annotations = ["@Configuration", "@Component"]

    @classmethod
    def start(cls):
        ignore_patterns = ["venv", ".idea", ".test.py", "build", "dist", ".egg-info", "site-packages", ".json", ".git", "__pycache__"]
        cls.import_all_modules(root_dir=cls.root_dir, ignore_patterns=ignore_patterns)
        cls.start_all_modules()

    @staticmethod
    def is_ignored(path, ignore_patterns) -> bool:
        return any(pattern in str(path) for pattern in ignore_patterns)

    @classmethod
    def get_module_name_from_path(cls, path):
        rel_path = os.path.relpath(path, cls.root_dir).replace(os.sep, '.')
        module_name, _ = os.path.splitext(rel_path)
        return module_name

    @classmethod
    def import_module_from_path(cls, file_path):
        with open(file_path) as file:
            try:
                file_txt = file.read()
            except UnicodeDecodeError:
                return
        file.close()

        if any(annotation in file_txt for annotation in cls.possible_annotations):
            module_name = cls.get_module_name_from_path(file_path)
            try:
                log.info(f"Importing {module_name}")
                importlib.import_module(module_name)
            except Exception as e:
                log.info(f"Failed to import {module_name}: {e}")

    @classmethod
    def import_all_modules(cls, root_dir: str | Path = ".", ignore_patterns=None):
        if not isinstance(root_dir, Path):
            root_dir = Path(root_dir)
        for file in root_dir.iterdir():
            if file.is_dir():
                if cls.is_ignored(file, ignore_patterns or []):
                    continue
                cls.import_all_modules(file, ignore_patterns)
            else:
                if str(file).endswith('.py') and not cls.is_ignored(file, ignore_patterns):
                    cls.import_module_from_path(file)

    @classmethod
    def start_all_modules(cls):
        cls.order_beans()
        for clz, bean in cls.beans.items():
            clz.start(cls, bean)

    @classmethod
    def order_beans(cls):
        def get_bean_place(bean):
            bean_name = bean[0].__class__.__name__
            if bean_name in cls.possible_annotations:
                return cls.possible_annotations.index("@" + bean_name)
            return len(cls.possible_annotations)

        cls.beans = OrderedDict(sorted(cls.beans.items(), key=lambda bean: get_bean_place(bean)))

    @classmethod
    def accept(cls, dict_to_accept):
        cls.beans.update(dict_to_accept)

    @classmethod
    def get_injections(cls, obj):
        instance_fun = obj.__init__
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            instance_fun = obj
        sig = inspect.signature(instance_fun)
        kwargs = {}
        for name, param in sig.parameters.items():
            if name == 'self' or IoC._inspection_is_empty(param):
                continue
            annotation = instance_fun.__annotations__[name]
            if hasattr(annotation, "child_class"):
                annotation = annotation.child_class
            kwargs[name] = cls._get_dependency(annotation, obj)
        return kwargs

    @classmethod
    def _inspection_is_empty(cls, param):
        return param.annotation == param.empty

    @classmethod
    def is_function_or_method(cls, element):
        return inspect.isfunction(element) or inspect.ismethod(element)

    @classmethod
    def append(cls, app):
        cls.app = app
        return cls

    @classmethod
    def _get_dependency(cls, annotation, obj):

        if annotation == obj:
            raise RuntimeError(f"Circular dependency detected for service {obj.__name__}")

        instantiated_beans = [bean for bean in cls.beans.values() if type(bean) != type]
        dependency_dict = {bean.__class__: bean for bean in instantiated_beans}

        if annotation in dependency_dict.keys():
            return dependency_dict[annotation]

        try:
            if annotation in cls.beans.keys():
                return cls.beans[annotation].start(cls, cls.beans[annotation])
        except RuntimeError:
            raise RuntimeError(f"Dependency {annotation} not found for object {obj.__name__}")

    @classmethod
    def instance(cls, obj_type):
        if obj_type in cls.beans.keys():
            return cls.beans[obj_type]
        instance = obj_type(**cls.get_injections(obj_type))
        cls.beans[obj_type] = instance
        return instance
