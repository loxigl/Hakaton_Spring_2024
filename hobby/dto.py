from pydantic import BaseModel


class Hobby(BaseModel):
    name: str

    class Config:
        from_attributes = True
