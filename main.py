from app.database.database import init_db, get_sent_urls, save_results
from app.search.search_duckduckgo import search_duckduckgo
import logging
from app.config.settings import LOG_FILE

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    try:
        # ログ: プログラム開始
        logging.info("プログラムを開始します。")

        # データベースの初期化
        logging.info("データベースを初期化します。")
        init_db()

        # 過去の送信済みURLを取得
        logging.info("送信済みのURLを取得します。")
        exclude_urls = get_sent_urls()

        # 検索実行
        logging.info("DuckDuckGoで検索を実行します。")
        results = search_duckduckgo(exclude_urls=exclude_urls)

        if results:
            # 新しい検索結果を表示
            logging.info(f"{len(results)}件の新しい検索結果が見つかりました。")
            print("新しい検索結果:")
            for result in results:
                print(f"{result['url']}")
            
            # 検索結果をデータベースに保存
            logging.info("検索結果をデータベースに保存します。")
            save_results(results)
        else:
            # 新しい結果がない場合
            logging.info("新しい検索結果はありません。")
            print("新しい検索結果はありません。")

    except Exception as e:
        # エラーが発生した場合
        logging.error(f"エラーが発生しました: {e}")
        print(f"エラーが発生しました: {e}")

    finally:
        # ログ: プログラム終了
        logging.info("プログラムを終了します。")

if __name__ == "__main__":
    main()

