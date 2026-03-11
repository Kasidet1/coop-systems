from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# ดูเอกสารทั้งหมด
@router.get("/")
def get_documents(db: Session = Depends(get_db)):
    return db.query(models.Document).all()

# ดูเอกสารตาม student
@router.get("/student/{student_id}")
def get_student_documents(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.Document).filter(models.Document.student_id == student_id).all()

# เพิ่มเอกสาร
@router.post("/")
def create_document(student_id: int, title: str, file_url: str, db: Session = Depends(get_db)):
    new_doc = models.Document(
        student_id=student_id,
        title=title,
        file_url=file_url
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc