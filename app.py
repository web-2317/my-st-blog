import streamlit as st
import os
import sqlite3
from datetime import datetime

# --- 設定 ---
DB_PATH = "articles.db"


# --- SQLite関連の関数 ---
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """記事管理用のテーブルを作成"""
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def load_db_articles(category):
    """指定カテゴリの記事をSQLiteから取得"""
    conn = get_db_connection()
    cur = conn.execute(
        "SELECT id, title, content, created_at, updated_at FROM articles WHERE category = ? ORDER BY created_at DESC",
        (category,),
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "title": row["title"],
            "content": row["content"],
            "source": "db",
        }
        for row in rows
    ]


def create_article(category, title, content):
    """記事を新規投稿（SQLite）"""
    now = datetime.utcnow().isoformat()
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO articles (category, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        (category, title, content, now, now),
    )
    conn.commit()
    conn.close()


def update_article(article_id, title, content):
    """記事を更新（SQLite）"""
    now = datetime.utcnow().isoformat()
    conn = get_db_connection()
    conn.execute(
        "UPDATE articles SET title = ?, content = ?, updated_at = ? WHERE id = ?",
        (title, content, now, article_id),
    )
    conn.commit()
    conn.close()


def delete_article(article_id):
    """記事を削除（SQLite）"""
    conn = get_db_connection()
    conn.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()


# --- 設定・関数定義（ファイル記事の読み込み） ---
def load_articles(category):
    """指定したカテゴリーフォルダ内のファイルを取得し、タイトルと中身を返す"""
    base_path = f"articles/{category}"
    articles = []

    if not os.path.exists(base_path):
        return articles

    # フォルダ内のファイルを走査
    for filename in sorted(os.listdir(base_path)):
        if filename.endswith(".txt") or filename.endswith(".md") or filename.endswith(".html"):
            path = os.path.join(base_path, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                # ファイル名（拡張子なし）をタイトルにする
                title = os.path.splitext(filename)[0]
                articles.append(
                    {
                        "title": title,
                        "content": content,
                        "source": "file",
                    }
                )
    return articles


# --- 初期化 ---
init_db()


# --- 画面構成 ---
st.set_page_config(page_title="my-st-blog", layout="centered")
st.title("🗨️個人ブログ")
st.caption("色々書きます")

# サイドバー（認証）
with st.sidebar:
    password = st.text_input("Admin Password", type="password")

    # すでにログイン済みかどうかを確認
    is_admin = st.session_state.get("is_admin", False)

    if password:
        if password == st.secrets["LOGIN_PASSWORD"]:  # パスワードはsecretsで管理
            st.session_state.is_admin = True
            is_admin = True
            st.success("パスワードが正しいです。")
        else:
            st.session_state.is_admin = False
            is_admin = False
            st.error("パスワードが間違っています。")

    st.markdown("### リンク")
    st.write("🔗 [ロリータパヤオ](https://lolitapayao.neocities.org/)")
    st.write("🔗 [私のかわいい宝石たち。](https://mycutiejewels.neocities.org)")

# タブ作成
tab1, tab2, tab3, tab4 = st.tabs(["好きな音楽", "雑談", "好きな漫画", "技術"])

# 各カテゴリーの処理を一括化するための設定
categories = [
    {"tab": tab1, "key": "music", "label": "好きな音楽"},
    {"tab": tab2, "key": "zatudan", "label": "雑談"},
    {"tab": tab3, "key": "manga", "label": "好きな漫画"},
    {"tab": tab4, "key": "gijutsu", "label": "技術"},
]

for cat in categories:
    with cat["tab"]:
        st.header(cat["label"])

        # 管理者向け：記事の新規投稿フォーム（SQLite）
        if is_admin:
            with st.expander("✏️ 新しい記事を投稿する（HTMLも使用可）", expanded=False):
                new_title = st.text_input(
                    f"タイトル（{cat['label']}）",
                    key=f"new_title_{cat['key']}",
                )
                new_content = st.text_area(
                    "本文",
                    key=f"new_content_{cat['key']}",
                    height=200,
                )
                # 入力中の内容をHTML付きでプレビュー
                with st.expander("プレビュー（HTML反映）", expanded=False):
                    if new_content:
                        st.markdown(new_content, unsafe_allow_html=True)
                    else:
                        st.caption("ここにプレビューが表示されます。HTMLタグも反映されます。")
                if st.button("投稿する", key=f"create_{cat['key']}"):
                    if new_title and new_content:
                        create_article(cat["key"], new_title, new_content)
                        st.success("記事を投稿しました。")
                        st.rerun()
                    else:
                        st.warning("タイトルと本文を入力してください。")

        # SQLiteとファイルから記事を読み込み
        db_articles = load_db_articles(cat["key"])
        file_articles = load_articles(cat["key"])
        articles = db_articles + file_articles
        
        # 状態管理用のキー
        session_key = f"{cat['key']}_selected"
        if session_key not in st.session_state:
            st.session_state[session_key] = None

        # 記事が1つもない場合
        if not articles:
            st.write("まだ記事がありません。")
        
        # 記事一覧の表示
        elif st.session_state[session_key] is None:
            for i, article in enumerate(articles):
                if st.button(article["title"], key=f"{cat['key']}_{i}"):
                    st.session_state[session_key] = i
                    st.rerun() # 状態を確定させて再描画
        
        # 記事詳細の表示
        else:
            if st.button("← 戻る", key=f"top_{cat['key']}_back"):
                st.session_state[session_key] = None
                st.rerun()

            post = articles[st.session_state[session_key]]
            st.divider()
            st.subheader(post["title"])
            # HTMLが含まれる場合を考慮して unsafe_allow_html=True
            st.markdown(post["content"], unsafe_allow_html=True) 

            # 管理者のみ、SQLite記事の編集・削除を許可
            if post.get("source") == "db" and is_admin:
                with st.expander("この記事を編集・削除する"):
                    edit_title = st.text_input(
                        "タイトル",
                        value=post["title"],
                        key=f"edit_title_{cat['key']}_{post['id']}",
                    )
                    edit_content = st.text_area(
                        "本文",
                        value=post["content"],
                        key=f"edit_content_{cat['key']}_{post['id']}",
                        height=200,
                    )
                    # 編集内容のプレビュー（HTML反映）
                    with st.expander("プレビュー（HTML反映）", expanded=False):
                        if edit_content:
                            st.markdown(edit_content, unsafe_allow_html=True)
                        else:
                            st.caption("ここにプレビューが表示されます。HTMLタグも反映されます。")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("更新する", key=f"update_{cat['key']}_{post['id']}"):
                            if edit_title and edit_content:
                                update_article(post["id"], edit_title, edit_content)
                                st.success("記事を更新しました。")
                                st.rerun()
                            else:
                                st.warning("タイトルと本文を入力してください。")
                    with col2:
                        if st.button("削除する", key=f"delete_{cat['key']}_{post['id']}"):
                            delete_article(post["id"])
                            st.success("記事を削除しました。")
                            st.session_state[session_key] = None
                            st.rerun()

            if st.button("← 記事一覧に戻る", key=f"bottom_{cat['key']}_back"):
                st.session_state[session_key] = None
                st.rerun()