from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
import models

from routers import students, companies, requests, notifications, schedule, documents, reports

app = FastAPI(title="Coop System API")


# ======================
# Login Model
# ======================
class Login(BaseModel):
    username: str
    password: str


# ======================
# Login API
# ======================
@app.post("/login")
def login(data: Login, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        (models.User.username == data.username) |
        (models.User.student_id == data.username)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="incorrect username or password")

    if user.password != data.password:
        raise HTTPException(status_code=401, detail="incorrect username or password")

    return {
        "message": "login success",
        "username": user.username,
        "role": user.role
    }


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
