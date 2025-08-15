# schemas.py
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, computed_field

class FileBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    filename: str
    public_url: Optional[str] = None

    # берём из ORM, но не выводим в ответ
    project_name: Optional[str] = Field(None, exclude=True)

    @computed_field(alias="project", return_type=Optional[str])
    def project(self) -> Optional[str]:
        return self.project_name