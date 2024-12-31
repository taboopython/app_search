import sqlite3
from datetime import datetime
import webbrowser
import logging
from urllib.parse import urlparse, parse_qs, unquote
from app.search.search_duckduckgo import search_duckduckgo

# 履歴DBファイル
DB_NAME = "search_history.db"
RESULTS_FILE = "search_results.html"

# ログ設定
LOG_FILE = "application.log"
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def initialize_db():
    """履歴DBを初期化（初回実行時のみ必要）"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            query TEXT,
            url TEXT UNIQUE,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def extract_real_url(duckduckgo_url):
    """DuckDuckGoのリダイレクトリンクから実際のURLを抽出"""
    parsed_url = urlparse(duckduckgo_url)
    query_params = parse_qs(parsed_url.query)
    if 'uddg' in query_params:
        return unquote(query_params['uddg'][0])  # 実際のURLをデコードして返す
    return duckduckgo_url  # パラメータがない場合は元のURLを返す

def save_to_db(query, results):
    """新しい検索結果をDBに保存"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    new_results = []
    for url in results:
        real_url = extract_real_url(url)
        try:
            cursor.execute("""
                INSERT INTO history (date, query, url, status)
                VALUES (?, ?, ?, ?)
            """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), query, real_url, "unseen"))
            new_results.append(real_url)
        except sqlite3.IntegrityError:
            pass  # URLが既に存在する場合はスキップ
    conn.commit()
    conn.close()
    return new_results

def append_to_html(query, new_results):
    """新しい検索結果をHTMLファイルに追加保存"""
    with open(RESULTS_FILE, "a") as file:
        file.write(f"<h2>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h2>\n")
        file.write(f"<p>Query: {query}</p>\n")
        file.write("<ul>\n")
        for url in new_results:
            file.write(f'<li><a href="{url}" target="_blank">{url}</a></li>\n')
        file.write("</ul>\n")

def open_html_file():
    """HTMLファイルをブラウザで開く"""
    webbrowser.open(RESULTS_FILE)

def main():
    try:
        logging.info("プログラムを開始します。")
        query = "テナント 募集"
        initialize_db()
        logging.info("データベースを初期化しました。")

        logging.info("DuckDuckGoで検索を実行します。")
        exclude_urls = [row[0] for row in sqlite3.connect(DB_NAME).cursor().execute("SELECT url FROM history").fetchall()]
        results = search_duckduckgo(query, exclude_urls=exclude_urls)

        new_results = save_to_db(query, results)
        if new_results:
            append_to_html(query, new_results)
            logging.info(f"{len(new_results)} 件の新しい検索結果を保存しました。")
            open_html_file()
        else:
            logging.info("新しい検索結果はありません。")
            print("新しい検索結果はありません。")

    except Exception as e:
        logging.error(f"エラーが発生しました: {e}")
        print(f"エラーが発生しました: {e}")

    finally:
        logging.info("プログラムを終了します。")

if __name__ == "__main__":
    main()
