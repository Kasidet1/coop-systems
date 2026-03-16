from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.notification_service import create_notification
from database import get_db
import models
import schemas
from dependencies import get_current_user

router = APIRouter(
    prefix="/requests",
    tags=["Internship Requests"]
)


# ======================
# ดูคำร้อง
# ======================
@router.get("/")
def get_requests(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # teacher ดูทั้งหมด
    if current_user["role"] == "teacher":
        return db.query(models.InternshipRequest).all()

    # student ดูเฉพาะของตัวเอง
    if current_user["role"] == "student":
        return db.query(models.InternshipRequest).filter(
            models.InternshipRequest.student_id == current_user["username"]
        ).all()

    return {"error": "invalid role"}


# ======================
# นักศึกษายื่นคำร้อง
# ======================
@router.post("/")
def create_request(
    data: schemas.RequestCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "student":
        return {"error": "Only students can create request"}

    new_request = models.InternshipRequest(
        student_id=current_user["username"],
        company_name=data.company_name,
        status="รอการอนุมัติ"
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    # notification
    create_notification(
        db,
        current_user["username"],
        f"คุณได้ยื่นคำร้องฝึกงานกับบริษัท {data.company_name}"
    )

    return new_request


# ======================
# อาจารย์อนุมัติคำร้อง
# ======================
@router.put("/{request_id}/approve")
def approve_request(
    request_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "teacher":
        return {"error": "Only teacher can approve request"}

    request = db.query(models.InternshipRequest).filter(
        models.InternshipRequest.request_id == request_id
    ).first()

    if not request:
        return {"error": "Request not found"}

    request.status = "อนุมัติ"
    db.commit()

    create_notification(
        db,
        request.student_id,
        "คำร้องฝึกงานของคุณได้รับการอนุมัติ"
    )

    return {"message": "อนุมัติเรียบร้อย"}


# ======================
# อาจารย์ปฏิเสธคำร้อง
# ======================
@router.put("/{request_id}/reject")
def reject_request(
    request_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if current_user["role"] != "teacher":
        return {"error": "Only teacher can reject request"}

    request = db.query(models.InternshipRequest).filter(
        models.InternshipRequest.request_id == request_id
    ).first()

    if not request:
        return {"error": "Request not found"}

    request.status = "ไม่อนุมัติ"
    db.commit()

    create_notification(
        db,
        request.student_id,
        "คำร้องฝึกงานของคุณไม่ได้รับการอนุมัติ"
    )

    return {"message": "ไม่อนุมัติ"}