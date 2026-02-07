from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from sqlalchemy import func

from ..extensions import db
from ..models import Rumour, Report, User
from ..services.rumour_service import create_rumour

rumours_bp = Blueprint("rumours", __name__)

@rumours_bp.get("/")
@rumours_bp.get("/rumours")
def rumours_list():
    report_counts = (
        db.session.query(Report.rumour_id, func.count(Report.id).label("cnt"))
        .group_by(Report.rumour_id)
        .subquery()
    )
    rows = (
        db.session.query(Rumour, func.coalesce(report_counts.c.cnt, 0).label("report_count"))
        .outerjoin(report_counts, Rumour.id == report_counts.c.rumour_id)
        .order_by(func.coalesce(report_counts.c.cnt, 0).desc(), Rumour.created_at.desc())
        .all()
    )
    return render_template("rumours_list.html", rows=rows)

@rumours_bp.get("/rumours/new")
def rumour_new_form():
    return render_template("rumour_new.html")

@rumours_bp.post("/rumours/new")
def rumour_create():
    ok, msg = create_rumour(
        rumour_id=request.form.get("rumour_id",""),
        title=request.form.get("title",""),
        source=request.form.get("source",""),
        credibility_score=request.form.get("credibility_score","0.5"),
    )
    flash(msg, "success" if ok else "error")
    return redirect(url_for("rumours.rumours_list" if ok else "rumours.rumour_new_form"))

@rumours_bp.get("/rumours/<rumour_id>")
def rumour_detail(rumour_id: str):
    rumour = Rumour.query.get_or_404(rumour_id)
    report_count = Report.query.filter_by(rumour_id=rumour_id).count()

    reports = (
        db.session.query(Report, User)
        .join(User, User.id == Report.reporter_id)
        .filter(Report.rumour_id == rumour_id)
        .order_by(Report.reported_at.desc())
        .limit(50)
        .all()
    )

    users_general = User.query.filter_by(role="general").order_by(User.id.asc()).all()
    users_checker = User.query.filter_by(role="checker").order_by(User.id.asc()).all()

    return render_template(
        "rumour_detail.html",
        rumour=rumour,
        report_count=report_count,
        reports=reports,
        users_general=users_general,
        users_checker=users_checker,
        panic_threshold=current_app.config["PANIC_THRESHOLD"],
    )
