import streamlit as st
import datetime
import appdirs as ad
ad.user_cache_dir = lambda *args: "/tmp"
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

# Specify title and logo for the webpage.
st.set_page_config(page_icon=":bar_chart:", page_title='My Website', layout='centered')

# Sidebar
st.sidebar.title("Input Information")
symbol = st.sidebar.text_input('Please enter the stock first symbol:', "NVDA").upper()
symbol2 = st.sidebar.text_input('Please enter the stock second symbol:', "KO").upper()

# Selection for a specific time frame.
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

# Text above
st.title(f"{symbol} & {symbol2}")

stock = yf.Ticker(symbol)
stock2 = yf.Ticker(symbol2)

# Display company's basics
try:
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Company Name:** {stock.info['longName']}")
        st.write(f"**Sector:** {stock.info['sector']}")
        st.write(f"**Address:** {stock.info['address1']}")
        st.write(f"**Company Beta:** {stock.info['beta']}")
    with col2:
        st.write(f"**Company Name:** {stock2.info['longName']}")
        st.write(f"**Sector:** {stock2.info['sector']}")
        st.write(f"**Address:** {stock2.info['address1']}")
        st.write(f"**Company Beta:** {stock2.info['beta']} ")
except KeyError:
    st.error("Failed to fetch company information.")

# Fetch historical data
data = stock.history(start=sdate, end=edate)
data2 = stock2.history(start=sdate, end=edate)

# Combine Close and Volume data from both stocks
if not data.empty and not data2.empty:
    chart_data = pd.DataFrame({
        f"{symbol} Close": data['Close'],
        f"{symbol2} Close": data2['Close'],
        f"{symbol} Volume": data['Volume'],
        f"{symbol2} Volume": data2['Volume']
    })

    # Plot area charts
    st.area_chart(chart_data[[f"{symbol} Close", f"{symbol2} Close"]],x_label='Date',y_label='Close')
    st.area_chart(chart_data[[f"{symbol} Volume", f"{symbol2} Volume"]],x_label='Date',y_label='Volume')
else:
    st.error("Failed to fetch historical data.")
