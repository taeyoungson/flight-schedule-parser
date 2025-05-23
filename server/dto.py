import pydantic


class RegisterFlightRequest(pydantic.BaseModel):
    raw_ocr_result: str = pydantic.Field(..., title="ocr result over image")
    year: int | None = pydantic.Field(None, title="year of the schedule")
    month: int | None = pydantic.Field(None, title="month of the schedule")
