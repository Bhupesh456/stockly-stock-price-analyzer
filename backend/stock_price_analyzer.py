import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf                                
from datetime import datetime

print("============  Stock Market Analyser =========== ")

while True :               # Main program Loop
    while True:            # Market Selection Loop

        market = input("Choose the Market (NSE or NASDAQ) or Q to Quit:").upper()

        if market == "Q":
           break

        if market in ["NSE","NASDAQ"]:
            break
        else:
            print("Invalid Market. Please choose either NSE or NASDAQ.")

    if market == "Q":
        print("Thanks for using the Stock Market Analyser. See you again !!!")
        break

    symbol = input("Enter the stock symbol :").upper()     
    
    if market == "NSE":
        symbol += ".NS"
  
    try: 
        stock = yf.Ticker(symbol)         # Get the stock information using yfinance
        info = stock.info              

        name = info.get("longName","N/A")
        price = info.get("currentPrice")
        prev_price= info.get("previousClose")
        currency = info.get("currency")

        if currency is None:                    # Handle cases where currency is not available
            if symbol.endswith(".NS"):
                currency = "₹"
            else:
                currency = "$"
        

        # Print the Stock Information

        print("\n=============================================")

        print(f" Company Name: {name}")
        print(f" Current Price: {price} {currency}")
        
        if price and prev_price:
            change = price - prev_price
            percent = (change/prev_price)*100
            print(f" Change : {change:+.2f} ({percent:+.2f}%)")
        
        today = datetime.today().strftime("%Y-%m-%d")      # Get today's date

        print("\n=============================================")

        # Download Historical Data and Calculate Moving Averages

        df = yf.download(symbol, start= "2025-01-10", end = today, interval="1d")

        df["7_day_MA"] = df["Close"].rolling(window=7).mean()
        df["30_day_MA"] = df["Close"].rolling(window=30).mean()

        # Plot the Graph

        plt.figure(figsize=(10,5))
        plt.plot(df["Close"],label="Daily Closing Price")
        plt.plot(df["7_day_MA"],label="7 Day MA")
        plt.plot(df["30_day_MA"],label="30 Day MA")
        plt.title(f" {symbol} : Stock Price Analysis")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.show()

    
    except Exception as e:
        print("Invalid Symbol or Network error\n")