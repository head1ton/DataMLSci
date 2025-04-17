import datetime
import os

import cufflinks as cf
import pandas as pd
import streamlit as st
import yfinance as yf

cf.go_offline(connected=True)

st.set_page_config(layout='wide')

base_dir = os.path.join(os.path.dirname(__file__))

st.markdown("""
# Stock Price

Shown are the stock price data for query companies!
""")
st.write('---')

st.sidebar.subheader('Query parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))

file_path = os.path.join(base_dir, 'constituents_symbols.txt')
ticker_list = pd.read_csv(file_path)

tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list)
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
# for key, value in tickerData.info.items():
#     print(key, ' - ', value)
string_logo = '<h1 style="text-align: left;">%s</h1>' % tickerData.info['displayName']
st.markdown(string_logo, unsafe_allow_html=True)

string_name = tickerData.info['longName']
st.header('**%s**' % string_name)

string_summary = tickerData.info['longBusinessSummary']
st.info(string_summary)

st.header('**Ticker data**')
st.write(tickerDf)

date_period = end_date - start_date

st.header('**Bollinger Bands**')
qf = cf.QuantFig(tickerDf, title='First Quant Figure', showlegend=True, name='GS')
# qf.add_bollinger_bands(periods=date_period, boll_std=2)
qf.add_bollinger_bands()


#### 이거 오류나네 cufflinks 버전도 오래되고.. 이렇게 저렇게 수정해도 안돈당..
# fig = qf.iplot(asFigure=True)
# st.plotly_chart(fig)

st.write('---')
# # st.write(tickerData.info)
for key, value in tickerData.info.items():
    st.write(key, ' - ', value)
#     print(key, ' - ', value)