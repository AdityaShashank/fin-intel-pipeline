import streamlit as st
import pandas as pd
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# --- Setup ---
st.set_page_config(page_title="Market Intel Dashboard", layout="wide")
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@st.cache_data(ttl=600) # Cache for 10 minutes to save Supabase bandwidth
def load_all_data():
    response = supabase.table("financial_signals").select("*").execute()
    return pd.DataFrame(response.data)

# --- UI & Logic ---
st.title("🛰️ Professional Financial Intelligence")

try:
    df = load_all_data()
    df['published_at'] = pd.to_datetime(df['published_at'])
    df['date'] = df['published_at'].dt.date

    # 1. Sidebar Filter
    st.sidebar.header("Market Filters")
    unique_tickers = sorted(df['ticker'].unique())
    selected_ticker = st.sidebar.selectbox("Select Target Company", options=unique_tickers)

    # 2. Key Metrics for Selected Company
    filtered_df = df[df['ticker'] == selected_ticker]
    avg_score = filtered_df['sentiment_score'].mean()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(f"{selected_ticker} Sentiment", f"{avg_score:.2f}")
        if avg_score > 0.15:
            st.success("💎 Trend: BULLISH Momentum")
        elif avg_score < -0.15:
            st.error("⚠️ Trend: BEARISH Pressure")
        else:
            st.info("⚖️ Trend: NEUTRAL / Sideways")

    # 3. Trendy Graph (Time Series)
    with col2:
        st.subheader(f"📈 {selected_ticker} Sentiment Over Time")
        daily_trend = filtered_df.groupby('date')['sentiment_score'].mean()
        st.line_chart(daily_trend)

    st.divider()

    # 4. Market Leaderboard (Comparison of all tracked stocks)
    st.subheader("🏆 Market Leaderboard (Avg Sentiment)")
    leaderboard = df.groupby('ticker')['sentiment_score'].mean().sort_values(ascending=False)
    st.bar_chart(leaderboard)

    # 5. Live Feed
    st.subheader("📰 Recent AI-Scored Signals")
    for _, row in filtered_df.head(10).iterrows():
        with st.expander(f"{row['sentiment_label']} | {row['headline'][:80]}..."):
            st.write(f"**Score:** {row['sentiment_score']}")
            st.link_button("View Source", row['url'])

except Exception as e:
    st.error(f"Connect to Supabase to see data. Error: {e}")