import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project, ProjectStatus, TaskStatus
from app.repositories import ProjectRepository


async def complete_project_tasks(project_id: int, session: AsyncSession) -> None:
    await asyncio.sleep(5)

    project: Project = await ProjectRepository.retrieve(
        project_id=project_id, session=session)
    project.status = ProjectStatus.IN_PROGRESS
    await session.commit()
    await session.refresh(project)

    for task in project.tasks:
        await asyncio.sleep(5)

        task.status = TaskStatus.COMPLETED
        await session.commit()

    project.status = ProjectStatus.COMPLETED
    await session.commit()
