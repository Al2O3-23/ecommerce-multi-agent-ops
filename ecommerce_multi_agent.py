import os
import time
import random
from typing import List, Dict, Any
from dotenv import load_dotenv

# LangChain 核心库
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# ========== 配置与初始化 ==========
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 初始化大模型
llm = ChatOpenAI(model="gpt-4o", temperature=0.7, api_key=OPENAI_API_KEY)

# ========== 定义电商模拟工具 ==========
@tool
def get_market_data(category: str) -> Dict:
    """获取指定类目的市场选品数据（模拟接口）"""
    print(f"🛠️  抓取类目: {category} 市场数据...")
    time.sleep(1)
    mock_data = {
        "category": category,
        "hot_products": ["复古牛仔外套", "无线蓝牙耳机", "便携咖啡机"],
        "trend_keywords": ["美拉德风", "高续航", "Office适用"],
        "competition_score": random.randint(40, 80),
        "avg_profit_margin": 0.35
    }
    return mock_data

@tool
def generate_content(product_name: str, style: str = "带货风") -> str:
    """生成商品详情页文案与短视频脚本"""
    print(f"🛠️  生成商品: {product_name} 带货文案...")
    time.sleep(1)
    return f"【{product_name}】爆款文案：\n家人们谁懂啊！这款{product_name}性价比拉满，刚需必入，限时福利！"

@tool
def optimize_ads_budget(budget: float, ctr: float) -> Dict:
    """电商投流预算智能分配"""
    print(f"🛠️  进行投流预算优化分配...")
    time.sleep(1)
    return {
        "douyin": budget * 0.6,
        "xiaohongshu": budget * 0.3,
        "taobao_ztc": budget * 0.1,
        "predicted_roi": 2.8
    }

@tool
def handle_after_sales(order_id: str, issue: str) -> str:
    """智能处理售后纠纷"""
    print(f"🛠️  处理订单 {order_id} 售后问题...")
    time.sleep(1)
    return "已完成售后安抚，支持无理由退换，赠送优惠券提升复购。"

@tool
def generate_business_report(start_date: str, end_date: str) -> str:
    """生成店铺经营复盘报告"""
    print(f"🛠️  生成经营复盘报告...")
    time.sleep(1.5)
    return "📊 店铺复盘报告\n销售额稳定增长，爆款品类投流ROI表现优异，建议追加热门品类预算。"

all_tools = [
    get_market_data,
    generate_content,
    optimize_ads_budget,
    handle_after_sales,
    generate_business_report
]

# ========== 多Agent协作核心架构 ==========
class EcommerceOpsCenter:
    def __init__(self):
        self.llm = llm
        self.tools = all_tools
        
    def _create_agent(self, system_prompt: str) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=False, handle_parsing_errors=True)

    def run_full_workflow(self, initial_category: str):
        print("🚀 中小电商全链路多Agent自动化运营系统")

        # 1.选品Agent
        agent1 = self._create_agent("你是专业电商选品分析师，分析类目并推荐爆款单品。")
        res1 = agent1.invoke({"input": f"分析{initial_category}类目，推荐一款爆款"})
        print("✅ 选品结果：", res1['output'])

        # 2.文案Agent
        agent2 = self._create_agent("你是电商文案策划，生成爆款带货文案。")
        res2 = agent2.invoke({"input": "为复古牛仔外套生成抖音带货文案"})
        print("✅ 文案结果：", res2['output'])

        # 3.投流Agent
        agent3 = self._create_agent("你是电商投流优化师，合理分配推广预算。")
        res3 = agent3.invoke({"input": "日预算5000元，CTR3.5%，做投流分配方案"})
        print("✅ 投流方案：", res3['output'])

        # 4.售后Agent
        agent4 = self._create_agent("你是专业电商售后客服，温和处理用户纠纷。")
        res4 = agent4.invoke({"input": "订单8888，尺码不合适要退货"})
        print("✅ 售后处理：", res4['output'])

        # 5.复盘Agent
        agent5 = self._create_agent("你是电商运营总监，输出专业经营复盘建议。")
        res5 = agent5.invoke({"input": "生成本月上旬店铺经营复盘"})
        print("✅ 复盘报告：", res5['output'])

        print("🎉 多Agent全链路流程演示完毕")

if __name__ == "__main__":
    ops_center = EcommerceOpsCenter()
    ops_center.run_full_workflow(initial_category="女装")