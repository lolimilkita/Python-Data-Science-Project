import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf

st.set_option('deprecation.showPyplotGlobalUse', False)

row1_1, row1_2 = st.columns((1,1))

with row1_1:
    st.title("500 Stock Price Web App")

with row1_2:
    st.write(
    """
    ##
    Aplikasi ini mengambil data daftar **S&P 500** (dari Wikipedia) dan **harga stock closing** yang sesuai (tahun-ke-tanggal)!
    """)
    st.markdown("""
    * **Python library:** base64, pandas, streamlit, matplotlib, yfinance
    * **Sumber Data:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
    """)

st.write("""
***
""")


st.sidebar.header('Fitur Kostumisasi')

@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

st.header('Perusahaan sesuai dengan yang Dipilih Sectornya')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

# Download S&P500 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# https://pypi.org/project/yfinance/

data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Harga Closing dari kueri Symbol
def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  plt.figure(figsize = (12,8))
  plt.fill_between(df.Date, df.Close, color='blue', alpha=0.3)
  plt.plot(df.Date, df.Close, color='blue', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('Closing Price', fontweight='bold')
  return st.pyplot()

num_company = st.slider('Jumlah Perusahaan', 1, 10)

st.header('Stock Closing Price')
for i in list(df_selected_sector.Symbol)[:num_company]:
    price_plot(i)