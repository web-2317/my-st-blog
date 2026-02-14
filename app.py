import streamlit as st

# ページの設定
st.set_page_config(page_title="my-st-blog", layout="centered")

# タイトル
st.title("🗨️個人ブログ")
st.caption("色々書きます")

# サイドバー（プロフィールやリンクなど）
with st.sidebar:
    st.markdown("### このサイトについて")
    st.write("色々書きます")
    st.divider()
    st.write("🔗 [ロリータパヤオ](https://lolitapayao.neocities.org/)")

# カテゴリータブの作成
tab1, tab2, tab3 = st.tabs(["怖い話", "雑談", "技術"])

with tab1:
    st.header("怖い話")
    st.write("怖い話を書きます")

with tab2:
    st.header("雑談")
    st.write("雑談を書きます")

with tab3:
    st.header("技術")
    st.write("技術を書きます")