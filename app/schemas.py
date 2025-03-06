from pydantic import BaseModel, ConfigDict, Field


class TaskSchema(BaseModel):
    name: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class RetrieveProjectSchema(BaseModel):
    id: int
    name: str = Field(..., alias="project_name")
    location: str
    status: str
    tasks: list[TaskSchema]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CreateProjectSchema(BaseModel):
    project_name: str = Field(
        ..., max_length=255, alias="name", validation_alias="project_name")
    location: str = Field(..., max_length=255)
