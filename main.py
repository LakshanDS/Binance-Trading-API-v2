import os
import uvicorn
import asyncio
from dotenv import load_dotenv
from binance.client import Client
from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from Limit_Order import Place_Limit_Order, limit_order_status
from Market_Order import Place_Market_Order

load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Check if API keys are loaded
if not api_key or not api_secret: # Added check
    raise ValueError("Binance API key and secret must be set in the .env file") # Added check

class LimitOrderRequest(BaseModel):
    symbol: str
    quantity: float
    entry_price: float
    take_profit_1: float
    take_profit_2: float
    stop_loss: float
    leverage: int = 20

class MarketOrderRequest(BaseModel):
    symbol: str
    quantity: float
    take_profit_1: float
    take_profit_2: float
    stop_loss: float
    leverage: int = 20

app = FastAPI()
client = Client(api_key, api_secret, testnet=True) # This line remains the same, but uses the loaded variables

# # Allowed IP
# ALLOWED_IP = ["140.245.231.81"]

# # Middleware to restrict access by IP
# @app.middleware("http")
# async def ip_filtering(request: Request, call_next):
#     client_ip = request.client.host
#     if client_ip not in ALLOWED_IP:
#         print(f"Unauthorized access attempt from IP: {client_ip}")
#         return JSONResponse(status_code=403, content={"detail": "Access forbidden"})
#     return await call_next(request)

@app.post("/place_limit_order/", status_code=202)
async def place_order(order: LimitOrderRequest, background_tasks: BackgroundTasks):
    try:
        Side = "BUY" if order.take_profit_2 > order.stop_loss else "SELL"
        initial_result = await Place_Limit_Order(
            client,
            order.symbol,
            order.quantity,
            order.entry_price,
            order.leverage,
            Side)

        if not initial_result["success"]:
            return JSONResponse(status_code=400,
                                content={"success": False,
                                        "error": initial_result.get("error", "Unknown error"),
                                        "message": f"Failed to place limit order for {order.symbol}"})

        background_tasks.add_task(limit_order_status,
                            client,
                            order.symbol,
                            order.quantity,
                            order.entry_price,
                            order.take_profit_1,
                            order.take_profit_2,
                            order.stop_loss,
                            initial_result["order_id"])

        # Return success response with 202 status
        return {"success": True,
                "message": initial_result["message"],
                "order_id": initial_result["order_id"]}

    except Exception as e:
        return JSONResponse(status_code=400,
                            content={"success": False,
                                    "error": str(e),
                                    "message": f"Failed to place limit order for {order.symbol}"})

@app.post("/place_market_order/", status_code=200)
async def place_market_order(order: MarketOrderRequest):
    try:
        result = await Place_Market_Order(
                    client,
                    order.symbol,
                    order.quantity,
                    order.stop_loss,
                    order.take_profit_1,
                    order.take_profit_2,
                    order.leverage)

        if result.get("success", False):
            return {"success": True,
                    "message": result.get("message", f"Market order placed for {order.symbol}"),
                    "details": result}
        else:
            return JSONResponse(status_code=400,
                                content={"success": False,
                                        "error": result.get("error", "Unknown error"),
                                        "message": result.get("message", f"Failed to place market order for {order.symbol}")})

    except Exception as e:
        return JSONResponse(status_code=400,
                            content={"success": False,
                                    "error": str(e),
                                    "message": f"Failed to place market order for {order.symbol}"})

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=4444,
        reload=True)

# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=4444,
#         ssl_certfile="/root/cert/vpnlak.duckdns.org/fullchain.pem",
#         ssl_keyfile="/root/cert/vpnlak.duckdns.org/privkey.pem")