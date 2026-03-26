# 无人机通信心跳监测可视化
## 功能说明
1. 每秒生成带序号和时间的无人机心跳包
2. 3秒未收到心跳自动标记掉线
3. 实时展示心跳数据和时序折线图

## 运行方式
1. 安装依赖：`pip install -r requirements.txt`
2. 本地运行：`streamlit run app.py`
3. 云端部署：上传代码到GitHub，通过Streamlit Cloud关联部署
