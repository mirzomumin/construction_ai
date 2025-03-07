import json
import httpx
import logging
from fastapi import BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.models import Project
from app.repositories import ProjectRepository, TaskRepository
from app.schemas import CreateProjectSchema
from app.tasks import complete_project_tasks


class ProjectService:

    @classmethod
    async def create(
        cls,
        *,
        payload: CreateProjectSchema,
        tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_session),
    ) -> Project:
        project_values = payload.model_dump(by_alias=True)
        logging.info(f'INPUT DATA: {project_values}')

        prompt = f"""
            List a few tasks to build a {payload.project_name} in {payload.location} in JSON format.
            Use this JSON schema:
            Task = {{"name": "str"}}
            Return: list[Task]
        """

        response_schema = {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"}
                }
            }
        }
        tasks_data = await GeminiService.generate_content(
            prompt=prompt,
            response_schema=response_schema,
        )

        try:
            project = await ProjectRepository.create(
                values=project_values, session=session)
            for task_data in tasks_data:
                task_data["project_id"] = project.id

            await TaskRepository.bulk_create(values=tasks_data, session=session)
            await session.commit()
        except Exception as e:
            logging.exception(f"Create project exception: {e}")
            await session.rollback()
            raise HTTPException(status_code=503, detail="Service Unavailable")
        await session.refresh(project)

        tasks.add_task(complete_project_tasks, project.id, session)

        logging.info(f'OUTPUT DATA: {project}')
        return project

    @classmethod
    async def retrieve(
        cls,
        *,
        project_id: int,
        session: AsyncSession = Depends(get_session),
    ) -> Project:
        try:
            project = await ProjectRepository.retrieve(
                project_id=project_id, session=session)
        except Exception as e:
            logging.exception(f'Retrieve project exception: {e}')
            raise HTTPException(status_code=503, detail="Service Unavailable")

        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")

        logging.info(f'OUTPUT DATA: {project}')
        return project


class GeminiService:
    
    @classmethod
    async def generate_content(
        cls,
        *,
        prompt: str,
        response_schema: dict | None,
    ) -> dict:
        api_key = settings.GEMINI_API_KEY
        gemini_model = settings.GEMINI_MODEL
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent"
        headers = {
            "Content-Type": "application/json",
        }
        params = {
            "key": api_key,
        }
        payload = {
            "contents": [{
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }],
            "generationConfig": {
                "response_mime_type": "application/json",
                "response_schema": response_schema,
            },
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                params=params,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        return json.loads(data['candidates'][0]['content']['parts'][0]['text'])
