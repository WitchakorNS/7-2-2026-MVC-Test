import re
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Rumour, Report, User

RUMOUR_ID_RE = re.compile(r"^[1-9][0-9]{7}$")

def validate_rumour_id(rumour_id: str) -> bool:
    return bool(RUMOUR_ID_RE.match(rumour_id or ""))

def get_report_count(rumour_id: str) -> int:
    return Report.query.filter_by(rumour_id=rumour_id).count()

def update_panic_status_if_needed(rumour: Rumour, panic_threshold: int) -> None:
    count = get_report_count(rumour.id)
    if count > panic_threshold and rumour.status != "panic":
        rumour.status = "panic"
        db.session.commit()

def create_rumour(rumour_id: str, title: str, source: str, credibility_score: float):
    if not validate_rumour_id(rumour_id):
        return False, "รหัสข่าวลือต้องเป็นเลข 8 หลัก และตัวแรกห้ามเป็น 0"
    if not title.strip():
        return False, "หัวข้อข่าวห้ามว่าง"
    if not source.strip():
        return False, "แหล่งที่มาห้ามว่าง"

    try:
        score = float(credibility_score)
    except Exception:
        return False, "คะแนนความน่าเชื่อถือไม่ถูกต้อง"
    if score < 0 or score > 1:
        return False, "คะแนนความน่าเชื่อถือควรอยู่ในช่วง 0 ถึง 1"

    if Rumour.query.get(rumour_id):
        return False, "มีรหัสข่าวลือนี้อยู่แล้ว"

    rumour = Rumour(id=rumour_id, title=title.strip(), source=source.strip(), credibility_score=score, status="normal")
    db.session.add(rumour)
    db.session.commit()
    return True, "เพิ่มข่าวลือสำเร็จ"

def create_report(reporter_id: int, rumour_id: str, report_type: str, panic_threshold: int):
    rumour = Rumour.query.get(rumour_id)
    if not rumour:
        return False, "ไม่พบข่าวลือนี้"
    if rumour.is_verified:
        return False, "ข่าวลือนี้ถูกตรวจสอบแล้ว จึงไม่สามารถรายงานเพิ่มได้"

    reporter = User.query.get(reporter_id)
    if not reporter:
        return False, "ไม่พบผู้ใช้ผู้รายงาน"
    if report_type not in {"distortion", "incitement", "fake"}:
        return False, "ประเภทรายงานไม่ถูกต้อง"

    rep = Report(reporter_id=reporter_id, rumour_id=rumour_id, report_type=report_type)
    db.session.add(rep)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False, "ผู้ใช้นี้รายงานข่าวลือนี้ไปแล้ว (รายงานซ้ำไม่ได้)"

    update_panic_status_if_needed(rumour, panic_threshold)
    return True, "รายงานสำเร็จ"

def verify_rumour(checker_id: int, rumour_id: str, verified_as: str):
    rumour = Rumour.query.get(rumour_id)
    if not rumour:
        return False, "ไม่พบข่าวลือนี้"

    checker = User.query.get(checker_id)
    if not checker:
        return False, "ไม่พบผู้ตรวจสอบ"
    if checker.role != "checker":
        return False, "ผู้ใช้นี้ไม่มีสิทธิ์ตรวจสอบ (ต้องเป็นบทบาทผู้ตรวจสอบ)"

    if rumour.is_verified:
        return False, "ข่าวลือนี้ถูกตรวจสอบไปแล้ว"
    if verified_as not in {"true", "false"}:
        return False, "ค่าการยืนยันต้องเป็น true หรือ false"

    rumour.is_verified = True
    rumour.verified_as = verified_as
    rumour.verified_at = datetime.utcnow()
    rumour.verified_by_user_id = checker_id
    db.session.commit()
    return True, "ยืนยันผลสำเร็จ"
