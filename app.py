import streamlit as st

st.set_page_config(page_title="Quiz Game", layout="centered")

# 🔊 音效（使用 Google 免费音效）
SUCCESS_SOUND = "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg"
FAIL_SOUND = "https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg"

# 播放音效
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
        "question": "How long is my dick (answer in cm)?",
        "answer": "15"
    },
    {
        "question": "How many times can I have sex at one night?",
        "answer": "7"
    },
    {
        "question": "这是谁的照片？",
        "options": ["小王", "Lkr", "张三"],
        "answer": "Lkr",
        "image": "profile photo.jpg"
    }
]

# 初始化状态
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.failed = False
    st.session_state.completed = False

# 重启函数
def restart():
    st.session_state.step = 0
    st.session_state.failed = False
    st.session_state.completed = False
    st.rerun()

# 失败页面
def show_failure():
    play_sound(FAIL_SOUND)
    st.error("❌ You failed!")
    if st.button("Restart"):
        restart()

# 胜利页面
def show_success():
    play_sound(SUCCESS_SOUND)
    st.success("🎉 Congratulations! You passed all challenges.")
    if st.button("Restart"):
        restart()

# 游戏主逻辑
if st.session_state.failed:
    show_failure()
elif st.session_state.completed:
    show_success()
else:
    curr = st.session_state.step
    if curr < len(questions):
        q = questions[curr]
        st.markdown(f"### Question {curr + 1}")
        st.write(q["question"])

        if "image" in q:
            st.image(q["image"], caption="参考图片", use_container_width=True)

        if "options" in q:
            options = ["-- 请选择 --"] + q["options"]
            user_answer = st.radio("请选择一个答案：", options, key=f"radio_{curr}")
        else:
            user_answer = st.text_input("Your Answer:", key=f"input_{curr}")

        if st.button("Submit", key=f"submit_{curr}"):
            if "options" in q and user_answer == "-- 请选择 --":
                st.warning("⚠️ 请先选择一个答案！")
            elif user_answer.strip() == q["answer"]:
                st.session_state.step += 1
                if st.session_state.step >= len(questions):
                    st.session_state.completed = True
                st.rerun()
            else:
                st.session_state.failed = True
                st.rerun()
