from datetime import datetime
from ..extensions import db

class Rumour(db.Model):
    __tablename__ = "rumours"

    id = db.Column(db.String(8), primary_key=True)  # 8 digits, not starting 0
    title = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    credibility_score = db.Column(db.Float, nullable=False, default=0.5)

    status = db.Column(db.String(10), nullable=False, default="normal")  # normal | panic

    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    verified_as = db.Column(db.String(10), nullable=True)  # true | false
    verified_at = db.Column(db.DateTime, nullable=True)
    verified_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    reports = db.relationship("Report", back_populates="rumour", cascade="all, delete-orphan")
