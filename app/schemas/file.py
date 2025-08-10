# schemas.py
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class FileBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # замена orm_mode=True

    filename: str
    public_url: Optional[str] = None
    # читаем из атрибута/свойства ORM "project_name", а наружу возвращаем ключ "project"
    project: Optional[str] = Field(None, validation_alias="project_name")