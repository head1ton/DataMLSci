import pandas as pd
import streamlit as st

st.set_page_config(layout='wide')

st.markdown("""
# **Binance Price**

A simple cryptocurrency price app pulling price data from *Binance API*.
""")

st.header('**Selected Price**')

df = pd.read_json('https://api.binance.com/api/v3/ticker/24hr')
# print(list(df.symbol))
# print(list(cryptoList.keys()))
# print(list(cryptoList.keys())[1])
# print(list(df.symbol).index('ETHBUSD'))

def round_value(input_value):
    if input_value.values > 1:
        a = float(round(input_value.iloc[0], 2))
    else:
        a = float(round(input_value.iloc[0], 8))
    return a

col1, col2, col3 = st.columns(3)

cryptoList = {
    'Price 1': 'BTCBUSD',
    'Price 2': 'ETHBUSD',
    'Price 3': 'BNBBUSD',
    'Price 4': 'XRPBUSD',
    'Price 5': 'ADABUSD',
    'Price 6': 'DOGEBUSD',
    'Price 7': 'SHIBBUSD',
    'Price 8': 'DOTBUSD',
    'Price 9': 'MATICBUSD'
}

for i in range(len(cryptoList.keys())):
    selected_crypto_label = list(cryptoList.keys())[i]
    selected_crypto_index = list(df.symbol).index(cryptoList[selected_crypto_label])
    selected_crypto = st.sidebar.selectbox(selected_crypto_label, df.symbol, selected_crypto_index, key=str(i))

    col_df = df[df.symbol == selected_crypto]
    col_price = round_value(col_df.weightedAvgPrice)
    col_percent = f'{float(col_df.priceChangePercent.iloc[0])}%'
    if i < 3:
        with col1:
            st.metric(selected_crypto, col_price, col_percent)
    if 2 < i < 6:
        with col2:
            st.metric(selected_crypto, col_price, col_percent)
    if i > 5:
        with col3:
            st.metric(selected_crypto, col_price, col_percent)

st.header('**All Price**')
st.dataframe(df)

st.markdown("""
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)