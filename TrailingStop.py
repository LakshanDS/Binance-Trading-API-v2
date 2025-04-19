import math
import asyncio
from TakeProfit_Orders import Regular_Take_Profit
from StopLoss_Order import Place_stop_loss
from Close_All_Orders import close_all_positions
from Webhook import send_webhook

async def Place_Trailing_Stop(client, symbol, entry_price, take_profit_1, stop_loss_price, quantity, side):

    # Place initial Stop Loss order
    SL_result = await Place_stop_loss(client, symbol, stop_loss_price, side)
    if not SL_result.get("success", False):
        print(f"SL_result: {SL_result}")
        await close_all_positions(client, symbol)
        return {"success": False, "error": f"Failed to place initial Stop Loss order: {sl_result['error']}"}

    TP1_Quantity = lambda quantity: round((quantity/2) / 10**math.floor(math.log10(quantity/2))) * 10**math.floor(math.log10(quantity/2)) if quantity > 1 else quantity/2
    TP1_result = await Regular_Take_Profit(client, symbol, take_profit_1, TP1_Quantity(quantity), side)

    if not TP1_result.get("success", False):
        print(f"TP1_result: {TP1_result}")
        await close_all_positions(client, symbol)
        return {"success": False, "error": f"Failed to place initial Take Profit order: {TP1_result['error']}"}

    initial_tp_order = TP1_result["Take_Profit_1"]
    initial_sl_order = SL_result["Stop_Order"]

    asyncio.create_task(_trailing_stop_loop(client, symbol, entry_price, initial_tp_order, initial_sl_order, side))
    print("Trailing Stop activated")
    return {"success": True, "message": "Trailing Stop activated", "status": 202}

async def _trailing_stop_loop(client, symbol, entry_price, initial_tp_order, initial_sl_order, side):
    while True:
        await asyncio.sleep(10)  # Check order status every 60 seconds

        try:
            tp_order_status = client.futures_get_order(symbol=symbol, orderId=initial_tp_order['orderId'])

            if tp_order_status['status'] == 'FILLED':
                massage = "Take Profit order filled! Modifying Stop Loss to entry price."
                print(massage)
                send_webhook(massage)
                # Cancel existing Stop Loss order
                cancel_sl = client.futures_cancel_order(symbol=symbol, orderId=initial_sl_order['orderId'])
                print(f"Stop Loss order cancelled!")

                # Place new Stop Loss order at entry price
                new_sl_result = await Place_stop_loss(client, symbol, entry_price, side)
                if not new_sl_result.get("success", False):
                    await close_all_positions(client, symbol)
                    massage = {"success": False, "error": f"Failed to place new Stop Loss order at entry: {new_sl_result['error']}"}
                    print(massage)
                    return {massage}

                massage = f"New Stop Loss order placed at entry: {entry_price}"
                print(massage)
                send_webhook(massage)
                return {"success": True, "message": "Trailing Stop activated, Stop Loss moved to entry price."}

            elif tp_order_status['status'] != 'NEW' and tp_order_status['status'] != 'FILLED':
                massage = f"Take Profit order status is {tp_order_status['status']}. Exiting Trailing Stop loop."
                print(massage)
                send_webhook(massage)
                return {"success": False, "message": f"Take Profit order closed with status: {tp_order_status['status']}. Trailing Stop stopped."}

        except Exception as e:
            print(f"Error checking order status: {e}")
            return {"success": False, "error": str(e)}