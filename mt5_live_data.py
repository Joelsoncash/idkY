import time
import MetaTrader5 as mt5
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)  # Initialize colorama

def display_live_data(symbol="EURUSD"):
    if not mt5.initialize():
        print(Fore.RED + "Failed to initialize MT5 connection")
        return

    try:
        print(Fore.CYAN + "\nLive Market Data Stream - CTRL+C to exit\n")
        while True:
            tick = mt5.symbol_info_tick(symbol)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if tick is None:
                print(Fore.RED + f"[{current_time}] Error fetching data")
                continue
                
            print(Fore.YELLOW + f"[{current_time}] {symbol}")
            print(Fore.GREEN + f"Bid: {tick.bid:.5f} | Ask: {tick.ask:.5f}")
            print(Fore.BLUE + f"Spread: {(tick.ask - tick.bid):.5f}")
            print(Fore.MAGENTA + f"Volume: {tick.volume}")
            print("-" * 40)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(Fore.CYAN + "\n\nStopping live data feed...")
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    display_live_data()
