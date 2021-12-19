import yfinance as yf
import streamlit as st
import pandas as pd

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

row1_1, row1_2 = st.columns((3,1))

with row1_1:
    st.title("Simple Stock Price Of Meta Platforms Inc (Facebook)")

with row1_2:
    st.write(
    """
    ##
    Berikut adalah harga stock dan volume dari Meta Platforms!
    Data dari tahun 2010 Desember 17 sampai tahun 2021 Desember 17
    """)

tickerSymbol = 'FB'

tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start='2010-12-17', end='2021-12-17')

st.subheader('Closing Price')
st.line_chart(tickerDf.Close)

st.subheader('Volume Price')
st.line_chart(tickerDf.Volume)