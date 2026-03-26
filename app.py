import streamlit as st
import time
import datetime
import pandas as pd
import threading

st.set_page_config(page_title="无人机心跳监测", layout="wide")
heartbeat_data = []
last_receive_time = time.time()
is_online = True

def send_heartbeat():
    global last_receive_time, is_online
    seq = 1
    while True:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        heartbeat_data.append({"序号": seq, "时间": current_time, "状态": "正常"})
        last_receive_time = time.time()
        is_online = True
        seq += 1
        time.sleep(1)

def check_offline():
    global is_online
    while True:
        if time.time() - last_receive_time > 3:
            is_online = False
        time.sleep(0.5)

threading.Thread(target=send_heartbeat, daemon=True).start()
threading.Thread(target=check_offline, daemon=True).start()

st.title("无人机通信心跳监测可视化")
col1, col2 = st.columns(2)

with col1:
    st.subheader("连接状态")
    if is_online:
        st.success("✅ 无人机在线，心跳正常")
    else:
        st.error("❌ 无人机掉线！3秒未收到心跳包")

with col2:
    st.subheader("实时心跳数据")
    df = pd.DataFrame(heartbeat_data[-10:])
    st.dataframe(df, use_container_width=True)

st.subheader("心跳时序折线图")
if heartbeat_data:
    df_all = pd.DataFrame(heartbeat_data)
    df_all["时间"] = pd.to_datetime(df_all["时间"])
    st.line_chart(df_all, x="时间", y="序号", use_container_width=True)
