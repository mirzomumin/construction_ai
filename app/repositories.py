from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload

from app.models import Project, Task


class ProjectRepository:
    
    @classmethod
    async def create(cls, *, values: dict, session: AsyncSession) -> Project:
        stmt = insert(Project).values(
            **values
        ).returning(Project).options(selectinload(Project.tasks))
        result = await session.execute(stmt)
        return result.scalar_one()
    
    @classmethod
    async def retrieve(cls, *, project_id: int, session: AsyncSession) -> Project:
        stmt = select(Project).where(
            Project.id == project_id
        ).options(selectinload(Project.tasks))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


class TaskRepository:

    @classmethod
    async def bulk_create(
        cls,
        *,
        values: list[dict],
        session: AsyncSession,
    ) -> list[Task]:
        stmt = insert(Task).values(values).returning(Task)
        result = await session.execute(stmt)
        return result.scalars().all()
