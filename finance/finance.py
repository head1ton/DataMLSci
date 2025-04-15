import yfinance as yf
import streamlit as st

st.write("""
# Stock Price App

Shown are the stock **closing price** and ***volume*** of META!
""")

#define the ticker symbol
tickerSymbol = 'META'
# tickerSymbol = 'GOOG'
# tickerSymbol = 'AAPL'

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2015-3-31', end='2025-3-31')
# Open  High    Low Close   Volume  Dividends   Stock Splits

st.write("""
## Combined Price
""")
st.line_chart(tickerDf[['Close', 'Volume']])
st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume Price
""")
st.line_chart(tickerDf.Volume)
