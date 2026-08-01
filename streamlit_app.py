import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="群共享抽取器", page_icon="🎲")
st.title("🎲 群共享随机抽取器")
st.caption("所有人看到同一界面，结果实时共享")

# ===== 初始化 =====
if 'files_data' not in st.session_state:
    st.session_state.files_data = {}
if 'results' not in st.session_state:
    st.session_state.results = {"time": "", "files": []}

# ===== 侧边栏：上传文件 =====
with st.sidebar:
    st.header("📂 上传文件")
    
    uploaded = st.file_uploader("选择txt文件", accept_multiple_files=True, type=['txt'])
    
    if uploaded:
        for f in uploaded:
            if f.name not in st.session_state.files_data:
                st.session_state.files_data[f.name] = {
                    "content": f.read().decode('utf-8', errors='ignore'),
                    "time": datetime.now().strftime("%H:%M:%S")
                }
        st.success(f"✅ 上传了 {len(uploaded)} 个文件")
        st.rerun()
    
    # 文件列表
    if st.session_state.files_data:
        st.subheader(f"📚 已上传 ({len(st.session_state.files_data)}个)")
        for name in st.session_state.files_data:
            st.text(f"📄 {name}")
        
        if st.button("🗑 清空全部"):
            st.session_state.files_data = {}
            st.session_state.results = {"time": "", "files": []}
            st.rerun()

# ===== 主界面 =====
if not st.session_state.files_data:
    st.info("👈 请在左侧上传文件")
else:
    names = list(st.session_state.files_data.keys())
    
    # 勾选区域
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        if 'checked' not in st.session_state:
            st.session_state.checked = names.copy()
        st.session_state.checked = st.multiselect(
            "勾选参与抽取的文件",
            names,
            default=st.session_state.checked
        )
    with col2:
        st.write("")
        if st.button("☑ 全选", use_container_width=True):
            st.session_state.checked = names.copy()
            st.rerun()
    with col3:
        st.write("")
        if st.button("☐ 取消全选", use_container_width=True):
            st.session_state.checked = []
            st.rerun()
    
    # 抽取按钮
    checked = st.session_state.checked
    if checked:
        col1, col2 = st.columns([3, 1])
        with col1:
            count = st.number_input("抽取数量", 1, len(checked), min(3, len(checked)))
        with col2:
            st.write("")
            if st.button("🎲 开始抽取", type="primary", use_container_width=True):
                result = random.sample(checked, count)
                st.session_state.results = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "files": result
                }
                st.rerun()
    
    # 显示结果
    results = st.session_state.results
    if results["files"]:
        st.divider()
        st.subheader(f"📋 抽取结果（{results['time']}）")
        
        for i, name in enumerate(results["files"], 1):
            with st.expander(f"📄 {i}. {name}", expanded=(i <= 3)):
                content = st.session_state.files_data.get(name, {}).get("content", "")
                if len(content) > 500:
                    content = content[:500] + "\n\n... (仅显示前500字)"
                st.text_area("内容", content, height=200, disabled=True, key=f"r_{i}")
    
    # 刷新按钮
    st.divider()
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 刷新", use_container_width=True):
            st.rerun()
    with col2:
        st.caption("💡 多人同时打开，点击刷新可同步看到最新上传和抽取结果")