from flask import Blueprint, current_app, request, redirect, url_for, flash
from ..services.rumour_service import create_report, verify_rumour

reports_bp = Blueprint("reports", __name__)

@reports_bp.post("/rumours/<rumour_id>/report")
def report_rumour(rumour_id: str):
    try:
        reporter_id = int(request.form.get("reporter_id",""))
    except Exception:
        flash("รหัสผู้รายงานไม่ถูกต้อง", "error")
        return redirect(url_for("rumours.rumour_detail", rumour_id=rumour_id))

    report_type = request.form.get("report_type","")
    ok, msg = create_report(
        reporter_id=reporter_id,
        rumour_id=rumour_id,
        report_type=report_type,
        panic_threshold=current_app.config["PANIC_THRESHOLD"],
    )
    flash(msg, "success" if ok else "error")
    return redirect(url_for("rumours.rumour_detail", rumour_id=rumour_id))

@reports_bp.post("/rumours/<rumour_id>/verify")
def verify_rumour_action(rumour_id: str):
    try:
        checker_id = int(request.form.get("checker_id",""))
    except Exception:
        flash("รหัสผู้ตรวจสอบไม่ถูกต้อง", "error")
        return redirect(url_for("rumours.rumour_detail", rumour_id=rumour_id))

    verified_as = request.form.get("verified_as","")
    ok, msg = verify_rumour(checker_id=checker_id, rumour_id=rumour_id, verified_as=verified_as)
    flash(msg, "success" if ok else "error")
    return redirect(url_for("rumours.rumour_detail", rumour_id=rumour_id))
