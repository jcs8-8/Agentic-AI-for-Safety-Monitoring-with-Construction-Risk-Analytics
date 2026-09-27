from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import socketio

from app.database import engine, Base
from app.routers import projects, site_risks, dashboard, agents, alerts, safety, compliance, insurance, reports, copilot, emergencies, front_desk
from app.auth import router as auth_router
from app.socket import sio

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

fastapi_app = FastAPI(title="BuildSure AI", description="Agentic Construction Risk Intelligence Platform", version="1.0.0", lifespan=lifespan)

fastapi_app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

fastapi_app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth"])
fastapi_app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
fastapi_app.include_router(site_risks.router, prefix="/api/v1", tags=["Site Risks"])
fastapi_app.include_router(safety.router, prefix="/api/v1", tags=["Safety"])
fastapi_app.include_router(compliance.router, prefix="/api/v1", tags=["Compliance"])
fastapi_app.include_router(insurance.router, prefix="/api/v1", tags=["Insurance"])
fastapi_app.include_router(reports.router, prefix="/api/v1", tags=["Reports"])
fastapi_app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])
fastapi_app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
fastapi_app.include_router(alerts.router, prefix="/api/v1", tags=["Alerts"])
fastapi_app.include_router(copilot.router, prefix="/api/v1", tags=["Copilot"])
fastapi_app.include_router(copilot.router, prefix="/api", tags=["Copilot"])
fastapi_app.include_router(emergencies.router, prefix="/api/v1", tags=["Emergencies"])
fastapi_app.include_router(front_desk.router, prefix="/api/v1", tags=["Front Desk"])

@fastapi_app.get("/health")
async def health_check():
    return {"status": "healthy", "milestone": "Milestone 3 complete", "platform": "BuildSure AI"}


app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
