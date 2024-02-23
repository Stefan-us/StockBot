from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd
import csv

API_KEY = 'XVLMEBWYJ9X5CYWJ'  # Use your Alpha Vantage API key

def fetch_historical_data(symbol, time_window='100days'):
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
    # If a specific time window is needed, adjust the following line
    if time_window:
        data = data.head(int(time_window.replace('days', '')))
    data['symbol'] = symbol
    return data

def plot_historical_data(data, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(data['4. close'])
    plt.title(f'Historical Daily Closing Prices for {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price ($)')
    plt.grid(True)
    plt.show()

def save_historical_data_to_csv(data, symbol, filename='historical_stock_data.csv'):
    data.to_csv(filename)
    print(f"Historical stock data for {symbol} has been saved to {filename}.")

def fetch_current_data(symbol):
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data, _ = ts.get_quote_endpoint(symbol=symbol)
    return data.iloc[0].to_dict()

def save_to_csv(stock_data_list, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['symbol', 'date', 'open', 'high', 'low', 'price', 'volume']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for stock_data in stock_data_list:
            row = {
                'symbol': stock_data['01. symbol'],
                'date': stock_data['07. latest trading day'],
                'open': stock_data['02. open'],
                'high': stock_data['03. high'],
                'low': stock_data['04. low'],
                'price': stock_data['05. price'],
                'volume': stock_data['06. volume']
            }
            writer.writerow(row)

def main():
    choice = input("Enter '1' for historical data of one stock, '2' for current data of multiple stocks: ")
    if choice == '1':
        symbol = input("Enter the stock symbol (e.g., AAPL for Apple): ").upper()
        time_window = input("Enter the time window for historical data (e.g., 100days): ")
        historical_data = fetch_historical_data(symbol, time_window)
        plot_historical_data(historical_data, symbol)
        save_historical_data_to_csv(historical_data, symbol)
    elif choice == '2':
        filename = 'current_stock_data.csv'
        symbols_input = input("Enter stock symbols separated by comma (e.g., AAPL,MSFT,GOOGL): ")
        symbols = [symbol.strip().upper() for symbol in symbols_input.split(',')]
        stock_data_list = [fetch_current_data(symbol) for symbol in symbols]
        save_to_csv(stock_data_list, filename)
        print(f"Current stock data for {', '.join(symbols)} has been saved to {filename}.")
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
