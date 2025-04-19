import asyncio
from binance.client import Client

async def Place_stop_loss(client, symbol, stop_loss_price, stop_loss_side):
    try:
        stop_loss_order = client.futures_create_order(
            symbol=symbol,
            side=stop_loss_side,
            type='STOP_MARKET',
            stopPrice=stop_loss_price,
            closePosition=True,
            timeInForce='GTE_GTC')

        return {"success": True, "Stop_Order": stop_loss_order}

    except Exception as e:

        return {"success": False, "error": str(e)}
        print(f"Error for {symbol}: {e}")