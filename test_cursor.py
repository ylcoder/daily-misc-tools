import yfinance as yf
import pandas as pd
# import talib as ta

def fetch_price(ticker, period='1mo', interval='1d'):
  return yf.Ticker(ticker).history(period=period)

def fetch_and_calculate_moving_averages(ticker, period='2y', interval='1d', lastn=10):
  # Fetch historical data for FXI
  fxi = yf.Ticker(ticker)
  # Fetch at least 200 days of historical data
  hist = fxi.history(period=period, interval=interval)

  win50 = 50
  win200 = 200
  if interval == '1wk':
    win50 = 10
    win200 = 40
  elif interval == '1mo':
    win50 = 2
    win200 = 8

  if len(hist) < win50:
    win50 = len(hist)
  if len(hist) < win200:
    win200 = len(hist)

  # Calculate the 50-day and 200-day moving averages
  hist['MA50'] = hist['Close'].rolling(window=win50).mean()
  hist['MA200'] = hist['Close'].rolling(window=win200).mean()

  # Display the relevant columns for the last 10 days
  result = hist[['Close', 'MA50', 'MA200']].tail(lastn)
  print(result)
  return hist[['Close', 'MA50', 'MA200']]

if __name__ == "__main__":
    df = fetch_and_calculate_moving_averages('FXI')
    print(df)

    # Plot the price and moving averages
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df['Close'], label='Price')
    plt.plot(df.index, df['MA50'], label='50-day MA')
    plt.plot(df.index, df['MA200'], label='200-day MA')
    plt.title('Price and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()
