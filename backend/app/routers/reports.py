from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Report
from app.schemas import APIResponse

router = APIRouter()

@router.get("/projects/{project_id}/reports", response_model=APIResponse)
async def list_reports(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Report).where(Report.project_id == project_id).order_by(Report.generated_at.desc()))
    return APIResponse(data=[{"id": str(r.report_id), "type": r.report_type, "format": r.file_format, "generated": r.generated_at.isoformat()} for r in result.scalars().all()])
