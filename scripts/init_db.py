from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from rumor_tracker import create_app
from rumor_tracker.extensions import db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ Initialized database (drop_all + create_all).")
