from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
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
# ดูเอกสารทั้งหมด (Teacher/Admin) หรือของตัวเอง (Student)
# ======================
@router.get("/")
def get_documents(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # teacher และ admin ดูได้ทั้งหมด
    if current_user["role"] in ["teacher", "admin"]:
        documents = db.query(models.Document).all()
        # เปลี่ยน file_url ให้เป็น URL สำหรับ browser
        for doc in documents:
            doc.file_url = f"http://127.0.0.1:8000/uploads/students/{doc.student_id}/{os.path.basename(doc.file_url)}"
        return documents

    # student ดูเฉพาะของตัวเอง
    if current_user["role"] == "student":
        documents = db.query(models.Document).filter(
            models.Document.student_id == current_user["username"]
        ).all()
        for doc in documents:
            doc.file_url = f"http://127.0.0.1:8000/uploads/students/{doc.student_id}/{os.path.basename(doc.file_url)}"
        return documents

    raise HTTPException(status_code=403, detail="Invalid role")


# ======================
# ดูเอกสารของนักศึกษาเฉพาะคน (Teacher/Admin)
# ======================
@router.get("/student/{student_id}")
def get_student_documents(
    student_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    documents = db.query(models.Document).filter(
        models.Document.student_id == student_id
    ).all()

    # แปลง file_url เป็น URL สำหรับ browser
    for doc in documents:
        doc.file_url = f"http://127.0.0.1:8000/uploads/students/{student_id}/{os.path.basename(doc.file_url)}"

    return documents


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
        raise HTTPException(status_code=403, detail="Only student can upload document")

    student_id = current_user["username"]

    # โฟลเดอร์ของนักศึกษา
    student_folder = f"{UPLOAD_FOLDER}/{student_id}"
    os.makedirs(student_folder, exist_ok=True)

    file_path = f"{student_folder}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ใช้ path local แต่ browser จะเข้าถึงผ่าน URL
    new_doc = models.Document(
        student_id=student_id,
        title=title,
        file_url=file_path
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # เพิ่ม URL สำหรับส่งกลับ browser
    new_doc.file_url = f"http://127.0.0.1:8000/uploads/students/{student_id}/{file.filename}"

    return {
        "message": "File uploaded successfully",
        "data": new_doc
    }


# ======================
# แก้ไขเอกสาร (student)
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
        raise HTTPException(status_code=404, detail="Document not found")

    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Permission denied")

    if doc.student_id != current_user["username"]:
        raise HTTPException(status_code=403, detail="You can edit only your document")

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

    # แปลง file_url เป็น URL สำหรับ browser
    doc.file_url = f"http://127.0.0.1:8000/uploads/students/{doc.student_id}/{os.path.basename(doc.file_url)}"

    return doc


# ======================
# ลบเอกสาร (student)
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
        raise HTTPException(status_code=404, detail="Document not found")

    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Permission denied")

    if doc.student_id != current_user["username"]:
        raise HTTPException(status_code=403, detail="You can delete only your document")

    # ลบไฟล์ใน server
    if os.path.exists(doc.file_url):
        os.remove(doc.file_url)

    db.delete(doc)
    db.commit()

    return {"message": "Document deleted successfully"}