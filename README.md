# Rumor Tracking System (MVC) — Flask + SQLite

> เวอร์ชันนี้แก้ปัญหา `ModuleNotFoundError: No module named 'rumor_tracker'` บน Windows แล้ว
> โดย `scripts/*.py` จะปรับ `sys.path` ให้อัตโนมัติ

## โครงสร้าง MVC
- Model: `rumor_tracker/models`
- View: `rumor_tracker/templates`
- Controller: `rumor_tracker/controllers`
- Business rules: `rumor_tracker/services/rumour_service.py`

## วิธีรัน (Windows PowerShell)
```powershell
python -m venv venv
.env\Scripts\Activate.ps1
pip install -r requirements.txt

python .\scripts\init_db.py
python .\scripts\seed_data.py
python .un.py
```

เปิดเว็บ: http://127.0.0.1:5000
