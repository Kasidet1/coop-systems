from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/requests",
    tags=["Internship Requests"]
)

@router.get("/")
def get_requests(db: Session = Depends(get_db)):
    return db.query(models.InternshipRequest).all()

@router.post("/")
def create_request(data: schemas.RequestCreate, db: Session = Depends(get_db)):
    new_request = models.InternshipRequest(**data.dict())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request