import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_fetcher import DataFetcher
from analyzer import Analyzer
from ai_explainer import AIExplainer

# Page Configuration
st.set_page_config(
    page_title="Bloomberg AI Stock Analyzer",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- BLOOMBERG STYLE CSS ---
st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp {
        background-color: #0d0d0d;
        color: #ffffff;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        border-right: 1px solid #333;
    }
    
    /* Bloomberg Amber Headers */
    h1, h2, h3 {
        color: #ffb900 !important;
        font-family: 'Courier New', Courier, monospace;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Metric Cards Styling */
    div[data-testid="stMetricValue"] {
        color: #00ff00 !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #cccccc !important;
        text-transform: uppercase;
        font-size: 0.8rem !important;
    }

    /* Custom Container for Bloomberg Widgets */
    .bloomberg-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 2px;
        border: 1px solid #333;
        margin-bottom: 15px;
    }
    
    /* Financial Table Styling */
    .stTable {
        background-color: #1a1a1a;
        border: 1px solid #333;
    }
    
    /* Custom Price Header */
    .price-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 0px;
    }
    
    .ticker-header {
        color: #ffb900;
        font-size: 1.2rem;
        margin-top: -10px;
    }
    
    /* AI Insight Box */
    .insight-box {
        background-color: #002b36;
        border-left: 5px solid #ffb900;
        padding: 15px;
        margin-top: 20px;
    }

    /* Health Score Circular Display (Simplified) */
    .health-score-container {
        text-align: center;
        padding: 20px;
        border: 2px solid #ffb900;
        border-radius: 50%;
        width: 150px;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Bloomberg_logo.svg/1280px-Bloomberg_logo.svg.png", width=200)
    st.markdown("---")
    ticker_input = st.text_input("TICKER SYMBOL:", value="AAPL").upper()
    openai_api_key = st.text_input("OPENAI API KEY:", type="password")
    st.markdown("---")
    st.markdown("### SYSTEM STATUS")
    st.success("TERMINAL CONNECTED")
    st.info("REAL-TIME FEED: ACTIVE")

# --- INITIALIZE DATA ---
fetcher = DataFetcher(ticker_input)
explainer = AIExplainer(api_key=openai_api_key if openai_api_key else None)

if ticker_input:
    with st.spinner(f"REQUESTING DATA: {ticker_input}..."):
        stock_info = fetcher.get_info()
        
    if stock_info:
        # --- HEADER SECTION ---
        col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
        
        with col_h1:
            st.markdown(f"<div class='price-header'>${stock_info.get('price', 'N/A')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='ticker-header'>{ticker_input} | {stock_info.get('name')} | {stock_info.get('sector')}</div>", unsafe_allow_html=True)
        
        analyzer = Analyzer(stock_info)
        health_score = analyzer.calculate_health_score()
        risk_alerts = analyzer.get_risk_alerts()

        with col_h2:
            st.metric("FINANCIAL HEALTH", f"{health_score:.1f}/100")
        
        with col_h3:
            market_cap_bn = stock_info.get('market_cap', 0) / 1e9
            st.metric("MARKET CAP", f"{market_cap_bn:.2f}B")

        st.markdown("---")

        # --- DASHBOARD GRID ---
        col_main_1, col_main_2 = st.columns([1, 2])

        with col_main_1:
            # PANEL 1: KEY FUNDAMENTALS
            st.markdown("### <i class='fas fa-list'></i> FUNDAMENTALS", unsafe_allow_html=True)
            
            fundamental_metrics = {
                "P/E RATIO": f"{stock_info.get('pe_ratio', 'N/A')}",
                "EPS (TTM)": f"{stock_info.get('eps', 'N/A')}",
                "REV GROWTH": f"{stock_info.get('revenue_growth', 0)*100:.2f}%",
                "PROFIT MARGIN": f"{stock_info.get('profit_margin', 0)*100:.2f}%",
                "DEBT/EQUITY": f"{stock_info.get('debt_to_equity', 'N/A')}",
                "DIV YIELD": f"{stock_info.get('dividend_yield', 0)*100:.2f}%"
            }
            
            for label, value in fundamental_metrics.items():
                st.markdown(f"""
                    <div style='display: flex; justify-content: space-between; border-bottom: 1px solid #333; padding: 5px 0;'>
                        <span style='color: #888;'>{label}</span>
                        <span style='color: #00ff00; font-family: monospace;'>{value}</span>
                    </div>
                """, unsafe_allow_html=True)

            # PANEL 2: RISK ALERTS
            if risk_alerts:
                st.markdown("<br>### <i class='fas fa-exclamation-triangle'></i> RISK ALERTS", unsafe_allow_html=True)
                for alert in risk_alerts:
                    st.error(alert)
            else:
                st.markdown("<br>### <i class='fas fa-check-circle'></i> RISK PROFILE")
                st.success("NO MAJOR RISK ALERTS DETECTED")

        with col_main_2:
            # PANEL 3: PRICE HISTORY CHART
            history = fetcher.get_history()
            if history is not None and not history.empty:
                fig_price = go.Figure()
                fig_price.add_trace(go.Scatter(
                    x=history.index, 
                    y=history['Close'], 
                    fill='tozeroy',
                    line=dict(color='#ffb900', width=2),
                    name="Price"
                ))
                fig_price.update_layout(
                    template="plotly_dark",
                    title=f"{ticker_input} PRICE HISTORY (1Y)",
                    xaxis_title="DATE",
                    yaxis_title="PRICE (USD)",
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_price, use_container_width=True)

            # PANEL 4: REVENUE & NET INCOME
            revenue_trend = fetcher.get_revenue_trend()
            if revenue_trend is not None and not revenue_trend.empty:
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Bar(
                    x=revenue_trend.index.year,
                    y=revenue_trend.iloc[:, 0],
                    name="REVENUE",
                    marker_color='#ffb900'
                ))
                fig_trend.add_trace(go.Bar(
                    x=revenue_trend.index.year,
                    y=revenue_trend.iloc[:, 1],
                    name="NET INCOME",
                    marker_color='#00ff00'
                ))
                fig_trend.update_layout(
                    template="plotly_dark",
                    title="ANNUAL REVENUE & NET INCOME",
                    barmode='group',
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_trend, use_container_width=True)

        # --- AI ANALYST SECTION ---
        st.markdown("---")
        st.markdown("### <i class='fas fa-robot'></i> AI FINANCIAL ANALYST", unsafe_allow_html=True)
        
        col_ai_1, col_ai_2 = st.columns([1, 4])
        
        with col_ai_1:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("RUN AI ANALYSIS", use_container_width=True):
                with st.spinner("ANALYZING..."):
                    explanation = explainer.generate_explanation(stock_info, health_score, risk_alerts)
                    st.session_state['ai_explanation'] = explanation
        
        with col_ai_2:
            if 'ai_explanation' in st.session_state:
                st.markdown(f"<div class='insight-box'>{st.session_state['ai_explanation']}</div>", unsafe_allow_html=True)
            else:
                st.info("AWAITING ANALYSIS COMMAND. CLICK 'RUN AI ANALYSIS' TO START.")

        # PANEL 5: COMPANY SUMMARY
        with st.expander("VIEW FULL BUSINESS SUMMARY"):
            st.write(stock_info.get("summary"))

    else:
        st.error(f"TICKER NOT FOUND: {ticker_input}. VERIFY SYMBOL AND RE-ENTER.")
else:
    st.info("ENTER TICKER SYMBOL IN THE SIDEBAR TERMINAL.")
