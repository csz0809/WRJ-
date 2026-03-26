import streamlit as st
import time
import datetime
import pandas as pd

st.set_page_config(page_title="无人机心跳", layout="wide")

# 初始化数据
if "data" not in st.session_state:
    st.session_state.data = []
    st.session_state.seq = 1

# 每秒生成一条心跳
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.session_state.data.append({
    "序号": st.session_state.seq,
    "时间": current_time,
    "状态": "正常"
})
st.session_state.seq += 1

# 界面
st.title("无人机通信心跳监测可视化")

col1, col2 = st.columns(2)
with col1:
    st.subheader("连接状态")
    st.success("✅ 无人机在线，心跳正常")

with col2:
    st.subheader("实时心跳数据")
    df = pd.DataFrame(st.session_state.data[-10:])
    st.dataframe(df, use_container_width=True)

# 折线图
st.subheader("心跳时序折线图")
df_all = pd.DataFrame(st.session_state.data)
df_all["时间"] = pd.to_datetime(df_all["时间"])
st.line_chart(df_all, x="时间", y="序号", use_container_width=True)

# 自动刷新
time.sleep(1)
st.rerun()
