import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class DataFetcher:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol.upper()
        self.ticker = yf.Ticker(self.ticker_symbol)

    def get_info(self):
        """Fetches general company information and key metrics."""
        try:
            info = self.ticker.info
            return {
                "name": info.get("longName", self.ticker_symbol),
                "price": info.get("currentPrice"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "eps": info.get("trailingEps"),
                "debt_to_equity": info.get("debtToEquity"),
                "profit_margin": info.get("profitMargins"),
                "revenue_growth": info.get("revenueGrowth"),
                "free_cash_flow": info.get("freeCashflow"),
                "dividend_yield": info.get("dividendYield"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "summary": info.get("longBusinessSummary")
            }
        except Exception as e:
            print(f"Error fetching info for {self.ticker_symbol}: {e}")
            return None

    def get_financials(self):
        """Fetches historical financial statements."""
        try:
            income_stmt = self.ticker.income_stmt
            balance_sheet = self.ticker.balance_sheet
            cash_flow = self.ticker.cashflow
            
            return {
                "income_stmt": income_stmt,
                "balance_sheet": balance_sheet,
                "cash_flow": cash_flow
            }
        except Exception as e:
            print(f"Error fetching financials for {self.ticker_symbol}: {e}")
            return None

    def get_history(self, period="1y"):
        """Fetches historical price data."""
        try:
            return self.ticker.history(period=period)
        except Exception as e:
            print(f"Error fetching history for {self.ticker_symbol}: {e}")
            return None

    def get_revenue_trend(self):
        """Extracts revenue and net income for the last 4 years."""
        try:
            income_stmt = self.ticker.income_stmt
            if income_stmt is not None and not income_stmt.empty:
                # Transpose to have dates as index and metrics as columns
                df = income_stmt.transpose()
                # Use 'Total Revenue' and 'Net Income' (keys may vary slightly in yfinance)
                available_cols = df.columns.tolist()
                rev_col = next((c for c in available_cols if 'Revenue' in c), None)
                net_inc_col = next((c for c in available_cols if 'Net Income' in c), None)
                
                if rev_col and net_inc_col:
                    return df[[rev_col, net_inc_col]].sort_index()
            return None
        except Exception as e:
            print(f"Error getting revenue trend: {e}")
            return None
