
import os
import csv
import time
import datetime
import schedule
import requests

# === Configuration ===
API_KEY = "9OCRMK3V67KUE7QD"  # Replace with your actual API key
STOCKS = ["AAPL", "MSFT","GOOG","NVDA","IBM","TSLA","AMZN","META","CAT","AMD"]        # List of stock symbols to track
CSV_FILE = "multiple_stocks_data.csv"     # CSV file to store the collected data

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

def job():
    """
    Scheduled job: fetch data for each stock symbol and write to CSV.
    """
    print("Starting data collection job for multiple stocks...")
    for symbol in STOCKS:
        data = fetch_stock_data(symbol)
        if data:
            write_to_csv(data)
    print("Job finished.\n")

def main():
    # Schedule the job to run every hour.
    schedule.every(0.01).hours.do(job)
    job()  # Run once immediately

    print("Scheduler started. Data will be collected every hour. Press Ctrl+C to exit.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Data collection stopped.")

if __name__ == "__main__":
    main()
