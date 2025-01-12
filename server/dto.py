import pydantic


class ScheduleData(pydantic.BaseModel):
    result: str = pydantic.Field(..., title="ocr result over image")
