from looqbox_commons.src.main.path_manager.path import Path, InternalPath
from looqbox_commons.src.main.logger.logger import RootLogger

logger = RootLogger().get_new_logger("commons")


class I18NKeyCreator:
    @staticmethod
    def delegate(instance, language, vocab_resources_path: Path):
        """
        Delegate attributes from the instance based on the language.
        """
        language = language.upper()
        vocab_path = vocab_resources_path.join(language + ".json")
        translations = vocab_path.read_json()
        logger.info(f"Loading translations for {language} language in {vocab_path}")
        class_items = dict(instance.__annotations__)
        for key in class_items.keys():
            setattr(instance, key, translations.get(key, key))
