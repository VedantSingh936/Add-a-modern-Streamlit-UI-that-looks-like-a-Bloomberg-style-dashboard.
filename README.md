# Add-a-modern-Streamlit-UI-that-looks-like-a-Bloomberg-style-dashboard.
**AI Stock Fundamental Analyzer** is a tool that fetches real-time financial data from Yahoo Finance and analyzes key metrics like PE ratio, revenue, EPS, and debt levels. It uses AI from OpenAI to explain a company’s financial health and valuation in simple terms, helping retail investors better understand stock fundamentals.
# AI Stock Fundamental Analyzer 🚀

An intelligent tool for retail investors to analyze stock fundamentals, visualize financial trends, and get AI-powered explanations of a company's financial health.

## Features ✨

- **Real-Time Data Fetching**: Retrieves financial data (P/E Ratio, EPS, Revenue, Debt, etc.) using `yfinance`.
- **Financial Dashboard**: Interactive visualizations of revenue trends, net income, and stock price history.
- **Financial Health Score**: A proprietary 0–100 score based on key valuation, growth, profitability, and risk metrics.
- **AI-Powered Insights**: Uses OpenAI's GPT models to explain complex financial data in simple terms.
- **Risk Alerts**: Automatically flags high valuation, excessive debt, or low profit margins.

## Tech Stack 🛠️

- **Python**: Core programming language.
- **Streamlit**: Web application framework for the UI.
- **yfinance**: For fetching real-time financial data.
- **Pandas**: Data manipulation and analysis.
- **Plotly**: Interactive charts and visualizations.
- **OpenAI API**: For generating AI-driven financial insights.

## Project Structure 📁

```text
AI-Stock-Fundamental-Analyzer
│
├── app.py           # Main Streamlit application
├── data_fetcher.py  # Data retrieval logic
├── analyzer.py      # Financial metric calculations and scoring
├── ai_explainer.py  # OpenAI integration for AI insights
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
```

## Installation and Setup 🚀

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/AI-Stock-Fundamental-Analyzer.git
    cd AI-Stock-Fundamental-Analyzer
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables**:
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```text
    OPENAI_API_KEY=your_openai_api_key_here
    ```

4.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## Usage 📈

1. Enter a stock ticker symbol (e.g., `AAPL`, `TSLA`, `NVDA`) in the sidebar.
2. View the financial health score and key metrics.
3. Explore the revenue and net income trends.
4. Click **"Generate AI Insights"** to get a detailed breakdown of the company's financial health from an AI financial analyst.

## Screenshots 📸

*(Add screenshots here after running the app)*

---

**Disclaimer**: This tool is for educational purposes only and does not constitute financial advice. Always do your own research before investing.
