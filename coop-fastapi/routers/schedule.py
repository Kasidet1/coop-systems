from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/schedule",
    tags=["Schedule"]
)

@router.get("/")
def get_schedule(db: Session = Depends(get_db)):
    return db.query(models.Schedule).all()