import asyncio
from binance.client import Client
from Close_All_Orders import close_all_positions
from StopLoss_Order import Place_stop_loss
from TrailingStop import Place_Trailing_Stop
from Webhook import send_webhook
from TakeProfit_Orders import Place_Take_Profits

async def Place_Market_Order(client, symbol, quantity, stop_loss, take_profit_1, take_profit_2, leverage):

    try:
        await close_all_positions(client, symbol)
        client.futures_change_leverage(symbol=symbol, leverage=leverage)

        market_order_side = "BUY" if take_profit_2 > stop_loss else "SELL"
        stop_loss_side = "SELL" if market_order_side == "BUY" else "BUY"

        market_order = client.futures_create_order(
            symbol=symbol,
            side=market_order_side,
            type='MARKET',
            quantity=quantity) # Place a market order
        
        positions = client.futures_position_information(symbol=symbol)
        filled_price = next((position['entryPrice'] for position in positions if float(position['positionAmt']) != 0), 'N/A')
        message = f"MARKET ORDER FILLED! {symbol} At {filled_price}!"
        send_webhook(message)

        TP1_Quantity = lambda quantity: round((quantity/2) / 10**math.floor(math.log10(quantity/2))) * 10**math.floor(math.log10(quantity/2)) if quantity > 1 else quantity/2
        TP2_result = await Place_Take_Profits(client, symbol, str(take_profit_2), stop_loss_side)
        SLTP_result = await Place_Trailing_Stop(client, symbol, filled_price, str(take_profit_1), str(stop_loss), quantity, stop_loss_side)

        if not TP2_result.get("success", False):
            error = f"An error placing Take Profit 2 order, All positions closed for {symbol}"
            send_webhook(error)
            await close_all_positions(client, symbol)
            return {"success": False, "message": error}

        if not SLTP_result.get("success", False):
            error = f"An error placing Stop-loss order, All positions closed for {symbol}"
            send_webhook(error)
            await close_all_positions(client, symbol)
            return {"success": False, "message": error}

        else :
            success_message = f"Stop Loss and Take Profit placed Successfully for {symbol} at stop at {stop_loss} and TP1 at {take_profit_1} and TP2 at {take_profit_2}!"
            send_webhook(success_message)
            print(success_message)
            return {"success": True, "message": success_message, "market_order": market_order}

    except Exception as e:
        error_message = f"Error placing market order for {symbol} : {e}"
        print(error_message)
        return {"success": False, "error": str(e), "message": error_message}