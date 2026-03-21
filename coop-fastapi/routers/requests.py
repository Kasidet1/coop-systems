from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from dependencies import get_current_user
from utils.notification_service import create_notification

import models
import schemas

router = APIRouter(
    prefix="/requests",
    tags=["Internship Requests"]
)

# ======================
# ฟังก์ชันช่วยดึงชื่อเต็มนักศึกษา
# ======================
def get_student_full_name(student_id: str, db: Session):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if student:
        return f"{student.first_name} {student.last_name}"
    return None

# ======================
# ดูคำร้อง (รวมข้อมูลบริษัท)
# ======================
@router.get("/")
def get_requests(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] in ["admin", "teacher"]:
        requests = db.query(models.InternshipRequest)\
            .options(joinedload(models.InternshipRequest.company))\
            .filter(models.InternshipRequest.status.in_(["อนุมัติ", "รอการนิเทศ"]))\
            .all()
    elif current_user["role"] == "student":
        requests = db.query(models.InternshipRequest)\
            .options(joinedload(models.InternshipRequest.company))\
            .filter(
                models.InternshipRequest.student_id == current_user["username"],
                models.InternshipRequest.status.in_(["อนุมัติ", "รอการนิเทศ"])
            ).all()
    else:
        raise HTTPException(status_code=403, detail="Invalid role")

    result = []
    for r in requests:
        company = r.company
        result.append({
            "request_id": r.request_id,
            "student_id": r.student_id,
            "student_name": r.student_name,
            "company_id": r.company_id,
            "company_name": company.company_name if company else r.company_name,
            "contact_person": company.contact_person if company else None,
            "email": company.email if company else None,
            "phone": company.phone if company else None,
            "address": company.address if company else None,
            "status": r.status,
            "can_mark_done": r.status == "รอการนิเทศ",  # ✅ ปุ่ม “นิเทศแล้ว” จะแสดงเฉพาะรอนิเทศ
            "created_at": r.created_at
        })
    return result

# ======================
# นักศึกษายื่นคำร้อง
# ======================
@router.post("/")
def create_request(
    data: schemas.RequestCreate,  # ตอนนี้ต้องมี company_id
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can create request")

    student_id = current_user["username"]

    student_name = get_student_full_name(student_id, db)
    if not student_name:
        raise HTTPException(status_code=404, detail="Student name not found")

    existing = db.query(models.InternshipRequest).filter(
        models.InternshipRequest.student_id == student_id,
        models.InternshipRequest.status == "รอการอนุมัติ"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="คุณได้ยื่นคำร้องแล้ว")

    # 🔹 ดึงบริษัทจาก DB
    company = db.query(models.Company).filter(models.Company.company_id == data.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    new_request = models.InternshipRequest(
        student_id=student_id,
        student_name=student_name,
        company_id=company.company_id,
        company_name=company.company_name,
        status="รอการอนุมัติ"
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    create_notification(
        db,
        student_id,
        f"คุณได้ยื่นคำร้องฝึกงานกับบริษัท {company.company_name}"
    )

    return new_request

# ======================
# อนุมัติคำร้อง
# ======================
@router.put("/{request_id}/approve")
def approve_request(
    request_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can approve")

    request = db.query(models.InternshipRequest).filter(
        models.InternshipRequest.request_id == request_id
    ).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request.status = "อนุมัติ"
    db.commit()

    create_notification(
        db,
        request.student_id,
        "คำร้องฝึกงานของคุณได้รับการอนุมัติ"
    )

    return {"message": "อนุมัติเรียบร้อย"}

# ======================
# ปฏิเสธคำร้อง
# ======================
@router.put("/{request_id}/reject")
def reject_request(
    request_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can reject")

    request = db.query(models.InternshipRequest).filter(
        models.InternshipRequest.request_id == request_id
    ).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request.status = "ไม่อนุมัติ"
    db.commit()

    create_notification(
        db,
        request.student_id,
        "คำร้องฝึกงานของคุณไม่ได้รับการอนุมัติ"
    )

    return {"message": "ไม่อนุมัติ"}

# ======================
# Dashboard Statistics
# ======================
@router.get("/stats")
def get_request_stats(
    db: Session = Depends(get_db)
):
    pending = db.query(models.InternshipRequest).filter(
        models.InternshipRequest.status == "รอการอนุมัติ"
    ).count()
    approved = db.query(models.InternshipRequest).filter(
        models.InternshipRequest.status == "อนุมัติ"
    ).count()
    rejected = db.query(models.InternshipRequest).filter(
        models.InternshipRequest.status == "ไม่อนุมัติ"
    ).count()

    total = pending + approved + rejected

    return {
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
        "total": total
    }

# ======================
# คำร้องล่าสุด (Dashboard)
# ======================
@router.get("/latest")
def get_latest_requests(
    db: Session = Depends(get_db)
):
    requests = db.query(models.InternshipRequest)\
        .order_by(models.InternshipRequest.created_at.desc())\
        .limit(3)\
        .all()

    result = []
    for r in requests:
        company = r.company
        result.append({
            "student_name": r.student_name,
            "company_name": company.company_name if company else r.company_name,
            "contact_person": company.contact_person if company else None,
            "email": company.email if company else None,
            "phone": company.phone if company else None,
            "address": company.address if company else None,
            "status": r.status
        })

    return result

@router.put("/{request_id}/done")
def mark_done(
    request_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="Only teachers or admin can mark done")

    request = db.query(models.InternshipRequest).filter(
        models.InternshipRequest.request_id == request_id
    ).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if request.status != "รอการนิเทศ":
        raise HTTPException(status_code=400, detail="Cannot mark this request as done")

    request.status = "นิเทศแล้ว"
    db.commit()

    create_notification(
        db,
        request.student_id,
        f"นิเทศนักศึกษาของคุณ {request.student_name} เสร็จเรียบร้อย"
    )

    return {"message": "สถานะนิเทศเรียบร้อย"}