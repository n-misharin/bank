import os

from bank.config.default import DefaultConfig, ProductionConfig


def get_config() -> DefaultConfig:
    env = os.environ.get("ENV", "local")
    if env == "production":
        return ProductionConfig()
    return DefaultConfig()
