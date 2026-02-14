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
    st.markdown("### リンク")
    st.write("🔗 [ロリータパヤオ](https://lolitapayao.neocities.org/)")
    st.divider()
    st.markdown("### 目次")
    st.write("怖い話")
    st.write("雑談")
    st.write("技術")
    st.divider()
    st.expander("怖い話")
    st.expander("雑談")
    st.expander("技術")

# カテゴリータブの作成
tab1, tab2, tab3 = st.tabs(["怖い話", "雑談", "技術"])

# --- 怖い話 ---
with tab1:
    st.header("怖い話")
    st.write("怖い話を書きます")            

    stories = [
        {"title": "リアル", "content": "これ怖いよね"}, 
        {"title": "パラレルワールド", "content": '''ある朝、鏡の中に自分以外のなにかが...<br>
<iframe width="560" height="315" src="https://www.youtube.com/embed/ovq9sdDpRJk?si=1EeQ89rSS05V3Gw_" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
''' }
    ]

    if "kowai_selected" not in st.session_state:
        st.session_state.kowai_selected = None

    # 記事リンクの表示
    for i, story in enumerate(stories):
        if st.button(story["title"], key=f"kowai_{i}"):
            st.session_state.kowai_selected = i

    st.divider()

    # 記事表示
    if st.session_state.kowai_selected is not None:
        post = stories[st.session_state.kowai_selected]
        st.subheader(post["title"])
        st.write(post["content"])
        if st.button("← 記事一覧に戻る", key="kowai_back"):
            st.session_state.kowai_selected = None

# --- 雑談 ---
with tab2:
    st.header("雑談")
    st.write("雑談を書きます")

    chats = [
        {"title": "最近ハマってるゲーム", "content": "最近は○○というゲームに夢中です！"}, 
        {"title": "おすすめのカフェ", "content": "駅前に新しくできたカフェがすごく良かった話"}
    ]

    if "zatudan_selected" not in st.session_state:
        st.session_state.zatudan_selected = None

    for i, chat in enumerate(chats):
        if st.button(chat["title"], key=f"zatudan_{i}"):
            st.session_state.zatudan_selected = i

    st.divider()

    if st.session_state.zatudan_selected is not None:
        post = chats[st.session_state.zatudan_selected]
        st.subheader(post["title"])
        st.write(post["content"])
        if st.button("← 記事一覧に戻る", key="zatudan_back"):
            st.session_state.zatudan_selected = None

# --- 技術 ---
with tab3:
    st.header("技術")
    st.write("技術を書きます")

    techs = [
        {"title": "PythonでWebアプリ", "content": "Streamlitで簡単にWebアプリが作れます！"}, 
        {"title": "Docker入門", "content": "Dockerを使ってみたメモ"}
    ]

    if "gijutsu_selected" not in st.session_state:
        st.session_state.gijutsu_selected = None

    for i, tech in enumerate(techs):
        if st.button(tech["title"], key=f"gijutsu_{i}"):
            st.session_state.gijutsu_selected = i

    st.divider()

    if st.session_state.gijutsu_selected is not None:
        post = techs[st.session_state.gijutsu_selected]
        st.subheader(post["title"])
        st.write(post["content"])
        if st.button("← 記事一覧に戻る", key="gijutsu_back"):
            st.session_state.gijutsu_selected = None