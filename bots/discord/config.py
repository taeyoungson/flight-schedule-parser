import pydantic_settings


class Config(pydantic_settings.BaseSettings):
    jarvis_bot_token: str

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="DISCORD_",
        env_file=[".env", ".env.dev", ".env.discord"],
        extra="allow",
    )


def load_config() -> Config:
    return Config()  # pylint: disable=no-value-for-parameter
