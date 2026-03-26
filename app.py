import streamlit as st
import time
import datetime
import pandas as pd
import threading

st.set_page_config(page_title="无人机心跳监测", layout="wide")

# 初始化会话状态（解决刷新问题）
if "heartbeat_data" not in st.session_state:
    st.session_state.heartbeat_data = []
if "last_receive_time" not in st.session_state:
    st.session_state.last_receive_time = time.time()
if "is_online" not in st.session_state:
    st.session_state.is_online = True

# 心跳发送线程
def send_heartbeat():
    seq = 1
    while True:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.heartbeat_data.append({
            "序号": seq, 
            "时间": current_time, 
            "状态": "正常"
        })
        st.session_state.last_receive_time = time.time()
        st.session_state.is_online = True
        seq += 1
        time.sleep(1)

# 掉线检测线程
def check_offline():
    while True:
        if time.time() - st.session_state.last_receive_time > 3:
            st.session_state.is_online = False
        time.sleep(0.5)

# 启动线程
if "thread_started" not in st.session_state:
    threading.Thread(target=send_heartbeat, daemon=True).start()
    threading.Thread(target=check_offline, daemon=True).start()
    st.session_state.thread_started = True

# 页面自动刷新（关键）
st.rerun_script = st.empty()

# 界面展示
st.title("无人机通信心跳监测可视化")
col1, col2 = st.columns(2)

with col1:
    st.subheader("连接状态")
    if st.session_state.is_online:
        st.success("✅ 无人机在线，心跳正常")
    else:
        st.error("❌ 无人机掉线！3秒未收到心跳包")

with col2:
    st.subheader("实时心跳数据")
    df = pd.DataFrame(st.session_state.heartbeat_data[-10:])
    st.dataframe(df, use_container_width=True)

# 折线图（实时更新）
st.subheader("心跳时序折线图")
if st.session_state.heartbeat_data:
    df_all = pd.DataFrame(st.session_state.heartbeat_data)
    df_all["时间"] = pd.to_datetime(df_all["时间"])
    st.line_chart(df_all, x="时间", y="序号", use_container_width=True)

# 强制刷新
time.sleep(1)
st.rerun()
