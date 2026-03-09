class Analyzer:
    def __init__(self, stock_info):
        self.stock_info = stock_info

    def calculate_health_score(self):
        """Calculates a health score from 0-100 based on key financial metrics."""
        score = 0
        total_possible = 0

        # PE Ratio Scoring (Lower is often better for valuation, but context dependent)
        pe = self.stock_info.get("pe_ratio")
        if pe is not None:
            total_possible += 25
            if pe < 15: score += 25
            elif pe < 25: score += 15
            elif pe < 40: score += 5

        # Revenue Growth Scoring
        growth = self.stock_info.get("revenue_growth")
        if growth is not None:
            total_possible += 25
            if growth > 0.2: score += 25
            elif growth > 0.1: score += 15
            elif growth > 0: score += 5

        # Profit Margin Scoring
        margin = self.stock_info.get("profit_margin")
        if margin is not None:
            total_possible += 25
            if margin > 0.2: score += 25
            elif margin > 0.1: score += 15
            elif margin > 0.05: score += 5

        # Debt to Equity Scoring (Lower is better)
        debt = self.stock_info.get("debt_to_equity")
        if debt is not None:
            total_possible += 25
            if debt < 50: score += 25
            elif debt < 100: score += 15
            elif debt < 150: score += 5

        if total_possible == 0:
            return 0
        
        return (score / total_possible) * 100

    def get_risk_alerts(self):
        """Identifies potential financial risks."""
        alerts = []
        
        pe = self.stock_info.get("pe_ratio")
        if pe and pe > 50:
            alerts.append("High Valuation: The P/E ratio is quite high, which may indicate overvaluation.")
            
        debt = self.stock_info.get("debt_to_equity")
        if debt and debt > 150:
            alerts.append("High Debt: The debt-to-equity ratio is high, suggesting potential financial risk.")
            
        margin = self.stock_info.get("profit_margin")
        if margin and margin < 0.02:
            alerts.append("Low Margins: Profit margins are thin, leaving little room for error.")
            
        growth = self.stock_info.get("revenue_growth")
        if growth and growth < 0:
            alerts.append("Negative Growth: The company's revenue is declining.")
            
        return alerts

    def get_valuation_insight(self):
        """Provides a simple interpretation of the company's valuation."""
        pe = self.stock_info.get("pe_ratio")
        forward_pe = self.stock_info.get("forward_pe")
        
        if pe is None:
            return "Valuation data is currently unavailable."
            
        if pe < 10:
            return "The company appears to be undervalued based on its trailing earnings."
        elif 10 <= pe < 25:
            return "The company's valuation seems reasonable compared to historical market averages."
        else:
            return "The company is trading at a premium, which might be justified by high growth expectations."
