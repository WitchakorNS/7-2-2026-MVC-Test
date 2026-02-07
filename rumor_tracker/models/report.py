from datetime import datetime
from ..extensions import db

class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    rumour_id = db.Column(db.String(8), db.ForeignKey("rumours.id"), nullable=False)

    reported_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    report_type = db.Column(db.String(30), nullable=False)  # distortion | incitement | fake

    reporter = db.relationship("User")
    rumour = db.relationship("Rumour", back_populates="reports")

    __table_args__ = (
        db.UniqueConstraint("reporter_id", "rumour_id", name="uq_reporter_rumour"),
    )
