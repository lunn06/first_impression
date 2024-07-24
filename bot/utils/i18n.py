import os
from glob import glob

from fluent_compiler.bundle import FluentBundle  # type: ignore
from fluentogram import TranslatorHub, FluentTranslator  # type: ignore
from pydantic import DirectoryPath

from bot.configs.config import parse_config


def create_translator_hub(locales_path: DirectoryPath) -> TranslatorHub:
    locales_regex = str(locales_path) + os.sep + "**" + os.sep + "*.ftl"
    filenames = [ftl_file for ftl_file in glob(locales_regex, recursive=True)]

    translator_hub = TranslatorHub(
        {
            "ru": ("ru",),
        },
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU",
                    filenames=filenames)),
        ],
        root_locale="ru",
    )
    return translator_hub


if __name__ == '__main__':
    cfg = parse_config()
    create_translator_hub(cfg.locales_path)
