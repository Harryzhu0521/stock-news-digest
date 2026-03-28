"""Summarize articles using Google Gemini (free tier)."""

import time
import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL, SUMMARY_LANGUAGE


def _get_prompt(article: dict) -> str:
    lang_instruction = (
        "用中文回答。" if SUMMARY_LANGUAGE == "zh"
        else "Answer in English."
    )

    return f"""{lang_instruction}

你是一个专业的金融市场分析师，专注于股票、期权和科技行业。请对以下新闻文章进行分析：

**标题**: {article['title']}
**来源**: {article['source']}
**摘要**: {article['summary']}

请严格按照以下格式输出（必须包含【总结】和【分析】两个标记）：

【总结】
（3-5句话，完整概括新闻的核心内容，包括涉及的公司、数据、事件背景）

【分析】
（1-2句话，从量化交易/投资的角度，这条新闻可能对市场产生什么影响？对哪些板块/个股可能有影响？）

要求：语言简洁专业，如果涉及具体数字/数据务必保留。必须同时输出【总结】和【分析】两部分。"""


def summarize_articles(articles: list[dict]) -> list[dict]:
    """Add AI-generated summaries to each article."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)

    results = []
    for i, article in enumerate(articles):
        try:
            response = model.generate_content(_get_prompt(article))
            article["ai_summary"] = response.text
        except Exception as e:
            article["ai_summary"] = f"(总结生成失败: {e})"

        results.append(article)

        # Rate limiting: Gemini free tier allows 15 RPM
        if i < len(articles) - 1:
            time.sleep(4.5)

    return results
