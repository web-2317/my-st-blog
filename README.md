# Streamlit ブログアプリケーション

個人ブログ用のStreamlitアプリケーションです。

## セットアップ

### 前提条件
- Docker Desktop がインストールされていること
- Docker Desktop が起動していること

### venv（仮想環境）について

**Dockerを使う場合**: venvは**不要**です。Dockerコンテナ内で環境が分離されているため、ローカルのPython環境に影響を与えません。

**ローカル開発で使いたい場合**: IDEの補完機能を使いたい、またはローカルで直接実行したい場合は、以下の手順でvenvを設定できます。

```bash
# Python 3.11以上がインストールされていることを確認
python3 --version

# venvを作成
python3 -m venv venv

# venvを有効化（Linux/Mac）
source venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt

# Streamlitをローカルで実行
streamlit run app.py
```

venvを無効化する場合は:
```bash
deactivate
```

### 起動方法

#### 方法1: Docker Compose を使用（推奨）

```bash
# イメージをビルドして起動
docker-compose up --build

# バックグラウンドで起動
docker-compose up -d --build

# 停止
docker-compose down
```

#### 方法2: Docker コマンドを直接使用

```bash
# イメージをビルド
docker build -t my-st-blog .

# コンテナを起動
docker run -p 8501:8501 my-st-blog

# バックグラウンドで起動
docker run -d -p 8501:8501 --name my-blog my-st-blog

# 停止
docker stop my-blog
docker rm my-blog
```

### アクセス

ブラウザで以下のURLにアクセス:
- http://localhost:8501

### 開発時の注意

`docker-compose.yml` ではボリュームマウントを設定しているため、`app.py` を編集すると自動的に反映されます（Streamlitのホットリロード機能）。

### トラブルシューティング

#### 白い画面が表示される場合

1. **ブラウザのキャッシュをクリア**
   - `Ctrl+Shift+R` (Windows/Linux) または `Cmd+Shift+R` (Mac) でハードリロード
   - または、ブラウザの開発者ツール（F12）を開いて、ネットワークタブで「キャッシュを無効にする」にチェック

2. **ブラウザのコンソールでエラーを確認**
   - 開発者ツール（F12）を開く
   - Consoleタブでエラーメッセージを確認
   - エラーがあれば、その内容を確認

3. **コンテナのログを確認**
   ```bash
   docker-compose logs -f streamlit-app
   ```

4. **コンテナを再起動**
   ```bash
   docker-compose restart
   ```

5. **完全に再ビルド**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

#### その他の問題

- ポート8501が既に使用されている場合:
  - `docker-compose.yml` の `ports` セクションを `"8502:8501"` などに変更
  - または、使用しているプロセスを停止

- イメージを再ビルドしたい場合:
  ```bash
  docker-compose build --no-cache
  ```
