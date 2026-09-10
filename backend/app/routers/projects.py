from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectResponse, ProjectListResponse, APIResponse

router = APIRouter()

@router.get("", response_model=APIResponse)
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return APIResponse(
        data=ProjectListResponse(
            projects=[ProjectResponse.model_validate(p) for p in projects],
            total=len(projects)
        )
    )

@router.post("", response_model=APIResponse)
async def create_project(project: ProjectCreate, db: AsyncSession = Depends(get_db)):
    db_project = Project(**project.model_dump())
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return APIResponse(data=ProjectResponse.model_validate(db_project), message="Project created")

@router.get("/{project_id}", response_model=APIResponse)
async def get_project(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.project_id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return APIResponse(data=ProjectResponse.model_validate(project))
