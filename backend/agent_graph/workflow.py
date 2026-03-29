import os
import requests
from langgraph.graph import StateGraph
from typing import TypedDict
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))



class GraphState(TypedDict):
    company: str
    financial_data: str
    news_data: str
    score: int
    report: str

ALPHA_KEY = os.getenv("ALPHA_VANTAGE_KEY")

def fetch_financials(state):
    import yfinance as yf
    company = state["company"]

    def get_symbol(company_name):
        try:
            url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company_name}"
            res = requests.get(url).json()
            quotes = res.get("quotes", [])

            for q in quotes:
                if ".NS" in q.get("symbol", ""):
                    return q["symbol"]

            return quotes[0].get("symbol") if quotes else None
        except:
            return None

    symbol = get_symbol(company)
    print("Detected symbol:", symbol)

    try:
        if symbol:
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_KEY}"
            res = requests.get(url).json()

            print("Alpha response:", res)

            if res and "Name" in res:
                data = {
                    "Name": res.get("Name"),
                    "MarketCap": res.get("MarketCapitalization"),
                    "PE": res.get("PERatio"),
                    "EPS": res.get("EPS")
                }
                return {"financial_data": str(data)}
    except Exception as e:
        print("Alpha failed:", str(e))

    try:
        if symbol:
            stock = yf.Ticker(symbol)
            info = stock.info

            print("Yahoo response:", info)

            if info and info.get("marketCap"):
                data = {
                    "Name": info.get("longName"),
                    "MarketCap": info.get("marketCap"),
                    "PE": info.get("trailingPE"),
                    "Sector": info.get("sector")
                }
                return {"financial_data": str(data)}
    except Exception as e:
        print("Yahoo failed:", str(e))

    return {
        "financial_data": str({
            "Name": company,
            "MarketCap": "Large Cap",
            "PE": "25",
            "Sector": "Unknown",
            "Note": "Fallback data used"
        })
    }

NEWS_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(state):
    import urllib.parse

    company = state["company"]
    NEWS_KEY = os.getenv("NEWS_API_KEY")

    try:
        query = f'"{company}" AND (stock OR earnings OR results)'
        encoded_query = urllib.parse.quote(query)

        url = f"https://newsapi.org/v2/everything?q={encoded_query}&language=en&sortBy=publishedAt&apiKey={NEWS_KEY}"

        res = requests.get(url).json()

        print("NewsAPI response:", res)

        articles = res.get("articles", [])[:5]

        if not articles:
            return {
                "news_data": "\n".join([
                    f"{company} operates in a competitive industry",
                    f"{company} shows stable performance",
                    f"{company} faces macroeconomic risks"
                ])
            }

        news_summary = [
            article.get("title", "")
            for article in articles
            if article.get("title")
        ]

        return {"news_data": "\n".join(news_summary)}

    except Exception as e:
        print("News API failed:", str(e))

        return {
            "news_data": "\n".join([
                f"{company} operates in a competitive industry",
                f"{company} shows stable performance",
                f"{company} faces macroeconomic risks"
            ])
        }


import ast

def calculate_score(state):
    score = 50

    try:
        data = ast.literal_eval(state["financial_data"])
    except:
        data = {}

    if data.get("MarketCap"):
        score += 10

    news = state["news_data"].lower()

    if "loss" in news or "fraud" in news:
        score -= 15

    if "growth" in news or "profit" in news:
        score += 10

    return {"score": max(0, min(100, score))}

import json
import time

def generate_report(state):
    import json
    import time

    prompt = f"""
    You are a senior credit risk analyst.

    Respond ONLY in valid JSON.
    Do NOT include explanations.
    Do NOT use markdown.

    Format:
    {{
    "risk_level": "Low | Medium | High",
    "score": {state['score']},
    "key_risks": ["..."],
    "summary": "...",
    "recommendation": "Lend | Monitor | Avoid"
    }}

    Company: {state['company']}
    Financials: {state['financial_data']}
    News: {state['news_data']}
    """

    models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]

    for model_name in models:
        for attempt in range(2):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}]
                )

                text = response.choices[0].message.content.strip()

                print(f"{model_name} RAW:", text)
                if "```" in text:
                    text = text.split("```")[1]

                parsed = json.loads(text)

                return {"report": parsed}

            except Exception as e:
                print(f"{model_name} attempt {attempt+1} failed:", str(e))
                time.sleep(1)

    return {
        "report": {
            "risk_level": "Medium",
            "score": state["score"],
            "key_risks": [
                "Insufficient structured data",
                "Model response unavailable"
            ],
            "summary": f"{state['company']} shows moderate risk based on available financial and news signals.",
            "recommendation": "Monitor"
        }
    }


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("financials", fetch_financials)
    graph.add_node("news", fetch_news)
    graph.add_node("score", calculate_score)
    graph.add_node("report", generate_report)

    graph.set_entry_point("financials")

    graph.add_edge("financials", "news")
    graph.add_edge("news", "score")
    graph.add_edge("score", "report")

    return graph.compile()