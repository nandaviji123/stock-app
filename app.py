import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.express as px
from stocknews import StockNews

st.title("Stock Dashboard")

ticker = st.sidebar.text_input('Ticker', value='MSFT')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

if ticker:
    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        st.warning(f"No data found for ticker {ticker}. Check symbol or date range.")
    else:
        # Handle MultiIndex
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]

        # Price chart
        fig = px.line(data, x=data.index, y='Close', title=f'{ticker} Closing Prices')
        st.plotly_chart(fig)

        # Tabs
        pricing_data, news = st.tabs(["Pricing Data", "Top 10 News"])

        with pricing_data:
            st.header('Price Movements')
            st.write(data)

            # % Change Calculation
            data2 = data.copy()
            data2['% Change'] = data2['Close'].pct_change()
            data2.dropna(inplace=True)

            # Annualized Return & Std Dev
            annual_return = data2['% Change'].mean() * 252 * 100
            stdev = data2['% Change'].std() * np.sqrt(252) * 100

            st.write(data2)
            st.write(f"**Annual Return:** {annual_return:.2f}%")
            st.write(f"**Annualized Volatility (Std Dev):** {stdev:.2f}%")

        with news:
            st.header(f'News of {ticker}')
            sn = StockNews(ticker, save_news=False)
            df_news = sn.read_rss()
            for i in range(min(10, len(df_news))):
                st.subheader(f'News {i+1}')
                st.write(df_news['published'][i])
                st.write(df_news['title'][i])
                st.write(df_news['summary'][i])
                st.write(f"Title Sentiment: {df_news['sentiment_title'][i]}")
                st.write(f"News Sentiment: {df_news['sentiment_summary'][i]}")
else:
    st.info("Enter a ticker symbol to fetch data.")

    
