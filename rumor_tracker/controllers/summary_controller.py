from flask import Blueprint, render_template
from sqlalchemy import func
from ..extensions import db
from ..models import Rumour, Report

summary_bp = Blueprint("summary", __name__)

@summary_bp.get("/summary")
def summary():
    panic_rumours = Rumour.query.filter_by(status="panic").order_by(Rumour.created_at.desc()).all()
    verified_true = Rumour.query.filter_by(is_verified=True, verified_as="true").order_by(Rumour.verified_at.desc()).all()
    verified_false = Rumour.query.filter_by(is_verified=True, verified_as="false").order_by(Rumour.verified_at.desc()).all()

    counts = dict(db.session.query(Report.rumour_id, func.count(Report.id)).group_by(Report.rumour_id).all())

    return render_template(
        "summary.html",
        panic_rumours=panic_rumours,
        verified_true=verified_true,
        verified_false=verified_false,
        counts=counts,
    )
