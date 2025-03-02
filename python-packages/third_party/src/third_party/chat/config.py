import pydantic
import pydantic_settings


class LangchainConfig(pydantic_settings.BaseSettings):
    openai_api_key: str = pydantic.Field(...)

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=[".env", ".env.dev", ".env.chat"],
        extra="allow",
    )


def load_config() -> LangchainConfig:
    return LangchainConfig()  # pylint: disable=no-value-for-parameter
