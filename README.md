# Binance Futures Trading Bot

A simplified Python trading bot for Binance Futures Testnet supporting market, limit, stop-market, stop-limit, and OCO orders with basic order management via CLI.

## Features

- Place MARKET, LIMIT, STOP_MARKET, STOP_LIMIT, and OCO orders
- Cancel all open orders for a trading pair
- Command-line interface for easy order placement
- Uses Binance Futures Testnet for safe testing
- Basic logging of order status and errors

## Requirements

- Python 3.7+
- `python-binance` library
- A Binance API key & secret for Futures Testnet

## Setup

1. Clone the repo:

   ```bash
   git clone https://github.com/sathwika16/binance_bot.git
   cd binance_bot
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create a config.py file with your API credentials:

python
Copy
Edit
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"
Run the bot via CLI:

bash
Copy
Edit
python cli.py --symbol BTCUSDT --side BUY --quantity 0.01 --order_type MARKET
Usage Examples
Place a Market Buy order:

bash
Copy
Edit
python cli.py --symbol BTCUSDT --side BUY --quantity 0.01 --order_type MARKET
Place a Limit Sell order:

bash
Copy
Edit
python cli.py --symbol BTCUSDT --side SELL --quantity 0.01 --order_type LIMIT --price 30000
Place an OCO order:

bash
Copy
Edit
python cli.py --symbol BTCUSDT --side SELL --quantity 0.01 --order_type OCO --price 110000 --stop_price 105000 --price_limit 104500
Cancel all open orders for a symbol:

bash
Copy
Edit
python cli.py --symbol BTCUSDT --cancel
