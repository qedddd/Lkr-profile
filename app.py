import streamlit as st

st.set_page_config(page_title="Quiz Challenge", layout="centered")

# 问题设置
questions = [
    {"question": "How long is my dick (answer in cm)?", "answer": "15"},
    {"question": "How many times can I have sex at one night?", "answer": "7"},
]

# 初始化状态
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.failed = False
    st.session_state.completed = False

def restart():
    st.session_state.step = 0
    st.session_state.failed = False
    st.session_state.completed = False
    st.rerun()

def show_failure():
    st.error("❌ You failed!")
    if st.button("Restart"):
        restart()

def show_success():
    st.success("🎉 Congratulations! You passed all challenges.")
    if st.button("Restart"):
        restart()

# 主逻辑
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

        answer = st.text_input("Your Answer:", key=f"answer_{curr}")

        if st.button("Submit", key=f"submit_{curr}"):
            if answer.strip() == q["answer"]:
                st.session_state.step += 1
                if st.session_state.step >= len(questions):
                    st.session_state.completed = True
                st.rerun()
            else:
                st.session_state.failed = True
                st.rerun()
