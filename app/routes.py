from fastapi import APIRouter, Depends

from app.models import Project
from app.schemas import RetrieveProjectSchema
from app.services import ProjectService


router = APIRouter(prefix='/projects')


@router.post('/')
async def create_project(
    project: Project = Depends(ProjectService.create)
) -> RetrieveProjectSchema:
    return project
