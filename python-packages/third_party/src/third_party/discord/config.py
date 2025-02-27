import pydantic
import pydantic_settings


class Config(pydantic_settings.BaseSettings):
    dev_webhook: str = pydantic.Field(...)
    schedule_webhook: str = pydantic.Field(...)
    weather_webhook: str = pydantic.Field(...)

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="DISCORD_",
        env_file=[".env", ".env.dev", ".env.imgbb"],
        extra="allow",
    )


def load_config() -> Config:
    return Config()  # pylint: disable=no-value-for-parameter
