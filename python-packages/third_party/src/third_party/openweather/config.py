import pydantic
import pydantic_settings


class OWConfig(pydantic_settings.BaseSettings):
    api_key: str = pydantic.Field(...)

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="OW_",
        env_file=[".env", ".env.dev", ".env.ow"],
        extra="allow",
    )


def load_config() -> OWConfig:
    return OWConfig()  # pylint: disable=no-value-for-parameter
