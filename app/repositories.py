from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from sqlalchemy.orm import joinedload

from app.models import Project, Task


class ProjectRepository:
    
    @classmethod
    async def create(cls, *, values: dict, session: AsyncSession) -> Project:
        stmt = insert(Project).values(
            **values
        ).returning(Project).options(joinedload(Project.tasks))
        result = await session.execute(stmt)
        return result.scalar_one()


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
