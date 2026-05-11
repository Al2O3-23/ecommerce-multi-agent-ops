import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from database import init_db

st.set_page_config(
    page_title="抖店AI运营助手",
    page_icon="🛒",
    layout="wide",
)

init_db()

st.title("抖店AI运营助手")
st.caption("基于 MiMo 大模型的电商运营自动化工具")

st.markdown("---")

modules = [
    {
        "name": "商品文案生成",
        "icon": "✍️",
        "desc": "输入商品信息，AI 自动生成抖店商品标题、卖点提炼、详情页文案、常见问题FAQ",
        "page": "pages/1_content.py",
    },
    {
        "name": "智能客服",
        "icon": "💬",
        "desc": "粘贴客户消息，AI 生成专业客服回复话术，支持退换货、催付、差评处理等场景",
        "page": "pages/2_service.py",
    },
    {
        "name": "店铺经营复盘",
        "icon": "📈",
        "desc": "手动输入销售额、订单量、广告花费等数据，AI 生成专业复盘报告和下阶段建议",
        "page": "pages/3_review.py",
    },
]

cols = st.columns(3)
for i, mod in enumerate(modules):
    with cols[i]:
        with st.container(border=True):
            st.markdown(f"### {mod['icon']} {mod['name']}")
            st.write(mod["desc"])
            if st.button(f"进入 {mod['name']}", key=f"btn_{i}", use_container_width=True, type="primary"):
                st.switch_page(mod["page"])

st.markdown("---")
st.caption("技术栈: Python | LangChain | MiMo v2 Pro | Streamlit | SQLite")
