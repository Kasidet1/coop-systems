from sqlalchemy.orm import Session
import models

def create_notification(db: Session, student_id: str, message: str):

    notification = models.Notification(
        student_id=student_id,
        message=message,
        is_read=False
    )

    db.add(notification)
    db.commit()