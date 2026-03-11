from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    return db.query(models.Company).all()