import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIExplainer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def generate_explanation(self, stock_info, health_score, risk_alerts):
        """Generates an AI-powered financial explanation for a company."""
        if not self.client:
            return "OpenAI API key is missing. Please provide one in the .env file."

        prompt = f"""
        Explain the financial health of {stock_info.get('name')} in simple terms based on the following data:
        - Price: {stock_info.get('price')}
        - Market Cap: {stock_info.get('market_cap')}
        - PE Ratio: {stock_info.get('pe_ratio')}
        - EPS: {stock_info.get('eps')}
        - Revenue Growth: {stock_info.get('revenue_growth')}
        - Profit Margin: {stock_info.get('profit_margin')}
        - Debt to Equity: {stock_info.get('debt_to_equity')}
        - Free Cash Flow: {stock_info.get('free_cash_flow')}
        - Calculated Financial Health Score (0-100): {health_score:.2f}
        - Current Risk Alerts: {', '.join(risk_alerts) if risk_alerts else 'None'}

        Please provide your analysis in the following format:
        ### Summary
        ### Key Strengths
        ### Key Risks
        ### Investment Insight
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo", # Use GPT-3.5 or GPT-4 for analysis
                messages=[
                    {"role": "system", "content": "You are a helpful financial analyst providing simple insights for retail investors."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating explanation: {e}"
