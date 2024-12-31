# ベースイメージ
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコンテナにコピー
COPY . .

# デフォルトのエントリーポイント
CMD ["python", "main.py"]
