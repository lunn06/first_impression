from enum import StrEnum
from functools import lru_cache
from typing import Optional

from environs import Env
from pydantic import SecretStr, DirectoryPath, PositiveFloat, MySQLDsn, NatsDsn, PositiveInt, Field, FilePath
from pydantic_settings import BaseSettings

env = Env()
env.read_env()


class LocationMode(StrEnum):
    buttons = "buttons"
    picture = "picture"


class Config(BaseSettings):
    bot_token: SecretStr

    debug_mode: bool
    empty_db: bool

    db_url: MySQLDsn

    nats_servers: list[NatsDsn]

    nats_delayed_consumer_subject: str
    nats_delayed_consumer_stream: str
    nats_delayed_consumer_durable_name: str

    nats_notifications_consumer_subject: str
    nats_notifications_consumer_stream: str
    nats_notifications_consumer_durable_name: str

    nats_notifications_delay: PositiveInt

    webhook_url: str
    webhook_path: str
    port: int

    flood_awaiting: PositiveFloat
    top_getting_delay: PositiveInt
    location_mode: LocationMode = Field(default=LocationMode.buttons)

    telegram_secret_token: str

    locales_path: DirectoryPath
    models_path: DirectoryPath
    map_path: Optional[FilePath]

    admins: list[int]

    # model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache(maxsize=1)
def parse_config() -> Config:
    return Config()  # type: ignore


if __name__ == "__main__":
    config = parse_config()
    print(config)
