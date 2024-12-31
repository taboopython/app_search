import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, '../instance/search_history.db')
LOG_FILE = os.path.join(BASE_DIR, '../logs/search.log')

# 検索クエリ
SEARCH_QUERIES = [
    "テナント 募集",
    "商業施設 テナント"
]

# メール送信設定
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "False").lower() == "true"
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
