# 軽量なPythonイメージを使用
FROM python:3.11-slim

# コンテナ内の作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt .

# ライブラリのインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリのコードをコピー
COPY . .

# Streamlitのデフォルトポート8501を開放
EXPOSE 8501

# 起動コマンド
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]