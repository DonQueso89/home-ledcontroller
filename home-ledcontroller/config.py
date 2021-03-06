from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    pixel_pin: str = "D18"
    color_order: str = "GRB"
    num_leds: int = 50
    reload: bool = False

    class Config:
        env_file = ".env"

@lru_cache(maxsize=1)
def get():
    return Settings()