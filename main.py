import MetaTrader5 as mt5
import requests
import json
import time
import sys
import os
from datetime import datetime
import pandas as pd
from TheSSS.src.services.mt5_service import MT5Client
from TheSSS.src.services.rl_trader import RLTrader

# Initialize MT5 client with config
# Convert account number to integer for MT5 login
mt5_client = MT5Client('config/mt5_config.json')
if not mt5_client.connect():
    exit("Failed to connect to MT5")

# Mac configuration
MAC_IP = "192.168.1.100"  # UPDATE WITH YOUR MAC'S IP
MAC_PORT = "5000"
API_ENDPOINT = f"http://{MAC_IP}:{MAC_PORT}/api/mt5-data"

def send_to_mac(data):
    """Send formatted data to Mac running TheSSS"""
    try:
        response = requests.post(
            API_ENDPOINT,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending data to Mac: {e}")
        return False

def get_account_info():
    account_info = mt5_client.get_account_info()
    if account_info:
        print("Account Info:", account_info)
    else:
        print("No account info available.")

def place_market_order(symbol, volume, order_type, deviation=20):
    """
    Place a market order on the live account.
    (Uncomment the call in main() only if you're sure to trade live!)
    """
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        print(f"Failed to get {symbol} price")
        return None
    
    price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    if result is None:
        print("order_send() failed, error code:", mt5.last_error())
        return None
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order failed, retcode:", result.retcode)
        return None
    
    return result

class PaperTrading:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance
        self.positions = []

    def execute_trade(self, symbol, volume, order_type, price):
        """Simulate trade execution"""
        trade_type_str = "BUY" if order_type == mt5.ORDER_TYPE_BUY else "SELL"
        trade = {
            'symbol': symbol,
            'volume': volume,
            'type': trade_type_str,
            'price': price,
            'time': datetime.now()
        }
        self.positions.append(trade)
        print(f"Simulated trade: {trade}")

        # Update balance (simplified update: no commissions or slippage)
        if order_type == mt5.ORDER_TYPE_BUY:
            self.balance -= volume * price
        else:
            self.balance += volume * price

    def get_balance(self):
        return self.balance

    def get_positions(self):
        return self.positions

def run_diagnostics():
    """MT5 connection diagnostic similar to check_mt5_import.py"""
    print("MetaTrader 5 Connection Diagnostic Tool")
    print("======================================")
    print(f"Timestamp: {datetime.now()}")
    print(f"Timestamp: {datetime.now()}")
    print(f"Timestamp: {datetime.now()}")

    print("\nPython Environment:")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Working Directory: {os.getcwd()}")
    
    print("\nMetaTrader5 Package:")
    print(f"MT5 Version: {mt5.__version__}")
    print(f"MT5 Package Path: {mt5.__file__}")
    
    print("\nTesting MT5 Terminal Connection:")
    if not mt5.initialize():
        print(f"MT5 initialization failed. Error code: {mt5.last_error()}")
        return False
    terminal_info = mt5.terminal_info()
    if terminal_info is None:
        print(f"Failed to get terminal info. Error code: {mt5.last_error()}")
        return False
    print("\nTerminal Information:")
    print(f"Connected: {terminal_info.connected}")
    print(f"Trade Allowed: {terminal_info.trade_allowed}")
    print(f"Terminal Build: {terminal_info.build}")
    print(f"Terminal Path: {terminal_info.path}")
    mt5.shutdown()
    return True

def main():
    # Continuous data collection and transmission
    while True:
        try:
            # Get market data for configured symbols
            data = {
                "timestamp": datetime.now().isoformat(),
                "account": mt5_client.get_account_info(),
                "symbols": {}
            }
            
            # Get data for each symbol
            for symbol in mt5_client.config["symbols"]:
                df = mt5_client.get_data(
                    symbol=symbol,
                    timeframe=mt5_client.config["timeframe"],
                    n=mt5_client.config["data_window"]
                )
                data["symbols"][symbol] = json.loads(df.to_json(orient="records"))
            
            # Send to Mac
            if send_to_mac(data):
                print(f"Data sent successfully at {datetime.now()}")
            else:
                print(f"Failed to send data at {datetime.now()}")
            
        except KeyboardInterrupt:
            print("Stopping data collection...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying
        finally:
            time.sleep(300)  # Wait for 5 minutes

if __name__ == "__main__":
    main()
