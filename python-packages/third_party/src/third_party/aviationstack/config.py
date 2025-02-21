import pydantic
import pydantic_settings


class Config(pydantic_settings.BaseSettings):
    api_key: str = pydantic.Field(...)

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="AS_",
        env_file=[".env", ".env.dev", ".env.aviation"],
        extra="allow",
    )


def load_config() -> Config:
    return Config()  # pylint: disable=no-value-for-parameter
