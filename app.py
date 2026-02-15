import streamlit as st
import os

# --- 設定・関数定義 ---
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
                articles.append({"title": title, "content": content})
    return articles

# --- 画面構成 ---
st.set_page_config(page_title="my-st-blog", layout="centered")
st.title("🗨️個人ブログ")
st.caption("色々書きます")

# サイドバー
with st.sidebar:
    st.markdown("### リンク")
    st.write("🔗 [ロリータパヤオ](https://lolitapayao.neocities.org/)")
    st.write("🔗 [私のかわいい宝石たち。](https://mycutiejewels.neocities.org)")

# タブ作成
tab1, tab2, tab3 = st.tabs(["怖い話", "雑談", "技術"])

# 各カテゴリーの処理を一括化するための設定
categories = [
    {"tab": tab1, "key": "kowai", "label": "怖い話"},
    {"tab": tab2, "key": "zatudan", "label": "雑談"},
    {"tab": tab3, "key": "gijutsu", "label": "技術"}
]

for cat in categories:
    with cat["tab"]:
        st.header(cat["label"])
        
        # ファイルから記事を読み込み
        articles = load_articles(cat["key"])
        
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
            
            if st.button("← 記事一覧に戻る", key=f"bottom_{cat['key']}_back"):
                st.session_state[session_key] = None
                st.rerun()