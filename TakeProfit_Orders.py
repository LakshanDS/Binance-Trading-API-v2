import asyncio
from binance.client import Client
from StopLoss_Order import Place_stop_loss

async def Place_Take_Profits(client, symbol, take_profit_price, Take_Profit_side):
    try:
        take_profit_order = client.futures_create_order(
            symbol=symbol,
            side=Take_Profit_side,
            type='TAKE_PROFIT_MARKET',
            stopPrice=take_profit_price,
            closePosition=True,
            timeInForce='GTE_GTC')

        return {"success": True, "Take_Profit_2": take_profit_order}
        
    except Exception as e:

        return {"success": False, "error": str(e)}
        print(f"Error for {symbol}: {e}")

async def Regular_Take_Profit(client, symbol, take_profit_price, quantity, Take_Profit_side):

    try:
        take_profit_order = client.futures_create_order(
            symbol=symbol,
            side=Take_Profit_side,
            type='TAKE_PROFIT_MARKET',
            stopPrice=take_profit_price,
            quantity=quantity,
            timeInForce='GTE_GTC',
            reduceOnly=True)

        return {"success": True, "Take_Profit_1": take_profit_order}

    except Exception as e:

        return {"success": False, "error": str(e)}
        print(f"Error for {symbol}: {e}")