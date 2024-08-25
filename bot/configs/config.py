from functools import lru_cache

from environs import Env
from pydantic import SecretStr, DirectoryPath, PositiveFloat, MySQLDsn, NatsDsn
from pydantic_settings import BaseSettings

env = Env()
env.read_env()


class Config(BaseSettings):
    bot_token: SecretStr

    debug_mode: bool
    empty_db: bool
    db_url: MySQLDsn
    nats_servers: list[NatsDsn]
    webhook_url: str
    webhook_path: str
    port: int
    flood_awaiting: PositiveFloat
    telegram_secret_token: str
    locales_path: DirectoryPath
    models_path: DirectoryPath
    admins: list[int]

    # model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache(maxsize=1)
def parse_config() -> Config:
    return Config()  # type: ignore


if __name__ == "__main__":
    config = parse_config()
    print(config)
