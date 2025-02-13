"""
multiple_stocks_data_collector.py

This script fetches detailed stock data for multiple symbols using the Alpha Vantage API.
It collects metrics such as open, high, low, price, volume, and more for each stock and
writes the data along with a timestamp to a CSV file.
"""

import os
import csv
import datetime
import requests

# === Configuration ===
API_KEY = os.getenv("AKGPPTHLE1M1XCEQ")  # Fetch API Key from GitHub Secrets
STOCKS = ["AAPL", "MSFT", "GOOG", "NVDA", "IBM", "TSLA", "AMZN", "META", "ORCL", "KO"]  # List of stock symbols
CSV_FILE = "multiple_stocks_data.csv"  # CSV file to store the collected data

def fetch_stock_data(symbol):
    """
    Fetches the latest stock data for the given symbol using Alpha Vantage.

    Returns:
        dict: Contains a timestamp, symbol, and several financial metrics,
              or None if an error occurs.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

    if "Global Quote" not in data or not data["Global Quote"]:
        print(f"Error: Unexpected data format or empty response for {symbol}.")
        return None

    quote = data["Global Quote"]
    try:
        stock_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "symbol": symbol,
            "open": float(quote.get("02. open", 0)),
            "high": float(quote.get("03. high", 0)),
            "low": float(quote.get("04. low", 0)),
            "price": float(quote.get("05. price", 0)),
            "volume": int(quote.get("06. volume", 0)),
            "latest_trading_day": quote.get("07. latest trading day", ""),
            "previous_close": float(quote.get("08. previous close", 0)),
            "change": float(quote.get("09. change", 0)),
            "change_percent": quote.get("10. change percent", "")
        }
    except ValueError as ve:
        print(f"Data conversion error for {symbol}: {ve}")
        return None

    print(f"[{stock_data['timestamp']}] {symbol} - Price: ${stock_data['price']:.2f}, Volume: {stock_data['volume']}")
    return stock_data

def write_to_csv(stock_data):
    """
    Appends a row of stock data to the CSV file. Creates the file with headers if it doesn't exist.
    """
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="") as csv_file:
        fieldnames = [
            "timestamp", "symbol", "open", "high", "low", "price", "volume",
            "latest_trading_day", "previous_close", "change", "change_percent"
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(stock_data)
    print(f"Data for {stock_data['symbol']} written to CSV.")

def main():
    """
    Fetch stock data and write to CSV.
    """
    print("Starting stock data collection...")
    for symbol in STOCKS:
        data = fetch_stock_data(symbol)
        if data:
            write_to_csv(data)
    print("Stock data collection completed.")

if __name__ == "__main__":
    main()
