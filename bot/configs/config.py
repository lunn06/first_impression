from functools import lru_cache

from environs import Env
from pydantic import SecretStr, MariaDBDsn, DirectoryPath, PositiveFloat, FilePath, MySQLDsn, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings

env = Env()
env.read_env()


class Config(BaseSettings):
    bot_token: SecretStr

    debug_mode: bool
    empty_db: bool
    db_url: MySQLDsn | PostgresDsn
    webhook_url: str
    webhook_path: str
    port: int
    flood_awaiting: PositiveFloat
    telegram_secret_token: str
    locales_path: DirectoryPath
    models_path: DirectoryPath
    # map_path: FilePath
    admins: list[int]
    # star_stations: list[str]
    # stations_list: list[str]
    # star_stations: list[str]
    # star_station_points: int
    # usual_station_points: int

    # model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache(maxsize=1)
def parse_config() -> Config:
    return Config()  # type: ignore


if __name__ == "__main__":
    config = parse_config()
    print(config)
