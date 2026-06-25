import os
from datetime import datetime
import google.generativeai as genai

# 1. 自动获取今天是周几
WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
current_day = WEEKDAYS[datetime.today().weekday()]

# 2. 根据你的 README 排班表，自动匹配今天的学习主题
THEMES = {
    "周一": "采购英语 (Procurement & Sourcing) - 结合外贸、招标、供应商沟通",
    "周二": "项目管理英语 (Project Management) - 结合项目进度、ESCO节能项目、交付",
    "周三": "物业管理英语 (Property Management) - 结合租户沟通、设施维护、投诉处理",
    "周四": "工程施工英语 (Engineering & Construction) - 结合施工现场、技术标准、安全规范",
    "周五": "谈判英语 (Negotiation & Contract) - 结合价格谈判、合同条款、笑着怼人/礼貌发飙",
    "周六": "Native Speaker表达 (Hong Kong & UK Office Idioms) - 港英办公室地道行话",
    "周日": "Native Speaker表达 (Hong Kong & UK Office Idioms) - 经典职场行话复盘"
}

today_theme = THEMES.get(current_day, "商务英语")

# 3. 配置 Gemini API
gemini_key = os.getenv("AI_API_KEY")
genai.configure(api_key=gemini_key)

# 4. 组装 Prompt
user_prompt = f"""
今天是：{current_day}
今日核心训练主题是：{today_theme}

请严格按照以下格式为我生成今天的学习内容（不要包含任何多余的废话和 Markdown 之外的杂质）：

Today's Business English Coach ({current_day}·{today_theme})
---

### 📩 1. 今日1句商务英语（正式邮件版）
* **Expression:** [写出地道的邮件长句或核心短语]
* **Meaning:** [中文解释]
* **Example:** [结合节能/物业/采购场景的邮件例句]

### 👥 2. 今日1句会议表达（口语版）
* **Expression:** [写出会议、开场、讨论或反驳时的口语表达]
* **Meaning:** [中文解释]
* **Example:** [口语场景例句]

### 🇬🇧 3. 今日1个Native表达（香港/英国办公室常用）
* **Expression:** [例如职场黑话、缩写、或俚语，如 Move the needle, Touch base, Keep me in the loop]
* **Meaning:** [中文解释]
* **Example:** [例句]

---
### 🎯 Challenge（今日挑战）
请将以下这句话翻译成地道的商务英语（回复本条消息即可练习）：
[请结合今天的场景，出一道中文翻译题。例如：“这个空调改造方案预计能帮租户节省15%的电费。”]
"""

# 5. 【核心修复点】更换为带完整发布商前缀的绝对路径模型名称
try:
    model = genai.GenerativeModel(
        model_name="publishers/google/models/gemini-1.5-flash",
    )
    # 免费层将系统提示词合并传入最安全
    response = model.generate_content(
        f"System: 你是一位资深跨国企业商务英语培训师，拥有香港和英国办公室多年工作经验。熟悉 ESCO（能源节能项目）、物业管理、采购招标和高管沟通场景。请根据用户提供的主题出题。\n\nUser: {user_prompt}"
    )
    print(response.text)
except Exception as e:
    print(f"呼叫 Gemini 失败了，错误原因: {e}")
