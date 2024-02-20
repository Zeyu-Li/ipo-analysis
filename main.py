import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import re


def main():
    # Define the ticker symbol (e.g., MSFT for Microsoft)
    ticker_symbols = ["MSFT", "PYPL", "MMM", "AMZN", "EA"]
    # ticker_symbols = ["MSFT", "PYPL"]

    # Fetch historical data for the first 2 years from IPO
    try:
        tickers = pd.read_csv("tickers.csv")
    except Exception as err:
        print(err)
        return
    
    yf_dates = {}
    for ticker_symbol in ticker_symbols:
        start_date = tickers[tickers['Symbol'] == ticker_symbol]['Date added'].values[0]
        # max 1984 or date added
        start_date = max(start_date, "1984-01-01")
        year_pattern = r'(\d{4})-(\d{2})-(\d{2})'
        match = re.search(year_pattern, start_date)
        year_2 = int(match.group(1)) + 2
        end_date = f'{year_2}-{match.group(2)}-{match.group(3)}'
        # end date should be two years later
        yf_dates[ticker_symbol] = (start_date, end_date)
    
    # print(yf_dates)
    historical_data = {}
    for k, v in yf_dates.items():
        yf_ticker = yf.Ticker(k)
        historical_data[k] = yf_ticker.history(start=v[0], end=v[1])
        # print(historical_data[k])


    # Find the maximum start date among all datasets
    max_start_date = max(data.index.min() for data in historical_data.values())

    normalized_prices = []
    # normalize dates
    for k, v in historical_data.items():
        shift_amount = (max_start_date - v.index.min()).days
        v.index = v.index + pd.Timedelta(days=shift_amount)
        first_value = v.iloc[0]['Close']
        # Normalize by dividing each value by the first value
        normalized_history = v['Close'] / first_value
        normalized_prices.append(normalized_history)
        v["normalized"] = normalized_history
        # historical_data[k] = normalize_data(min_date, v)

    # print(historical_data)
    # TODO: normalize date and price
    # print(historical_data)
    # Plot the closing price as a line chart
    plt.figure(figsize=(10, 6))
    
    for k, v in historical_data.items():
        plt.plot(v.index, v["normalized"], label=f"{k} Closing Price")
    plt.xlabel("Date (Over Two years)")
    plt.ylabel("Price (Relative)")
    plt.title(f"{ticker_symbol} Stock Price (First 2 Years from IPO)")
    plt.grid(True)
    plt.legend()

    # Save the plot as an image file
    plt.savefig("stock_price_chart.png")
    print("Stock price chart saved as stock_price_chart.png")

    # Alternatively, you can display the plot interactively in a Jupyter Notebook or other interactive environments.
    # plt.show()

if __name__ == "__main__":
    main()