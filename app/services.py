import json
import httpx
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.models import Project, Task
from app.repositories import ProjectRepository, TaskRepository
from app.schemas import CreateProjectSchema


class ProjectService:

    @classmethod
    async def create(
        cls,
        *,
        payload: CreateProjectSchema,
        session: AsyncSession = Depends(get_session),
    ) -> Project:
        project_values = payload.model_dump(by_alias=True)
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

        print(f'TASKS DATA 1: {tasks_data}')

        project = await ProjectRepository.create(
            values=project_values, session=session)
        for task_data in tasks_data:
            task_data["project_id"] = project.id

        print(f'TASKS DATA 2: {tasks_data}')

        await TaskRepository.bulk_create(values=tasks_data, session=session)

        await session.commit()
        await session.refresh(project)
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

        print(f'GEMINI RESPONSE DATA: {data}')
        return json.loads(data['candidates'][0]['content']['parts'][0]['text'])
