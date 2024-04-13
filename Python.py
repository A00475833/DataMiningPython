import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt


st.set_option('deprecation.showPyplotGlobalUse', False)


def fetch_crypto_data(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?x_cg_demo_api_key=CG-JbCTLwjQBhPiMTsYw1SkAhtN"
    params = {"vs_currency": "usd", "days": days}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()['prices']
        df = pd.DataFrame(data, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    else:
        st.error("Error fetching data")
        return None


def main():
    st.title("Cryptocurrency Analysis and Comparison App")

    
    coins_list_url = "https://api.coingecko.com/api/v3/coins/list?x_cg_demo_api_key=CG-JbCTLwjQBhPiMTsYw1SkAhtN"
    coins_list_response = requests.get(coins_list_url)
    coins_dict = {coin['id']: coin['name'] for coin in coins_list_response.json()}

    
    mode = st.radio("Choose an option:", ('View Single Cryptocurrency', 'Compare Two Cryptocurrencies'))

    if mode == 'View Single Cryptocurrency':
        selected_crypto = st.selectbox("Select a cryptocurrency", options=list(coins_dict.values()))
        crypto_id = [key for key, name in coins_dict.items() if name == selected_crypto][0]

        
        crypto_data = fetch_crypto_data(crypto_id, 365)
        if crypto_data is not None:
            
            st.subheader(f"Price Trend for {selected_crypto}")
            plt.figure(figsize=(10, 6))
            plt.plot(crypto_data['timestamp'], crypto_data['price'])
            plt.title(f"{selected_crypto} Price Trends Over Last Year")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            st.pyplot()

            
            highest_price = crypto_data['price'].max()
            lowest_price = crypto_data['price'].min()
            peak_price_date = crypto_data.loc[crypto_data['price'].idxmax(), 'timestamp']
            lowest_price_date = crypto_data.loc[crypto_data['price'].idxmin(), 'timestamp']
            st.write(f"Peak Price: ${highest_price:.2f}")
            st.write(f"Lowest Price: ${lowest_price:.2f}")
            st.write(f"Highest Price on: {peak_price_date}")
            st.write(f"Lowest Price on: {lowest_price_date}")

    elif mode == 'Compare Two Cryptocurrencies':
        coin_input_1 = st.selectbox("Select the first cryptocurrency", options=list(coins_dict.values()), key='1')
        coin_id_1 = [coin_id for coin_id, name in coins_dict.items() if name == coin_input_1][0]

        coin_input_2 = st.selectbox("Select the second cryptocurrency", options=list(coins_dict.values()), key='2')
        coin_id_2 = [coin_id for coin_id, name in coins_dict.items() if name == coin_input_2][0]

        
        time_frames = {"1 Week": 7, "1 Month": 30, "1 Year": 365}
        selected_time_frame = st.selectbox("Select the time frame", options=list(time_frames.keys()))

        
        coin_data_1 = fetch_crypto_data(coin_id_1, time_frames[selected_time_frame])
        coin_data_2 = fetch_crypto_data(coin_id_2, time_frames[selected_time_frame])

        if coin_data_1 is not None and coin_data_2 is not None:
            
            st.subheader(f"Price comparison between {coin_input_1} and {coin_input_2} over {selected_time_frame}")
            plt.figure(figsize=(10, 6))
            plt.plot(coin_data_1['timestamp'], coin_data_1['price'], label=coin_input_1)
            plt.plot(coin_data_2['timestamp'], coin_data_2['price'], label=coin_input_2)
            plt.title(f"Price Comparison Over {selected_time_frame}")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.legend()
            st.pyplot()

if __name__ == "__main__":
    main()
