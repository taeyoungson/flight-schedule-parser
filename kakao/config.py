import pydantic
import pydantic_settings


class KakaoConfig(pydantic_settings.BaseSettings):
    api_key: str = pydantic.Field(...)
    redirect_uri: str = pydantic.Field(...)
    auth_code: str = pydantic.Field(...)

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="KAKAO_",
        env_file=".env.dev",
        extra="allow",
    )


def load_config() -> KakaoConfig:
    return KakaoConfig()  # pylint: disable=no-value-for-parameter
