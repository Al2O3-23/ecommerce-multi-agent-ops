import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from datetime import date

st.set_page_config(page_title="店铺经营复盘", page_icon="📈", layout="wide")
from config import get_llm, extract_text
from database import init_db, get_session
from database.models import BusinessReport

init_db()

st.title("店铺经营复盘")
st.caption("手动输入数据，AI 生成专业复盘报告")

with st.form("review_form"):
    c1, c2 = st.columns(2)
    with c1:
        start_date = st.date_input("开始日期", value=date.today().replace(day=1))
    with c2:
        end_date = st.date_input("结束日期", value=date.today())

    st.subheader("销售数据")
    c1, c2, c3 = st.columns(3)
    with c1:
        total_sales = st.number_input("总销售额(元)", min_value=0.0, step=100.0)
        order_count = st.number_input("订单数", min_value=0, step=1)
    with c2:
        refund_amount = st.number_input("退款金额(元)", min_value=0.0, step=10.0)
        refund_count = st.number_input("退款订单数", min_value=0, step=1)
    with c3:
        avg_price = st.number_input("客单价(元)", min_value=0.0, step=1.0)
        new_customers = st.number_input("新客数", min_value=0, step=1)

    st.subheader("流量 & 广告")
    c1, c2, c3 = st.columns(3)
    with c1:
        uv = st.number_input("访客数(UV)", min_value=0, step=100)
    with c2:
        ad_spend = st.number_input("广告花费(元)", min_value=0.0, step=100.0)
    with c3:
        conversion_rate = st.number_input("转化率(%)", min_value=0.0, max_value=100.0, step=0.1)

    notes = st.text_area("补充说明（选填）", placeholder="爆款商品、竞品动态、活动情况等", height=60)
    submitted = st.form_submit_button("生成复盘报告", type="primary", use_container_width=True)

if submitted and total_sales > 0:
    with st.spinner("AI 正在分析..."):
        try:
            llm = get_llm()
            net_sales = total_sales - refund_amount
            refund_rate = refund_count / order_count * 100 if order_count > 0 else 0
            ad_roi = (order_count * avg_price / ad_spend) if ad_spend > 0 else 0

            prompt = f"""你是资深抖店运营总监，根据数据生成复盘报告。严格按以下格式输出：

【整体评分】
（A/B/C/D，一句话评价）

【核心指标】
（用3-5个短句概括关键数据表现，每行一个指标+评价）

【亮点】
（1-2个做得好的方面）

【问题】
（2-3个需要改进的问题，具体到数据）

【下一步行动】
（3-5条可执行的改进建议，每条一句话，要具体）

---
数据：
周期：{start_date}~{end_date}
销售额：¥{total_sales:,.2f}，净额：¥{net_sales:,.2f}
订单：{order_count}单，退款：{refund_count}单({refund_rate:.1f}%)，¥{refund_amount:,.2f}
客单价：¥{avg_price:.2f}，新客：{new_customers}人
UV：{uv}，转化率：{conversion_rate:.1f}%
广告：¥{ad_spend:,.2f}，ROI：{ad_roi:.2f}
备注：{notes or "无"}"""

            response = llm.invoke(prompt)
            text = extract_text(response)

            # Parse response
            sections = {"score": "", "metrics": "", "highlights": "", "problems": "", "actions": ""}
            current = None
            for line in text.split("\n"):
                line = line.strip()
                if line.startswith("【整体评分】"):
                    current = "score"
                    continue
                elif line.startswith("【核心指标】"):
                    current = "metrics"
                    continue
                elif line.startswith("【亮点】"):
                    current = "highlights"
                    continue
                elif line.startswith("【问题】"):
                    current = "problems"
                    continue
                elif line.startswith("【下一步行动】"):
                    current = "actions"
                    continue
                elif line == "---":
                    current = None
                    continue
                if current and line:
                    sections[current] += line + "\n"

            # --- Display ---
            st.markdown("---")

            # Overall grade
            if sections["score"]:
                score_text = sections["score"].strip()
                # Extract grade letter
                grade = "B"
                for g in ["A", "B", "C", "D"]:
                    if g in score_text:
                        grade = g
                        break
                color = {"A": "green", "B": "blue", "C": "orange", "D": "red"}.get(grade, "grey")
                st.markdown(f"### 经营评级")
                st.badge(f"{grade} 级", color=color)
                st.caption(score_text)

            # Key metric cards
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("净销售额", f"¥{net_sales:,.0f}")
            with col2:
                st.metric("退款率", f"{refund_rate:.1f}%")
            with col3:
                st.metric("转化率", f"{conversion_rate:.1f}%")
            with col4:
                st.metric("广告ROI", f"{ad_roi:.2f}")

            # Metric analysis
            if sections["metrics"]:
                st.subheader("指标分析")
                for line in sections["metrics"].strip().split("\n"):
                    if line:
                        if "↑" in line or "增长" in line or "好" in line or "高" in line:
                            st.success(line)
                        elif "↓" in line or "下降" in line or "低" in line or "差" in line:
                            st.error(line)
                        else:
                            st.info(line)

            # Highlights + Problems
            c1, c2 = st.columns(2)
            with c1:
                if sections["highlights"]:
                    st.subheader("亮点")
                    for line in sections["highlights"].strip().split("\n"):
                        if line:
                            st.success(line)
            with c2:
                if sections["problems"]:
                    st.subheader("待改进")
                    for line in sections["problems"].strip().split("\n"):
                        if line:
                            st.warning(line)

            # Action plan
            if sections["actions"]:
                st.subheader("下一步行动计划")
                for i, line in enumerate(sections["actions"].strip().split("\n")):
                    if line:
                        st.checkbox(line, key=f"action_{i}")

            # Fallback: show raw text
            if not sections["score"] and not sections["metrics"]:
                st.markdown(text)

            # Save to database
            record = BusinessReport(
                start_date=str(start_date), end_date=str(end_date), report_content=text,
            )
            session = get_session()
            try:
                session.add(record)
                session.commit()
            finally:
                session.close()

            st.divider()
            st.download_button("下载报告", data=text, file_name=f"复盘_{start_date}_{end_date}.md", mime="text/markdown")

        except Exception as e:
            st.error(f"生成失败: {e}")
elif submitted:
    st.warning("请至少填写销售额")
