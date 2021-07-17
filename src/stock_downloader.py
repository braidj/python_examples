#!/usr/bin/python3 env
import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials
import pprint



if __name__ == "__main__":

    stock = yf.download('BTC-USD', 
                      start='2020-08-01', 
                      end='2020-09-10', 
                      progress=False)

    print(stock.head())
    print(stock.all)


    # ticker = yf.Ticker('TSLA')
    # #stock = ticker.history(period="max")
    # #stock['Close'].plot(title="TSLA's stock price")

    # for k in ticker.info:
    #     print(f"{k}:\t{ticker.info[k]}")

    print("Complete")
