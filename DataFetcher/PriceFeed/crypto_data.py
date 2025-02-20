import requests
from datetime import datetime
from threading import Thread, Lock
from queue import Queue
from database_manager import DatabaseManager
from dotenv import load_dotenv
import os

# load .env file
load_dotenv()
FIAT_API_URL = os.getenv('FIAT_API_URL', '')
CRYPTO_API_URL = os.getenv('CRYPTO_API_URL', '')


class CurrencyDataWorker(Thread):
    def __init__(self, api_url, currency_type, queue):
        super().__init__()
        self.api_url = api_url
        self.currency_type = currency_type
        self.queue = queue

    def run(self):
        try:
            headers = {
                "accept": "application/json",
            }
            response = requests.get(self.api_url, headers=headers)
            data = response.json()

            if response.status_code == 200:
                rates = {}
                if self.currency_type == "fiat":
                    rates = data.get("rates", {})
                elif self.currency_type == "crypto":
                    crypto_symbol_list = data.get("data", [])
                    if not crypto_symbol_list:
                        print("No crypto data found")
                    else:
                        for crypto_symbol in crypto_symbol_list:
                            symbol = crypto_symbol.get("symbol")
                            if "USDT" in symbol:
                                symbol = symbol.replace("USDT", "")
                                price = float(crypto_symbol.get("lastPr"))
                                rates[symbol] = 1 / price if price != 0 else 0
                else:
                    print("Invalid currency type")
                self.queue.put((rates, datetime.now(), self.currency_type))
        except Exception as e:
            print(f"Error fetching {self.currency_type} data: {str(e)}")


class CurrencyData:
    def __init__(self):
        self.lock = Lock()
        self.fiat_rates = {}
        self.crypto_rates = {}
        self.last_update = None
        self.queue = Queue()

        # Initialize database manager
        self.db_manager = DatabaseManager()

        # Load latest data from database
        self.fiat_rates = self.db_manager.get_latest_rates('fiat')
        self.crypto_rates = self.db_manager.get_latest_rates('crypto')

        # Initialize two workers to fetch fiat and crypto data
        self.fiat_worker = CurrencyDataWorker(FIAT_API_URL, "fiat", self.queue)
        self.crypto_worker = CurrencyDataWorker(CRYPTO_API_URL, "crypto", self.queue)

        self.update_rates()

    def update_rates(self):
        """Start asynchronous rate fetching"""
        self.fiat_worker.start()
        self.crypto_worker.start()
        self.fiat_worker.join()
        self.crypto_worker.join()
        while not self.queue.empty():
            rates, timestamp, currency_type = self.queue.get()
            self.handle_rates_update(rates, timestamp, currency_type)

    def handle_rates_update(self, rates, timestamp, currency_type):
        """Handle rate updates"""
        with self.lock:
            if currency_type == "fiat":
                self.fiat_rates = rates
            elif currency_type == "crypto":
                self.crypto_rates = rates
            self.last_update = timestamp

            # Save to database
            self.db_manager.save_rates(rates, currency_type)

    def get_currencies(self):
        """Get all supported currency codes"""
        with self.lock:
            return list(self.fiat_rates.keys()) + list(self.crypto_rates.keys())

    def get_rate(self, currency):
        """Get the rate of a specified currency"""
        with self.lock:
            if currency in self.fiat_rates:
                return self.fiat_rates.get(currency)
            return self.crypto_rates.get(currency)

    def get_last_update(self):
        """Get the last update time"""
        with self.lock:
            return self.last_update.strftime("%Y-%m-%d %H:%M:%S") if self.last_update else "Never"


if __name__ == "__main__":
    currency_data = CurrencyData()