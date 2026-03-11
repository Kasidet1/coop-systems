from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/")
def get_notifications(db: Session = Depends(get_db)):
    return db.query(models.Notification).all()