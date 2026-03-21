from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# -----------------
# Student
# -----------------
class StudentCreate(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    faculty: str
    major: str
    year: int


class StudentResponse(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    faculty: str
    major: str
    year: int
    status: str
    company_name: Optional[str]  # <- ต้องมี

    class Config:
        from_attributes = True


# สำหรับอัปเดตสถานะนิเทศ
class InternshipStatusUpdate(BaseModel):
    status: str  # "รอนิเทศ", "นิเทศแล้ว", "พบปัญหา"


# -----------------
# Teacher
# -----------------
class TeacherCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    faculty: str | None = None


class TeacherResponse(TeacherCreate):
    teacher_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------
# Company
# -----------------
class CompanyCreate(BaseModel):
    company_name: str
    contact_person: str
    email: str
    phone: str
    address: str
    position: str


class CompanyResponse(CompanyCreate):
    company_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------
# Internship Request
# -----------------
class RequestCreate(BaseModel):
    company_id: int


class RequestResponse(BaseModel):
    request_id: int
    student_id: str
    student_name: str
    company_name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------
# Reports
# -----------------
class ReportCreate(BaseModel):
    student_id: str
    teacher_id: int
    title: str
    description: str


class ReportResponse(ReportCreate):
    report_id: int
    submitted_at: datetime

    class Config:
        from_attributes = True


# Rebuild models (FastAPI 2.x / Pydantic v2)
StudentResponse.model_rebuild()
TeacherResponse.model_rebuild()
CompanyResponse.model_rebuild()
RequestResponse.model_rebuild()
ReportResponse.model_rebuild()