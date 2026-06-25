import os
import sys
import google.generativeai as genai

# 从系统环境变量中获取 GitHub Actions 传进来的 API 密钥
api_key = os.environ.get("AI_API_KEY")

if not api_key:
    print("错误: 未找到 AI_API_KEY 环境变量，请检查 GitHub Secrets 配置。")
    sys.exit(1)

# 配置 Gemini
genai.configure(api_key=api_key)

# 使用稳定版模型
model = genai.GenerativeModel("gemini-2.5-flash")

# 设定你专属的每日商务英语教练 Prompt
prompt = """
你是一位专业的商务英语教练。请为我的小伙伴们生成今天的“每日商务英语核心课”。
内容要求精简、实用、地道，包含：
1. 今日核心商务短语/句型（附带职场真实应用场景说明）。
2. 2个极度地道的职场例句（包含中文翻译）。
3. 一个微型互动练习或跟读小建议，字数控制在300字以内，排版要清晰、空行明确。
"""

try:
    response = model.generate_content(prompt)
    # 打印输出，供工作流捕获并发送邮件
    print(response.text)
except Exception as e:
    print(f"呼叫 Gemini 失败了，错误原因: {e}")
    sys.exit(1)
