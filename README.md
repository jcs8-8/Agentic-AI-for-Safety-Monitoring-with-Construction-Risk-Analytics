# Agentic-AI-for-Safety-Monitoring-with-Construction-Risk-Analytics
Agentic AI-driven safety monitoring system designed for real-time construction risk analytics and hazard detection, developed as part of the Infosys Springboard Virtual Internship Program.

## Milestone 3: Integrated delivery and runtime validation
This milestone completes the project runtime flow for the BuildSure AI platform, including:
- FastAPI backend with authentication, project APIs, dashboard endpoints, and safety/compliance intelligence
- React + Vite frontend dashboard experience for executive, site-risk, safety, and compliance views
- Real-time socket support and agent orchestration flow for construction safety monitoring
- Verified startup and health checks for the full stack application

### Run locally
1. Start the backend in the project venv:
   `cd backend && ../.venv311/Scripts/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. Start the frontend:
   `cd frontend && npm install && npm run dev -- --host 0.0.0.0 --port 3000`
3. Open the app at http://localhost:3000

### Health check
- Backend: http://localhost:8000/health
- Frontend: http://localhost:3000
