import asyncio
from binance.client import Client

async def close_all_positions(client, symbol):
    try:
        # Cancel all open orders first
        try:
            client.futures_cancel_all_open_orders(symbol=symbol)
            print(f"Cancelled all open orders for {symbol}")
        except Exception as e:
            print(f"Error cancelling orders for {symbol}: {e}")
            return {"success": False, "error": str(e), "message": f"Error cancelling open orders for {symbol}: {e}"}

        # Get all open positions for the symbol
        position_info = client.futures_position_information(symbol=symbol)
        position = next((pos for pos in position_info if float(pos['positionAmt']) != 0), None)
        if not position:
            print(f"No open positions for {symbol}")
            return {"success": True, "message": f"No open positions for {symbol}", "position_closed": False}

        # Get the amount of the open position
        position_amt = float(position['positionAmt'])

        if position_amt > 0:
            side = 'SELL'  # Close long position
        elif position_amt < 0:
            side = 'BUY'  # Close short position

        close_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=abs(position_amt),  # Close the exact amount
            reduceOnly=True
        )
        
        print(f"Closed position for {symbol}")
        return {"success": True, "message": f"Closed all position and open orders for {symbol}", "order": close_order}

    except Exception as e:
        print(f"Error closing positions for {symbol}: {e}")
        return {"success": False, "error": str(e), "message": f"Error closing positions for {symbol}: {e}"}