import pydantic
import pydantic_settings


class Config(pydantic_settings.BaseSettings):
    dev_webhook: str | None = pydantic.Field(None)
    flight_webhook: str | None = pydantic.Field(None)
    weather_webhook: str | None = pydantic.Field(None)

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="DISCORD_",
        env_file=[".env", ".env.dev", ".env.imgbb"],
        extra="allow",
    )


def load_config() -> Config:
    return Config()  # pylint: disable=no-value-for-parameter
