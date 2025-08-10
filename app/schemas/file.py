# schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class FileBrief(BaseModel):
    filename: str
    public_url: Optional[str] = None
    project: Optional[str] = Field(None, alias="project_name")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True