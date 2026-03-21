from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from database import get_db
import models
from auth_utils import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# ======================
# Login Request Schema
# ======================
class LoginRequest(BaseModel):
    username: str
    password: str

# ======================
# Login API
# ======================
@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    # ======================
    # หา user
    # ======================
    user = db.query(models.User).filter(
        models.User.username == data.username
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid usermane or password")

    if data.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid usermane or password")


    # ======================
    # บันทึก Login Log
    # ======================
    log = models.LoginLog(
        username=user.username,
        role=user.role,
        login_time=datetime.now()
    )

    db.add(log)
    db.commit()


    # ======================
    # สร้าง JWT Token
    # ======================
    token = create_access_token({
        "user_id": user.id,
        "username": user.username,
        "role": user.role
    })


    # ======================
    # Response
    # ======================
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }