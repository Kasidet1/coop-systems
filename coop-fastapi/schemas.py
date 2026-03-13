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


# -----------------
# Company
# -----------------
class CompanyCreate(BaseModel):
    company_name: str
    contact_person: str
    email: str
    phone: str
    address: str


class CompanyResponse(CompanyCreate):
    company_id: int


# -----------------
# Internship Request
# -----------------
class RequestCreate(BaseModel):
    student_id: str
    company_name: str


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