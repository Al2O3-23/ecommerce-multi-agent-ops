import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

st.set_page_config(page_title="智能客服", page_icon="💬", layout="wide")
from config import get_llm, extract_text

st.title("智能客服话术助手")
st.caption("粘贴客户消息，AI 生成专业回复")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("客服场景")
    scene = st.radio("选择场景", ["通用客服", "退换货处理", "催付话术", "差评挽回", "售前咨询"], index=0)

    scene_system = {
        "通用客服": "你是专业抖店客服，语气亲切温和，善于解决问题。",
        "退换货处理": "你是抖店售后客服，处理退换货。态度诚恳，积极解决，尽量挽留。",
        "催付话术": "你是抖店销售客服，促成下单。热情不逼迫，善用紧迫感。",
        "差评挽回": "你是抖店客服，处理差评。先道歉安抚，再提补偿方案。",
        "售前咨询": "你是抖店售前客服，了解需求，推荐合适商品，打消顾虑。",
    }

    st.divider()
    # Quick scenarios
    st.subheader("快捷场景")
    quick_scenarios = {
        "客户要退货": "你好，我买的这个衣服尺码不合适，想退货",
        "客户催发货": "我的订单都3天了怎么还没发货？",
        "客户投诉质量": "收到的东西有质量问题，做工很差",
        "客户问尺码": "我身高165体重55公斤，穿M还是L？",
        "客户砍价": "能不能便宜点？别家都比你便宜",
    }
    for label, msg in quick_scenarios.items():
        if st.button(label, use_container_width=True, key=f"quick_{label}"):
            st.session_state.quick_msg = msg

    st.divider()
    if st.button("清空对话", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Handle quick message
if "quick_msg" in st.session_state:
    st.session_state.chat_history.append({"role": "user", "content": st.session_state.quick_msg})
    del st.session_state.quick_msg

# Chat area
chat_container = st.container(height=500, border=True)
with chat_container:
    if not st.session_state.chat_history:
        st.info("👈 选择快捷场景，或在下方输入客户消息开始对话")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("suggestion"):
                with st.expander("替换话术"):
                    st.info(msg["suggestion"])

# Input
user_input = st.chat_input("粘贴客户消息...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("生成回复中..."):
            try:
                llm = get_llm()

                history = "\n".join([
                    f"{'客户' if m['role']=='user' else '客服'}：{m['content']}"
                    for m in st.session_state.chat_history[-8:]
                ])

                prompt = f"""{scene_system[scene]}

对话记录：
{history}

回复客户最后一条消息，严格按以下格式：
【回复】
（你的回复内容，50-150字，亲切自然，像真人客服）

【替换方案】
（一个备选回复，语气或策略略有不同）"""

                response = llm.invoke(prompt)
                text = extract_text(response)

                # Parse response
                reply = ""
                alt = ""
                current = None
                for line in text.split("\n"):
                    line = line.strip()
                    if line.startswith("【回复】"):
                        current = "reply"
                        continue
                    elif line.startswith("【替换方案】"):
                        current = "alt"
                        continue
                    if current == "reply" and line:
                        reply += line
                    elif current == "alt" and line:
                        alt += line

                if not reply:
                    reply = text

                st.markdown(reply)
                if alt:
                    with st.expander("备选话术"):
                        st.info(alt)

                st.session_state.chat_history.append({
                    "role": "assistant", "content": reply, "suggestion": alt
                })

            except Exception as e:
                st.error(f"生成失败: {e}")

    st.rerun()
