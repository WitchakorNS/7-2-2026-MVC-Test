from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from datetime import datetime, timedelta
from random import choice

from rumor_tracker import create_app
from rumor_tracker.extensions import db
from rumor_tracker.models import User, Rumour, Report
from rumor_tracker.services.rumour_service import update_panic_status_if_needed

app = create_app()

def seed():
    users = [
        User(id=1, name="Alice", role="general"),
        User(id=2, name="Bob", role="general"),
        User(id=3, name="Chai", role="general"),
        User(id=4, name="Dara", role="general"),
        User(id=5, name="Eak", role="general"),
        User(id=6, name="Fah", role="general"),
        User(id=7, name="Gus", role="general"),
        User(id=8, name="Hana", role="general"),
        User(id=9, name="Ivy", role="checker"),
        User(id=10, name="Jom", role="checker"),
    ]

    base_time = datetime.utcnow() - timedelta(days=2)
    rumours = [
        Rumour(id="12345678", title="มีการปิดห้างทั่วประเทศพรุ่งนี้", source="Facebook", created_at=base_time + timedelta(hours=1), credibility_score=0.20),
        Rumour(id="23456789", title="น้ำมันจะขึ้นราคา 20 บาทในคืนนี้", source="Twitter", created_at=base_time + timedelta(hours=2), credibility_score=0.30),
        Rumour(id="34567890", title="มีแผ่นดินไหวใหญ่คืนนี้แน่นอน", source="LINE", created_at=base_time + timedelta(hours=3), credibility_score=0.15),
        Rumour(id="45678901", title="แจกเงินดิจิทัลรอบใหม่เริ่มสัปดาห์หน้า", source="TikTok", created_at=base_time + timedelta(hours=4), credibility_score=0.55),
        Rumour(id="56789012", title="โรงเรียนหยุดฉุกเฉิน 7 วัน", source="Facebook", created_at=base_time + timedelta(hours=5), credibility_score=0.25),
        Rumour(id="67890123", title="พบอาหารปนเปื้อนในซูเปอร์ดัง", source="Instagram", created_at=base_time + timedelta(hours=6), credibility_score=0.35),
        Rumour(id="78901234", title="รถไฟฟ้าฟรีตลอดเดือนนี้", source="Twitter", created_at=base_time + timedelta(hours=7), credibility_score=0.40),
        Rumour(id="89012345", title="ประกาศงดใช้เงินสดในบางจังหวัด", source="News Blog", created_at=base_time + timedelta(hours=8), credibility_score=0.10),
    ]

    db.session.add_all(users)
    db.session.add_all(rumours)
    db.session.commit()

    def add_report(reporter_id, rumour_id, report_type):
        db.session.add(Report(reporter_id=reporter_id, rumour_id=rumour_id, report_type=report_type))

    # PANIC_THRESHOLD = 3 => panic when reports > 3 (i.e. 4+)
    for uid in [1,2,3,4]:
        add_report(uid, "34567890", choice(["fake","incitement","distortion"]))
    for uid in [1,2,3,4,5]:
        add_report(uid, "89012345", choice(["fake","incitement","distortion"]))

    add_report(1, "12345678", "fake")
    add_report(2, "12345678", "fake")
    add_report(3, "23456789", "distortion")
    add_report(4, "23456789", "incitement")
    add_report(5, "45678901", "distortion")

    db.session.commit()

    threshold = app.config["PANIC_THRESHOLD"]
    for r in Rumour.query.all():
        update_panic_status_if_needed(r, threshold)

    # verified true & false for summary page
    r_true = Rumour.query.get("45678901")
    r_true.is_verified = True
    r_true.verified_as = "true"
    r_true.verified_at = datetime.utcnow() - timedelta(hours=1)
    r_true.verified_by_user_id = 9

    r_false = Rumour.query.get("12345678")
    r_false.is_verified = True
    r_false.verified_as = "false"
    r_false.verified_at = datetime.utcnow() - timedelta(hours=2)
    r_false.verified_by_user_id = 10

    db.session.commit()
    print("✅ Seeded sample data.")

with app.app_context():
    seed()
