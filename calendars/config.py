import pydantic
import pydantic_settings


class GoogleSettings(pydantic_settings.BaseSettings):
    email: str = pydantic.Field(...)
    calendar_id: str = pydantic.Field(...)

    token: str = pydantic.Field(...)
    refresh_token: str = pydantic.Field(...)

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="GOOGLE_",
        env_file=".env.dev",
    )


def load_config():
    return GoogleSettings()  # pylint: disable=no-value-for-parameter
