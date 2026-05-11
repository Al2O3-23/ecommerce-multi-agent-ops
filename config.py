import os
import functools
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

# ========== API ==========
MIMO_API_KEY = os.getenv("MIMO_API_KEY", "")
MIMO_BASE_URL = "https://token-plan-cn.xiaomimimo.com/anthropic"
MIMO_MODEL = "mimo-v2-pro"

# ========== Database ==========
DATABASE_URL = "sqlite:///ecommerce_ops.db"

# ========== LLM ==========
@functools.lru_cache(maxsize=1)
def get_llm():
    return ChatAnthropic(
        model=MIMO_MODEL,
        temperature=0.7,
        api_key=MIMO_API_KEY,
        base_url=MIMO_BASE_URL,
    )


def extract_text(response) -> str:
    """Extract plain text from MiMo API response"""
    content = response.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                return item.get("text", "")
    return str(content)
