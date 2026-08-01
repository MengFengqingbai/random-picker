import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="群共享抽取器", page_icon="🎲")
st.title("🎲 群共享随机抽取器")
st.caption("上传文件 → 勾选 → 抽取")

# 初始化
if 'files_data' not in st.session_state:
    st.session_state.files_data = {}
if 'results' not in st.session_state:
    st.session_state.results = {"time": "", "files": []}
if 'checked' not in st.session_state:
    st.session_state.checked = []

# 侧边栏
with st.sidebar:
    st.header("📂 上传文件")
    uploaded = st.file_uploader("选择txt文件", accept_multiple_files=True, type=['txt'])
    
    if uploaded:
        for f in uploaded:
            st.session_state.files_data[f.name] = {
                "content": f.read().decode('utf-8', errors='ignore'),
                "time": datetime.now().strftime("%H:%M:%S")
            }
        st.success(f"✅ 上传了 {len(uploaded)} 个文件")
        st.rerun()
    
    if st.session_state.files_data:
        st.subheader(f"📚 文件列表 ({len(st.session_state.files_data)}个)")
        for name in st.session_state.files_data:
            st.text(f"📄 {name}")
        
        if st.button("🗑 清空全部", use_container_width=True):
            st.session_state.files_data = {}
            st.session_state.results = {"time": "", "files": []}
            st.session_state.checked = []
            st.rerun()

# 主界面
if not st.session_state.files_data:
    st.info("👈 请先在左侧上传txt文件")
else:
    names = list(st.session_state.files_data.keys())
    
    st.subheader("📋 勾选参与抽取的文件")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("☑ 全选", use_container_width=True):
            st.session_state.checked = names.copy()
            st.rerun()
    with c2:
        if st.button("☐ 取消全选", use_container_width=True):
            st.session_state.checked = []
            st.rerun()
    
    st.session_state.checked = st.multiselect(
        "勾选文件（可多选）",
        names,
        default=st.session_state.checked
    )
    
    if st.session_state.checked:
        st.divider()
        st.subheader("🎯 抽取设置")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            count = st.number_input(
                "抽取数量", 
                1, 
                len(st.session_state.checked), 
                min(3, len(st.session_state.checked))
            )
        with c2:
            st.write("")
            st.write("")
            if st.button("🎲 开始抽取", type="primary", use_container_width=True):
                result = random.sample(st.session_state.checked, count)
                st.session_state.results = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "files": result
                }
                st.rerun()
    
    # 显示结果
    if st.session_state.results["files"]:
        st.divider()
        st.subheader(f"📋 抽取结果（{st.session_state.results['time']}）")
        
        for i, name in enumerate(st.session_state.results["files"], 1):
            with st.expander(f"📄 {i}. {name}", expanded=True):
                content = st.session_state.files_data.get(name, {}).get("content", "")
                if len(content) > 500:
                    content = content[:500] + "\n\n... (仅显示前500字)"
                st.text_area("内容预览", content, height=200, disabled=True, key=f"r_{i}")
    else:
        st.info("还没有抽取结果，请先勾选文件并点击抽取")
