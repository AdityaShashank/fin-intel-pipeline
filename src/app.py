import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv
import pandas as pd

# 1. Setup
load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.set_page_config(page_title="Fin-Intel Dashboard", layout="wide")
st.title("🛰️ Financial Intelligence Feed")

# 2. Fetching Data
def get_data():
    # Pull latest 20 signals from Supabase
    response = supabase.table("financial_signals").select("*").order("published_at", desc=True).limit(20).execute()
    return pd.DataFrame(response.data)

try:
    df = get_data()
    
    # 3. Top-Level Metrics
    avg_score = df['sentiment_score'].mean()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg Sentiment (NVDA)", f"{avg_score:.2f}", delta="Bullish" if avg_score > 0.1 else "Bearish")
    with col2:
        st.metric("Signals Ingested", len(df))
    with col3:
        # Mocking the balance for now based on your 25-limit
        st.metric("API Quota", "Healthy", delta="25/day")

    st.divider()

    # 4. The Intelligence Feed
    st.subheader("🤖 AI-Scored Market Signals")
    for _, row in df.iterrows():
        # Color-coding the label
        label_color = "🟢" if row['sentiment_label'] == "Bullish" else "🔴" if row['sentiment_label'] == "Bearish" else "⚪"
        
        with st.expander(f"{label_color} {row['sentiment_label']} | {row['headline'][:90]}..."):
            st.write(f"**Full News:** {row['headline']}")
            st.write(f"**AI Confidence Score:** {row['sentiment_score']}")
            st.write(f"**Published:** {row['published_at']}")
            st.link_button("Read Source Article", row['url'])

except Exception as e:
    st.error(f"Waiting for data... or check connection: {e}")