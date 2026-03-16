from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil
import os

from database import get_db
from dependencies import get_current_user
import models

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_FOLDER = "uploads/students"

# สร้างโฟลเดอร์หลักถ้ายังไม่มี
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ======================
# ดูเอกสาร
# ======================
@router.get("/")
def get_documents(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] == "teacher":
        return db.query(models.Document).all()

    if current_user["role"] == "student":
        return db.query(models.Document).filter(
            models.Document.student_id == current_user["username"]
        ).all()

    return {"error": "invalid role"}


# ======================
# อัปโหลดเอกสาร (student)
# ======================
@router.post("/upload")
def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "student":
        return {"error": "Only student can upload document"}

    student_id = current_user["username"]

    # โฟลเดอร์ของนักศึกษา
    student_folder = f"{UPLOAD_FOLDER}/{student_id}"
    os.makedirs(student_folder, exist_ok=True)

    file_path = f"{student_folder}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_doc = models.Document(
        student_id=student_id,
        title=title,
        file_url=file_path
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {
        "message": "File uploaded successfully",
        "data": new_doc
    }


# ======================
# แก้ไขเอกสาร
# ======================
@router.put("/{document_id}")
def update_document(
    document_id: int,
    title: str = Form(...),
    file: UploadFile = File(None),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    doc = db.query(models.Document).filter(
        models.Document.document_id == document_id
    ).first()

    if not doc:
        return {"error": "Document not found"}

    if current_user["role"] != "student":
        return {"error": "Permission denied"}

    if doc.student_id != current_user["username"]:
        return {"error": "You can edit only your document"}

    doc.title = title

    if file:

        student_folder = f"{UPLOAD_FOLDER}/{current_user['username']}"
        os.makedirs(student_folder, exist_ok=True)

        file_path = f"{student_folder}/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        doc.file_url = file_path

    db.commit()
    db.refresh(doc)

    return doc


# ======================
# ลบเอกสาร
# ======================
@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    doc = db.query(models.Document).filter(
        models.Document.document_id == document_id
    ).first()

    if not doc:
        return {"error": "Document not found"}

    if current_user["role"] != "student":
        return {"error": "Permission denied"}

    if doc.student_id != current_user["username"]:
        return {"error": "You can delete only your document"}

    # ลบไฟล์ใน server
    if os.path.exists(doc.file_url):
        os.remove(doc.file_url)

    db.delete(doc)
    db.commit()

    return {"message": "Document deleted successfully"}