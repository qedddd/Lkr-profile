import streamlit as st

st.set_page_config(page_title="Chat Quiz", layout="centered")

# ✅ 音效链接（你也可以换成自己的 mp3）
SUCCESS_SOUND = "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg"
FAIL_SOUND = "https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg"

def play_sound(sound_url):
    st.markdown(
        f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True,
    )

# ✅ 题库
questions = [
    {
        "question": "Lkr 什么时候出生？",
        "options": ["2000", "2001", "2002", "2003"],
        "answer": "2002"
    },
    {
        "question": "这是谁的照片？",
        "options": ["小王", "Lkr", "张三"],
        "answer": "Lkr",
        "image": "profile photo.jpg"
    },
    {
        "question": "How long is my dick (answer in cm)?",
        "answer": "15"
    },
    {
        "question": "How many times can I have sex at one night?",
        "answer": "7"
    }
]

# ✅ 初始化状态
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.failed = False
    st.session_state.completed = False
    st.session_state.history = []  # 存储所有问答历史

def restart():
    st.session_state.step = 0
    st.session_state.failed = False
    st.session_state.completed = False
    st.session_state.history = []
    # st.rerun()

# ✅ 显示历史问答记录
for entry in st.session_state.history:
    st.chat_message("assistant").markdown(entry["question"])
    if entry.get("image"):  # 修复 image 为 None 的情况
        st.image(entry["image"], caption="参考图片", use_container_width=True)
    st.chat_message("user").markdown(entry["user_answer"])

# ✅ 主流程控制
if not st.session_state.failed and not st.session_state.completed:
    curr = st.session_state.step
    q = questions[curr]

    # 当前问题展示
    with st.chat_message("assistant"):
        st.markdown(q["question"])
        if q.get("image"):
            st.image(q["image"], caption="参考图片", use_container_width=True)
        if "options" in q:
            st.markdown("选项：" + ", ".join(q["options"]))

    # 用户输入答案
    user_input = st.chat_input("请输入你的答案")

    if user_input:
        # 保存问答历史
        st.session_state.history.append({
            "question": q["question"],
            "user_answer": user_input,
            "image": q.get("image", None)
        })

        # 判断正误
        if user_input.strip() == q["answer"]:
            st.session_state.step += 1
            if st.session_state.step >= len(questions):
                st.session_state.completed = True
                play_sound(SUCCESS_SOUND)
                st.chat_message("assistant").success("🎉 恭喜你通关成功！")
                st.chat_message("assistant").button("Restart", on_click=restart)
            else:
                st.rerun()
        else:
            st.session_state.failed = True
            play_sound(FAIL_SOUND)
            st.chat_message("assistant").error("❌ 回答错误，闯关失败。")
            st.chat_message("assistant").button("Restart", on_click=restart)

# ✅ 结尾兜底 Restart（防止没按钮）
elif st.session_state.failed or st.session_state.completed:
    if st.button("Restart"):
        restart()
