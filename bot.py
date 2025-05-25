from binance.client import Client
from binance.enums import *
from logger import setup_logger

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.logger = setup_logger()
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        self.logger.info("Initialized Binance Futures Testnet Client")

    def place_order(self, symbol, side, quantity, order_type="MARKET", price=None, stop_price=None, price_limit=None):
        try:
            if order_type == "OCO":
                # OCO order on Binance Futures requires futures_create_order with special parameters
                # Binance Futures doesn't officially support OCO orders via API, so manual OCO via two orders or special API calls are needed.
                # Here, try futures_create_order with STOP_MARKET + LIMIT, handle separately or log error.
                # For simplicity, we'll do manual OCO via two orders here.
                raise NotImplementedError("OCO orders must be implemented manually or via two orders in Binance Futures API.")
            
            order_params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity,
            }
            if order_type == "LIMIT":
                order_params["price"] = str(price)
                order_params["timeInForce"] = TIME_IN_FORCE_GTC
            elif order_type == "STOP_MARKET":
                order_params["stopPrice"] = str(stop_price)
                order_params["closePosition"] = False
                order_params["priceProtect"] = False
            
            elif order_type == "STOP_LIMIT":
                order_params["stopPrice"] = str(stop_price)
                order_params["price"] = str(price_limit)
                order_params["timeInForce"] = TIME_IN_FORCE_GTC
                order_params["closePosition"] = False
                order_params["priceProtect"] = False
            
            order = self.client.futures_create_order(**order_params)
            self.logger.info(f"Order placed: {order}")
            print(f"Order successful: {order}")
        except NotImplementedError as nie:
            self.logger.error(str(nie))
            print(f"Order failed: {nie}")
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")
            print(f"Order failed: {e}")

    def cancel_all_orders(self, symbol):
        try:
            response = self.client.futures_cancel_all_open_orders(symbol=symbol)
            print(f"All open orders for {symbol} have been cancelled.")
            self.logger.info(f"Cancelled all orders for {symbol}: {response}")
        except Exception as e:
            print(f"Failed to cancel orders: {e}")
            self.logger.error(f"Cancel error: {e}")

    def get_current_price(self, symbol):
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            self.logger.error(f"Error fetching price: {e}")
            return None