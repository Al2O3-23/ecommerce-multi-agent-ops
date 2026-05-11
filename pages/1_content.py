import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

st.set_page_config(page_title="商品文案生成", page_icon="✍️", layout="wide")
from config import get_llm, extract_text

st.title("商品详情页文案生成")
st.caption("输入商品信息，AI 自动生成抖店上架文案")

with st.form("content_form"):
    c1, c2 = st.columns(2)
    with c1:
        product_name = st.text_input("商品名称 *", placeholder="蓝牙耳机无线降噪入耳式")
        category = st.text_input("商品类目", placeholder="数码配件")
        target_audience = st.text_input("目标人群", placeholder="18-35岁年轻上班族")
    with c2:
        selling_points = st.text_area("核心卖点（每行一个）", placeholder="主动降噪35dB\n蓝牙5.3低延迟\n续航30小时\nIPX5防水", height=100)
        price_range = st.text_input("价格区间", placeholder="29.9-59.9元")

    style = st.selectbox("文案风格", ["种草风", "带货风", "专业风", "简约风"], index=0)
    submitted = st.form_submit_button("生成文案", type="primary", use_container_width=True)

if submitted and product_name:
    with st.spinner("AI 正在创作中..."):
        try:
            llm = get_llm()
            prompt = f"""你是资深抖店文案策划。根据商品信息生成文案，严格按以下格式输出（不要添加额外说明）：

【标题】
（30字以内抖店商品标题，含核心关键词）

【卖点1】（一句话）
【卖点2】（一句话）
【卖点3】（一句话）
【卖点4】（一句话）
【卖点5】（一句话）

【详情】
（300-500字详情页文案，分3-4个段落）

【FAQ:问题1】
答案

【FAQ:问题2】
答案

【FAQ:问题3】
答案

---
商品：{product_name}
类目：{category}
人群：{target_audience}
卖点：{selling_points}
价格：{price_range}
风格：{style}"""

            response = llm.invoke(prompt)
            text = extract_text(response)

            # Parse sections
            sections = {"title": "", "selling": [], "detail": "", "faq": []}
            current = None
            for line in text.split("\n"):
                line = line.strip()
                if line.startswith("【标题】"):
                    current = "title"
                    continue
                elif line.startswith("【卖点"):
                    current = "selling_item"
                    content = line.split("】", 1)[-1].strip()
                    if content:
                        sections["selling"].append(content)
                    continue
                elif line.startswith("【详情】"):
                    current = "detail"
                    continue
                elif line.startswith("【FAQ:"):
                    current = "faq_q"
                    q = line.replace("【FAQ:", "").replace("】", "").strip()
                    sections["faq"].append({"q": q, "a": ""})
                    continue
                elif line == "---":
                    current = None
                    continue

                if current == "title" and line:
                    sections["title"] = line
                    current = None
                elif current == "selling_item" and line:
                    sections["selling"].append(line)
                    current = "selling_item"
                elif current == "detail" and line:
                    sections["detail"] += line + "\n"
                elif current == "faq_q" and line:
                    if sections["faq"]:
                        sections["faq"][-1]["a"] = line
                    current = "faq_a"
                elif current == "faq_a" and line:
                    if sections["faq"]:
                        sections["faq"][-1]["a"] += line

            # --- Display ---
            st.markdown("---")

            # Title
            if sections["title"]:
                st.subheader("推荐标题")
                st.code(sections["title"], language=None)
                st.caption(f"共 {len(sections['title'])} 字")

            # Selling points
            if sections["selling"]:
                st.subheader("核心卖点")
                for i, sp in enumerate(sections["selling"]):
                    st.success(f"**{i+1}.** {sp}")

            # Detail
            if sections["detail"]:
                st.subheader("详情页文案")
                with st.container(border=True):
                    st.markdown(sections["detail"])

            # FAQ
            if sections["faq"]:
                st.subheader("常见问题 FAQ")
                for faq in sections["faq"]:
                    with st.expander(f"Q: {faq['q']}"):
                        st.write(faq["a"])

            # Fallback: show raw text
            if not sections["title"] and not sections["selling"]:
                st.subheader("生成结果")
                st.markdown(text)

            st.divider()
            st.download_button("下载文案", data=text, file_name=f"{product_name}_文案.txt", mime="text/plain")

        except Exception as e:
            st.error(f"生成失败: {e}")
elif submitted:
    st.warning("请填写商品名称")
