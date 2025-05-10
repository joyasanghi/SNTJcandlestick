import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go

BASE_URL = "https://api-sntj.grakzjc49jfnj.ap-southeast-2.cs.amazonlightsail.com/v0"

# Function to fetch OHLC data
def get_ohlc_data(symbol):
    endpoint = f"/ohlc/{symbol}/"
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        ohlc_data = response.json()

        if not ohlc_data:
            st.error(f"No OHLC data available for {symbol}.")
            return None
        
        ohlc_df = pd.DataFrame(ohlc_data)
        ohlc_df['Date'] = pd.to_datetime(ohlc_df['timestamp_ms'], unit='ms')
        ohlc_df['Open'] = pd.to_numeric(ohlc_df['adj_open'], errors='coerce')
        ohlc_df['High'] = pd.to_numeric(ohlc_df['adj_high'], errors='coerce')
        ohlc_df['Low'] = pd.to_numeric(ohlc_df['adj_low'], errors='coerce')
        ohlc_df['Close'] = pd.to_numeric(ohlc_df['adj_close'], errors='coerce')
        ohlc_df = ohlc_df.dropna(subset=['Open', 'High', 'Low', 'Close'])

        return ohlc_df
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching OHLC data: {e}")
        return None

# Function to plot OHLC data as a candlestick chart (without volume)
def plot_candlestick_data(ohlc_df):
    if ohlc_df is not None:
        fig = go.Figure()

        # Plot the OHLC data as a candlestick chart
        fig.add_trace(go.Candlestick(
            x=ohlc_df['Date'],
            open=ohlc_df['Open'],
            high=ohlc_df['High'],
            low=ohlc_df['Low'],
            close=ohlc_df['Close'],
            name="Candlestick"
        ))

        # Update layout for the figure
        fig.update_layout(
            title=f"Candlestick Chart for {symbol}",
            xaxis_title="Date",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False  # Hide the range slider for a cleaner chart
        )

        st.plotly_chart(fig, use_container_width=True)

# Streamlit layout
st.title("SNTJ Stock Screener")

symbol = "AAPL" # SET SYMBOL HERE

if symbol:
    ohlc_data = get_ohlc_data(symbol)

    if ohlc_data is not None:
        plot_candlestick_data(ohlc_data)  # Only plot the candlestick chart without volume
    else:
        st.error(f"Could not fetch OHLC data for {symbol}. Please try again.")
