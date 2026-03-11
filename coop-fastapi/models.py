from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, TIMESTAMP
from database import Base

class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    major = Column(String)
    year = Column(Integer)

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True)
    company_name = Column(String)
    address = Column(Text)

class InternshipRequest(Base):
    __tablename__ = "internship_requests"

    request_id = Column(Integer, primary_key=True)
    student_id = Column(String, ForeignKey("students.student_id"))
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    status = Column(String)

class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String)
    message = Column(Text)
    is_read = Column(Boolean)

class Schedule(Base):
    __tablename__ = "schedule"

    schedule_id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)