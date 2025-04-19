import math
import asyncio
from binance.client import Client
from Close_All_Orders import close_all_positions
from TakeProfit_Orders import Place_Take_Profits
from Webhook import send_webhook
from TrailingStop import Place_Trailing_Stop

async def Place_Limit_Order(client, symbol, quantity, entry_price, leverage, side):

    try:
        await close_all_positions(client, symbol)
        client.futures_change_leverage(symbol=symbol, leverage=leverage)

        limit_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            quantity=quantity,
            price=str(entry_price),
            timeInForce='GTC'
        )
        
        order_id = limit_order['orderId']
        message = f"{side} Limit order placed for {symbol} at {entry_price}. Waiting for the order to fill..."
        send_webhook(message)
        print(message)
        
        return {"success": True, "message": message, "order_id": order_id, "complete": False}
    except Exception as e:
        error_message = f"An error occurred while placing order for {symbol}: {e}"
        print(error_message)
        return {"success": False, "error": str(e), "complete": True}

# Separate function for monitoring the fill
async def limit_order_status(client, symbol, quantity, entry_price, take_profit_1, take_profit_2, stop_loss, order_id):
    try:
        for _ in range(720):  # 2 hours monitoring(720)
            await asyncio.sleep(10)  # Wait 10 seconds
            try:
                order_status = client.futures_get_order(symbol=symbol, orderId=order_id)
                
                if order_status['status'] == 'FILLED':
                    fill_message = f"LIMIT ORDER FILLED! {symbol} at {entry_price}"
                    send_webhook(fill_message)
                    print(fill_message)

                    stop_loss_side = "SELL" if take_profit_1 > stop_loss else "BUY"
                    TP2_result = await Place_Take_Profits(client, symbol, str(take_profit_2), stop_loss_side)
                    SLTP1_result = await Place_Trailing_Stop(client, symbol, entry_price, str(take_profit_1), str(stop_loss), quantity, stop_loss_side)
                    if not SLTP1_result.get("success", False):
                        error_msg = f"Failed to place Stop Loss for {symbol}: {SLTP1_result.get('error', 'Unknown error')}. Closing position."
                        print(error_msg)
                        send_webhook(error_msg)
                        await close_all_positions(client, symbol)
                        return

                    # If both SL and TP placed successfully
                    success_message = f"Stop Loss and Take Profit placed for {symbol} at {stop_loss} and TP1 at {take_profit_1}, TP2 at {take_profit_2} Successfully"
                    print(success_message)
                    send_webhook(success_message)
                    return

                elif order_status['status'] == 'CANCELED':
                    error_message = f"Limit order for {symbol} at {entry_price} has been canceled by user or else"
                    send_webhook(error_message)
                    return
                    
            except Exception as e:
                await close_all_positions(client, symbol)
                message = f"Error monitoring order in 10 sec int. Closing all open orders and positions for {symbol}"
                print (f"{message} error : {str(e)}")
                send_webhook(message)
                return

        # Timeout - external function will handle cancellation
        await close_all_positions(client, symbol)
        message = f"Limit order for {symbol} has not been filled within 2 hours."
        error_message = {"success": False, "message": message}
        send_webhook(message)
        return

    except Exception as e:
        await close_all_positions(client, symbol)
        error_message = f"Error monitoring order 2h. Closing all open orders and positions for {symbol}"
        print (f"{error_message} error : {str(e)}")
        send_webhook(error_message)
        return