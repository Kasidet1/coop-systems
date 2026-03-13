from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from database import get_db
import models

from routers import students, companies, requests, notifications, schedule, documents, reports, auth

app = FastAPI(title="Coop System API")

# ======================
# Routers
# ======================
app.include_router(students.router)
app.include_router(companies.router)
app.include_router(requests.router)
app.include_router(notifications.router)
app.include_router(schedule.router)
app.include_router(documents.router)
app.include_router(reports.router)
app.include_router(auth.router)
