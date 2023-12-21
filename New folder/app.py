import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
import base64



def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('146.png')



def get_selected_stock_data(selected_symbols, start_date, end_date):
        selected_data = {}
        for symbol in selected_symbols:
            try:
                stock_data = yf.download(symbol, start=start_date, end=end_date)
                if not stock_data.empty:
                    selected_data[symbol] = stock_data
                else:
                    st.warning(f"No data available for {symbol}.")
            except Exception as e:
                st.error(f"Failed to fetch data for {symbol}. Error: {e}")
        return selected_data




st.markdown(
        """
        <style>
        .st-cj, .st-cc, .st-db {
            font-family: "Ink Free", Times, serif;
            color: #FFC0CB;
        }
        .st-df, .st-cf, .st-eb {
            font-family: "Ink Free", Times, serif;
            color: #FA8072;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
        st.header("STOCK PRICE PREDICTION")
        selected_symbols = st.multiselect('Select symbols', ('ADBE', 'GOOG', 'AMZN', 'F', 'UPWK', 'EBAY', 'DDOG', 'AAPL', 'TLSA', 'UPST', 'UBER', 'MDB'))  
        start_date = st.date_input('Start date')
        end_date = st.date_input('End date')
        
        selected_data = None

        if st.button('Submit'):
            if selected_symbols and start_date and end_date:
                selected_data = get_selected_stock_data(selected_symbols, start_date, end_date)
            else:
                st.warning("Please select symbols and date range to fetch data.")
                
                
        display_option = st.radio("Select Display Option", ["Prediction Price", "Graphs", "Analysis"])
    



        if display_option == "Prediction Price":
         if selected_data is not None:
           for symbol in selected_symbols:
            data = selected_data.get(symbol)

            if data is not None:
                if 'Date' in data.columns:
                    X = data[['Date']]
                else:
                    data['Date'] = data.index
                    X = data[['Date']]

                y = data['Close']
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                model = LinearRegression()
                model.fit(X_train, y_train)

                st.markdown(f"<h3 style='color: #FFC0CB'>Predicted Prices - {symbol}</h3>", unsafe_allow_html=True)

                prediction_days = 1  
                last_date = data.index[-1]
                prediction_dates = [last_date + timedelta(days=i) for i in range(1, prediction_days + 1)]
                prediction_dates_ord = [date.toordinal() for date in prediction_dates]
                predictions = model.predict([[date] for date in prediction_dates_ord])
                current_price = data['Close'].iloc[-1]

                for i in range(prediction_days):
                    predicted_date = datetime.fromordinal(prediction_dates[i].toordinal())

                    price_difference = predictions[i] - current_price

                    if price_difference > 0:
                        prediction_message = f"The predicted price is higher  ."
                        prediction_symbol = "↑"
                        prediction_color = "#90EE90"
                    elif price_difference < 0:
                        prediction_message = f"The predicted price is lower ."
                        prediction_symbol = "↓"
                        prediction_color = "#CD5C5C"
                    else:
                        prediction_message = f"The predicted price is the same as the current price."
                        prediction_symbol = "→"
                        prediction_color = "#ADD8E6"

                   
                    style = f"border-radius: 15px; padding: 10px; margin: 10px; background-color: {prediction_color}; color: black;"
                    st.markdown(f"<div style='{style}'><b>{prediction_message} {prediction_symbol}</b></div>", unsafe_allow_html=True)
                    st.write(f"<span style='color:#FFDAB9;'>current Price: ${current_price:.2f}</span>", unsafe_allow_html=True)
                    st.write("**Raw Data:**")
                    st.write(data)




        if display_option == "Graphs":
         if selected_data is not None:
          for symbol, data in selected_data.items():
            fig, ax = plt.subplots(figsize=(12, 6))

           
            ax.plot(data.index, data['Close'], label='Close Price', color='blue')
            ax.plot(data.index, data['Open'], label='Open Price', color='green')

        
            today_price = data['Close'].iloc[-1]
            ax.plot(data.index[-1], today_price, 'ro', label="Today's Price")

            last_few_points = 5
            x = range(len(data) - last_few_points, len(data))
            y = data['Close'].tail(last_few_points)

            if len(x) == len(y):
                m, b = np.polyfit(x, y, 1)
                predicted_prices = [m * i + b for i in range(len(data))]
                ax.plot(data.index, predicted_prices, label='Predicted Price', color='red', linestyle='--')
                
            
            ax.set_xlabel('Date')
            ax.set_ylabel('Price (USD)')
            ax.set_title(f'Close Price, Open Price, and Predicted Price Trend for {symbol}')
            ax.legend()

            open_price = data['Open'].iloc[-1]
            close_price = data['Close'].iloc[-1]
            current_price = data['Close'].iloc[-1]
                    
            st.write(f"**{symbol} Prices**")
            st.write(f"<span style='color:black;'> yestday's Open Price: ${open_price:.2f}</span>", unsafe_allow_html=True)
            st.write(f"<span style='color:black;'> yestday's Close Price: ${close_price:.2f}</span>", unsafe_allow_html=True)
            st.write(f"<span style='color:black;'>current Price: ${current_price:.2f}</span>", unsafe_allow_html=True)
            st.pyplot(fig)





        if display_option == "Analysis":
            if selected_data is not None:
                st.markdown("<h2 style='color: #E6E6FA'>Statistical Analysis</h2>", unsafe_allow_html=True)

                for symbol, data in selected_data.items():
                    st.write(f"**{symbol}**")

                    stats_data = {
                        "Metric": ["Mean", "Standard Deviation ", "Maximum ",
                                "Minimum ", "Median"],
                        "Value": [data['Close'].mean(), data['Close'].std(), data['Close'].max(),
                                data['Close'].min(), data['Close'].median()]
                    }

                    stats_df = pd.DataFrame(stats_data)
                    st.write(stats_df)

if __name__ == '__main__':
        main()