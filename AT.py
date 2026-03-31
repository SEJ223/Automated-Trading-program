import yfinance as yf #For downloading stock 
import pandas as pd #For data manipulation
import numpy as np #For numerical operations
import matplotlib.pyplot as plt #For plotting 

#ask the user to input stock ticker and start and end date of the stock ticker data they want to analyze
Stock_string = input("Enter the stock ticker: ")
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

ticker = Stock_string.upper() #Converts the stock ticker to uppercase


#fetch the historcal stock data
data =yf.download(ticker, start=start_date, end=end_date)

#prints out the first few rows
print(data.head())

#Calcuates the moving Averages
short_window = 50
Long_window = 300

data['SMA50'] = data['Close'].rolling(window=short_window).mean()
data['SMA200'] = data['Close'].rolling(window=Long_window).mean()

#Define the trading signals
data['Signal'] = 0
data.loc[data['SMA50'] > data['SMA200'], 'Signal'] = 1
data.loc[data['SMA50'] < data['SMA200'], 'Signal'] = -1

#Creates postions
data['Position'] = data['Signal'].shift(1)

#calcuate daily percentage change
data['Daily_Return'] = data['Close'].pct_change()

#Calculate strategy returns
data['Strategy_Return'] = data['Position'] * data['Daily_Return']

#Calculate cumulative returns
data['Cumulative_Strategy_Return'] = (1 + data['Strategy_Return']).cumprod()
data['Cumulative_Market_Return'] = (1 + data['Daily_Return']).cumprod()

#Plot the stock price and SMAs:
plt.figure(figsize=(12,6))
plt.plot(data['Close'], label = 'close price', alpha = 0.5)
plt.plot(data['SMA50'], label = 'SMA50', alpha = 0.75)
plt.plot(data['SMA200'], label = 'SMA300', alpha = 0.75)
plt.title(f'{ticker} Price and Moving Averages')
plt.legend()
plt.show()

#plots the Cumlative returns
plt.figure(figsize=(12,6))
plt.plot(data['Cumulative_Market_Return'],label ='Market Return', alpha = 0.75)
plt.plot(data['Cumulative_Strategy_Return'], label = 'Strategy Return', alpha = 0.75)
plt.title("Cumulative Returns")
plt.legend()
plt.show()

total_strategy_return = data['Cumulative_Strategy_Return'].iloc[-1] - 1
total_market_return = data['Cumulative_Market_Return'].iloc[-1] - 1

print(f'Total Strategy Return: {total_strategy_return:.2%}')
print(f'Total Market Return: {total_market_return:.2%}')