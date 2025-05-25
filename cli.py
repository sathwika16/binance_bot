import argparse
from bot import BasicBot
import config

def main():
    parser = argparse.ArgumentParser(description="Simplified Binance Futures Trading Bot")

    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--quantity", type=float, help="Order quantity")
    parser.add_argument("--order_type", choices=["MARKET", "LIMIT", "STOP_MARKET", "STOP_LIMIT", "OCO"], default="MARKET", help="Type of order")
    parser.add_argument("--price", type=float, help="Price (required for LIMIT and STOP_LIMIT orders)")
    parser.add_argument("--stop_price", type=float, help="Stop price (required for STOP_MARKET, STOP_LIMIT, and OCO orders)")
    parser.add_argument("--price_limit", type=float, help="Stop limit price (required for STOP_LIMIT and OCO orders)")
    parser.add_argument("--cancel", action="store_true", help="Cancel all open orders for the symbol")

    args = parser.parse_args()

    bot = BasicBot(config.API_KEY, config.API_SECRET)

    # Validate input combinations
    if args.cancel:
        bot.cancel_all_orders(symbol=args.symbol)
        return

    if args.order_type in ["LIMIT", "STOP_LIMIT"] and not args.price:
        parser.error("Price must be provided for LIMIT and STOP_LIMIT orders.")

    if args.order_type in ["STOP_MARKET", "STOP_LIMIT", "OCO"] and not args.stop_price:
        parser.error("Stop price must be provided for STOP_MARKET, STOP_LIMIT, and OCO orders.")

    if args.order_type == "OCO" and not args.price_limit:
        parser.error("Price limit must be provided for OCO orders.")

    if not args.side or not args.quantity:
        parser.error("Both --side and --quantity are required for placing an order.")

    # Fetch current price to validate price ranges
    current_price = bot.get_current_price(args.symbol)
    if current_price is None:
        print("Could not fetch current price, aborting.")
        return

    print(f"Current price for {args.symbol} is {current_price}")

    # Validate price logic based on side and order type
    side = args.side.upper()

    if args.order_type == "LIMIT":
        if side == "SELL" and args.price <= current_price:
            parser.error(f"For SELL LIMIT order, price must be greater than current price ({current_price})")
        if side == "BUY" and args.price >= current_price:
            parser.error(f"For BUY LIMIT order, price must be less than current price ({current_price})")

    if args.order_type in ["STOP_MARKET", "STOP_LIMIT"]:
        if side == "SELL" and args.stop_price >= current_price:
            parser.error(f"For SELL stop orders, stop_price must be less than current price ({current_price})")
        if side == "BUY" and args.stop_price <= current_price:
            parser.error(f"For BUY stop orders, stop_price must be greater than current price ({current_price})")

    if args.order_type == "OCO":
        # Validate OCO prices:
        # SELL: price (take profit) > current_price, stop_price < current_price, price_limit < stop_price
        if side == "SELL":
            if args.price <= current_price:
                parser.error(f"For SELL OCO, take profit price (--price) must be greater than current price ({current_price})")
            if args.stop_price >= current_price:
                parser.error(f"For SELL OCO, stop price (--stop_price) must be less than current price ({current_price})")
            if args.price_limit >= args.stop_price:
                parser.error(f"For SELL OCO, stop limit price (--price_limit) must be less than stop price ({args.stop_price})")
        # BUY: price (take profit) < current_price, stop_price > current_price, price_limit > stop_price
        elif side == "BUY":
            if args.price >= current_price:
                parser.error(f"For BUY OCO, take profit price (--price) must be less than current price ({current_price})")
            if args.stop_price <= current_price:
                parser.error(f"For BUY OCO, stop price (--stop_price) must be greater than current price ({current_price})")
            if args.price_limit <= args.stop_price:
                parser.error(f"For BUY OCO, stop limit price (--price_limit) must be greater than stop price ({args.stop_price})")
        else:
            parser.error("Invalid side for OCO order")

    # Place order logic

    if args.order_type == "OCO":
        # Binance Futures does not support OCO natively via API.
        # We implement manual OCO by placing two orders:
        # 1. LIMIT order for take profit
        # 2. STOP_MARKET order for stop loss

        print("Placing manual OCO orders (LIMIT + STOP_MARKET)")

        # Place take profit limit order
        bot.place_order(
            symbol=args.symbol,
            side="SELL" if side == "BUY" else "BUY",  # opposite side for take profit
            quantity=args.quantity,
            order_type="LIMIT",
            price=args.price
        )

        # Place stop loss stop market order
        bot.place_order(
            symbol=args.symbol,
            side=side,
            quantity=args.quantity,
            order_type="STOP_MARKET",
            stop_price=args.stop_price
        )

    else:
        # Normal order placement for other types
        bot.place_order(
            symbol=args.symbol,
            side=side,
            quantity=args.quantity,
            order_type=args.order_type,
            price=args.price,
            stop_price=args.stop_price,
            price_limit=args.price_limit
        )

if __name__ == "__main__":
    main()