import os

class Config:
    SECRET_KEY = "dev-secret-key"
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "rumor_tracker.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PANIC_THRESHOLD = 3
