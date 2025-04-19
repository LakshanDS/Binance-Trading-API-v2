# Binance Trading Bot API v2

## Description

This project is a Python-based API built using FastAPI to interact with the Binance Futures market. It provides functionalities to automate trading strategies by placing various types of orders, including:

*   **Limit Orders:** Place orders at a specific entry price.
*   **Market Orders:** Execute orders immediately at the current market price.
*   **Take Profit Orders:** Set multiple take profit levels (TP1 and TP2) to secure profits.
*   **Stop Loss Orders:** Implement stop loss mechanisms to limit potential losses, including trailing stop functionality.
*   **Webhook Integration:** Sends real-time updates to a specified webhook URL (e.g., Telegram) for order status and execution notifications.

This API is designed to be a v2 iteration, improving upon previous versions with enhanced features and a more robust structure for automated Binance Futures trading.

## Use Cases

*   **Algorithmic Trading:** Automate your Binance Futures trading strategies based on predefined conditions and signals.
*   **Trading Platform Integration:** Integrate this API with custom trading dashboards or platforms for streamlined order management.
*   **Educational Purposes:** Learn about Binance API functionalities and building automated trading systems.
*   **Risk Management:** Implement automated risk management strategies using stop loss and take profit features.

## How to Use

### Prerequisites

*   **Python 3.8+**
*   **Binance Account:** You need a Binance account to use this API.
*   **Binance API Keys:** Generate API keys from your Binance account settings (ensure Futures trading is enabled for the API keys).
*   **Dependencies:** Install the required Python packages listed in `requirements.txt`.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [repository_url] # Replace with your repository URL if applicable
    cd Binance # Or the cloned directory name
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate # On Linux/macOS
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r LakshanDS/requirements.txt
    ```

### Configuration

1.  **Set API Keys:**
    *   Create a `.env` file in the `LakshanDS/` directory.
    *   Add your Binance API key and secret to the `.env` file:

        ```
        BINANCE_API_KEY=YOUR_BINANCE_API_KEY
        BINANCE_API_SECRET=YOUR_BINANCE_API_SECRET
        ```
        **Replace `YOUR_BINANCE_API_KEY` and `YOUR_BINANCE_API_SECRET` with your actual Binance API credentials.**

2.  **Webhook URL (Optional):**
    *   In `LakshanDS/Webhook.py`, replace `"https://n8nlak.duckdns.org/webhook/89614ede-feda-4ec0-aa18-dd9f7632f2cd"` with your desired webhook URL to receive trading notifications.

### Running the API

Run the `main.py` file using uvicorn:

```bash
uvicorn LakshanDS.main:app --reload --host 127.0.0.1 --port 4444
```

The API will be accessible at `http://127.0.0.1:4444`.

### API Endpoints

#### 1. Place Limit Order

*   **Endpoint:** `/place_limit_order/`
*   **Method:** `POST`
*   **Request Body (JSON):**

    ```json
    {
        "symbol": "BTCUSDT",
        "quantity": 0.001,
        "entry_price": 30000,
        "take_profit_1": 31000,
        "take_profit_2": 32000,
        "stop_loss": 29000,
        "leverage": 20
    }
    ```

*   **Parameters:**
    *   `symbol` (str): Trading pair symbol (e.g., "BTCUSDT").
    *   `quantity` (float): Order quantity.
    *   `entry_price` (float): Limit order entry price.
    *   `take_profit_1` (float): First take profit price level.
    *   `take_profit_2` (float): Second take profit price level.
    *   `stop_loss` (float): Stop loss price.
    *   `leverage` (int, optional): Leverage for the trade (default: 20).

#### 2. Place Market Order

*   **Endpoint:** `/place_market_order/`
*   **Method:** `POST`
*   **Request Body (JSON):**

    ```json
    {
        "symbol": "ETHUSDT",
        "quantity": 0.01,
        "take_profit_1": 1800,
        "take_profit_2": 1900,
        "stop_loss": 1600,
        "leverage": 20
    }
    ```

*   **Parameters:**
    *   `symbol` (str): Trading pair symbol (e.g., "ETHUSDT").
    *   `quantity` (float): Order quantity.
    *   `take_profit_1` (float): First take profit price level.
    *   `take_profit_2` (float): Second take profit price level.
    *   `stop_loss` (float): Stop loss price.
    *   `leverage` (int, optional): Leverage for the trade (default: 20).

## Modules and Features

*   **`main.py`:**  The main FastAPI application that defines API endpoints and handles incoming requests. It uses other modules to place and manage orders.
*   **`Limit_Order.py`:** Implements functions for placing limit orders and monitoring their status until filled. Upon filling, it places take profit and stop loss orders.
*   **`Market_Order.py`:** Implements functions for placing market orders with predefined take profit and stop loss levels.
*   **`TrailingStop.py`:** Contains logic for placing and managing trailing stop orders, automatically adjusting stop loss levels as the price moves in a favorable direction.
*   **`StopLoss_Order.py`:**  Provides functions specifically for placing stop loss orders to manage risk.
*   **`TakeProfit_Orders.py`:** Includes functions for placing both regular take profit orders and take profit orders for closing the entire position.
*   **`Close_All_Orders.py`:** Offers functionality to close all open positions and cancel all pending orders for a given trading symbol. Useful for risk management and strategy adjustments.
*   **`Webhook.py`:**  Handles sending webhook messages to external services (like Telegram) to provide real-time notifications about order placements, fills, and status updates.
*   **`requirements.txt`:** Lists all Python package dependencies required to run the API.
*   **`.env`:**  Stores sensitive configuration information such as API keys, keeping them separate from the codebase.

## Disclaimer

Trading cryptocurrencies on Binance Futures involves significant risks. This API is provided as-is, for educational and automation purposes. Use it responsibly and at your own risk. The developers are not responsible for any financial losses incurred while using this API. Always conduct thorough testing and risk assessment before deploying automated trading strategies in live markets.