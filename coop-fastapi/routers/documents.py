from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# ดูเอกสาร
@router.get("/")
def get_documents(
    role: str = Query(...),
    student_id: str = Query(None),
    db: Session = Depends(get_db)
):

    # อาจารย์ดูได้ทั้งหมด
    if role == "teacher":
        return db.query(models.Document).all()

    # นักศึกษาดูได้เฉพาะของตัวเอง
    elif role == "student":
        return db.query(models.Document).filter(
            models.Document.student_id == student_id
        ).all()

    return {"error": "invalid role"}


# เพิ่มเอกสาร
@router.post("/")
def create_document(student_id: str, title: str, file_url: str, db: Session = Depends(get_db)):

    new_doc = models.Document(
        student_id=student_id,
        title=title,
        file_url=file_url
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return new_doc