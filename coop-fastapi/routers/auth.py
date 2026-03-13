from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from database import get_db
import models

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

class Login(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.username == data.username
    ).first()

    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="incorrect username or password")

    # บันทึก login log
    log = models.LoginLog(
        username=user.username,
        role=user.role,
        login_time=datetime.now()
    )

    db.add(log)
    db.commit()

    return {
        "message": "login success",
        "role": user.role
    }