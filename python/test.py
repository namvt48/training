import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
import websockets
import json
import logging

logging.basicConfig(
    filename='token_prices.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

tokens = [
    "ethusdt",  # Ethereum
    "btcusdt",  # Bitcoin
    "adausdt",  # Cardano
    "bnbusdt"   # Binance Coin
]

async def fetch_token_price(symbol):
    url = f"wss://stream.binance.com:9443/ws/{symbol}@ticker"
    async with websockets.connect(url) as websocket:
        try:
            response = await websocket.recv()
            data = json.loads(response)
            price = data['c']  # Lấy giá close
            logging.info(f"Giá {symbol.upper()} (Binance): {price} USD")
        except websockets.exceptions.ConnectionClosed as e:
            logging.error(f"WebSocket đóng: {symbol.upper()} - {e}")
        except Exception as e:
            logging.error(f"Lỗi khi xử lý {symbol.upper()}: {e}")

async def async_fetch_prices():
    tasks = [fetch_token_price(token) for token in tokens]
    await asyncio.gather(*tasks)

def get_prices():
    try:
        asyncio.run(async_fetch_prices())
    except Exception as e:
        logging.error(f"Lỗi khi chạy get_prices: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=get_prices,
        trigger=IntervalTrigger(seconds=5),  # Tần suất thực hiện
        id='check_token_prices',
        name='Check prices for multiple tokens',
        replace_existing=True
    )
    scheduler.start()
    logging.info("Scheduler started...")

if __name__ == "__main__":
    start_scheduler()
    try:
        # Giữ cho script chạy liên tục
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")