from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Alert
from app.schemas import AlertCreate, AlertResponse, APIResponse
from app.socket import sio
from app.services.notification_service import NotificationService
from app.config import get_settings

router = APIRouter()

@router.get("/projects/{project_id}/alerts", response_model=APIResponse)
async def list_alerts(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).where(Alert.project_id == project_id).order_by(Alert.created_at.desc()))
    alerts = result.scalars().all()
    return APIResponse(data=[AlertResponse.model_validate(a) for a in alerts])

@router.post("/projects/{project_id}/alerts", response_model=APIResponse)
async def create_alert(project_id: UUID, alert: AlertCreate, db: AsyncSession = Depends(get_db)):
    db_alert = Alert(**alert.model_dump(exclude={"project_id"}), project_id=project_id)
    db.add(db_alert)
    await db.flush()
    payload = AlertResponse.model_validate(db_alert)
    await sio.emit(f"new_alert:{project_id}", payload.model_dump(mode="json"), room=f"project:{project_id}")
    await NotificationService().send_alert(["dashboard", "email"], db_alert.message, [get_settings().NOTIFICATION_EMAIL] if get_settings().NOTIFICATION_EMAIL else [])
    return APIResponse(data=payload)

@router.put("/alerts/{alert_id}/acknowledge", response_model=APIResponse)
async def acknowledge_alert(alert_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).where(Alert.alert_id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        return APIResponse(success=False, message="Alert not found")
    alert.acknowledged = True
    await db.commit()
    return APIResponse(message="Alert acknowledged")

@router.get("/alerts/unread-count", response_model=APIResponse)
async def unread_alert_count(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).where(Alert.acknowledged.is_(False)))
    return APIResponse(data={"count": len(result.scalars().all())})

@router.post("/alerts/bulk-acknowledge", response_model=APIResponse)
async def bulk_acknowledge(alert_ids: list[UUID], db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).where(Alert.alert_id.in_(alert_ids)))
    alerts = result.scalars().all()
    for alert in alerts:
        alert.acknowledged = True
    await db.commit()
    return APIResponse(data={"acknowledged": len(alerts)}, message="Alerts acknowledged")
