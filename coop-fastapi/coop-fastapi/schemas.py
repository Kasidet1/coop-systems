from pydantic import BaseModel
from datetime import datetime


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


class StudentResponse(StudentCreate):
    created_at: datetime

    class Config:
        from_attributes = True


# -----------------
# Teacher
# -----------------
class TeacherCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    faculty: str


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
    student_id: str
    company_name: str


class RequestResponse(RequestCreate):
    request_id: int
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