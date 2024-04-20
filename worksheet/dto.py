from datetime import datetime

from pydantic import BaseModel


class WorksheetDTO(BaseModel):
    given_name: str
    family_name: str
    phone_number: str
    chosen_datetime: datetime
    meeting_duration: datetime
    hobby: list[str]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class WorksheetCreateDTO(WorksheetDTO):
    pass
