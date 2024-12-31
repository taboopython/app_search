import sqlite3
import logging
from app.config import DATABASE_PATH

# ログ設定
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_db():
    """データベースの初期化"""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                query TEXT,
                url TEXT UNIQUE,
                company_name TEXT,
                status TEXT
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"データベースの初期化エラー: {e}")
        conn.rollback()
    finally:
        conn.close()

def save_to_db(query, results):
    """検索結果をデータベースに保存"""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()
        new_results = []
        for url, company_name in results:
            try:
                cursor.execute("""
                    INSERT INTO history (date, query, url, company_name, status)
                    VALUES (datetime('now', 'localtime'), ?, ?, ?, 'unseen')
                """, (query, url, company_name))
                new_results.append((url, company_name))
            except sqlite3.IntegrityError:
                logging.warning(f"重複エントリのためスキップ: {url}")
        conn.commit()
        return new_results
    except sqlite3.Error as e:
        logging.error(f"データ保存エラー: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_seen_urls():
    """既にチェックされたURLを取得"""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM history WHERE status = 'seen'")
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        logging.error(f"URL取得エラー: {e}")
        return []
    finally:
        conn.close()

def mark_as_seen(urls):
    """指定されたURLをチェック済みにする"""
    if not urls:
        return
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()
        placeholders = ', '.join(['?'] * len(urls))
        cursor.execute(f"UPDATE history SET status = 'seen' WHERE url IN ({placeholders})", urls)
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"URL更新エラー: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_today_history():
    """本日の履歴を取得"""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM history
            WHERE date(date) = date('now', 'localtime')
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"履歴取得エラー: {e}")
        return []
    finally:
        conn.close()
