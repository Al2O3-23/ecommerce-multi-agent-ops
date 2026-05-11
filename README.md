# 抖店 AI 运营助手

基于 MiMo 大模型的电商运营自动化工具，提供三个核心功能模块。

## 功能模块

- **商品文案生成** — 输入商品信息，AI 自动生成抖店商品标题、卖点提炼、详情页文案、FAQ
- **智能客服** — 粘贴客户消息，AI 生成专业回复话术，支持退换货、催付、差评处理等场景
- **店铺经营复盘** — 手动输入销售数据，AI 生成复盘报告和改进建议

## 技术栈

Python | Streamlit | LangChain | MiMo v2 Pro | SQLite

## 快速开始

### 1. 克隆项目

```bash
git clone <仓库地址>
cd ecommerce-multi-agent-ops
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 API Key

复制 `.env.example` 为 `.env`，填入你的 MiMo API Key：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```
MIMO_API_KEY=你的API密钥
```

### 5. 启动

```bash
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501。

## 项目结构

```
├── app.py                  # 主页入口
├── config.py               # 配置（API Key、数据库、LLM 初始化）
├── database/
│   ├── __init__.py         # 数据库引擎和会话
│   └── models.py           # ORM 数据模型
├── pages/
│   ├── 1_content.py        # 商品文案生成
│   ├── 2_service.py        # 智能客服
│   └── 3_review.py         # 店铺经营复盘
├── requirements.txt
├── .env.example
└── .gitignore
```
