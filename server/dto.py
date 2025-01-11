import pydantic


class ImageData(pydantic.BaseModel):
    img_base64: str = pydantic.Field(..., title="base64 encoded image data")
