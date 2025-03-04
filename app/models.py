from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlalchemy import String, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base



class ProjectStatus(str, Enum):
    PROCESSING = "processing"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(
        SAEnum(
            ProjectStatus,
            names='project_status_enum',
        ),
        default=ProjectStatus.PROCESSING,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # relatioinship
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(
        SAEnum(
            TaskStatus,
            names='task_status_enum',
        ),
        default=TaskStatus.PENDING,
    )
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id"))

    # relatioinship
    project: Mapped[Project] = relationship(back_populates="tasks")
