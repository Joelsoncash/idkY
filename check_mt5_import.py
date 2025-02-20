import sys
import os
import time
from datetime import datetime

try:
    import MetaTrader5 as mt5
except ImportError as e:
    print(f"Critical Import Error: {str(e)}")
    print("Make sure you're using the Python environment with MetaTrader5 installed")
    print(f"Detected venv path: {sys.prefix}")
    sys.exit(1)

def check_python_environment():
    """Check Python environment details"""
    print("\nPython Environment:", flush=True)
    print(f"Python Version: {sys.version}", flush=True)
    print(f"Python Path: {sys.executable}", flush=True)
    print(f"Working Directory: {os.getcwd()}", flush=True)
    print(f"Virtual Environment: {sys.prefix}", flush=True)

def check_mt5_installation():
    """Check MetaTrader5 package installation"""
    print("\nMetaTrader5 Package:")
    print(f"MT5 Version: {mt5.__version__}")
    print(f"MT5 Package Path: {mt5.__file__}")

def check_mt5_connection():
    """Test connection to MetaTrader 5 terminal"""
    print("\nMetaTrader5 Connection Test:")
    
    # Initialize MT5 connection
    if not mt5.initialize():
        print(f"MT5 initialization failed. Error code: {mt5.last_error()}")
        return False
    
    # Get terminal info
    terminal_info = mt5.terminal_info()
    if terminal_info is None:
        print(f"Failed to get terminal info. Error code: {mt5.last_error()}")
        return False
    
    print("\nTerminal Information:")
    print(f"Connected: {terminal_info.connected}")
    print(f"Trade Allowed: {terminal_info.trade_allowed}")
    print(f"Terminal Build: {terminal_info.build}")
    print(f"Terminal Path: {terminal_info.path}")
    
    return True

def check_config_credentials():
    """Check if MT5 config file exists and has credentials"""
    config_path = os.path.join('config', 'mt5_config.json')
    if not os.path.exists(config_path):
        print(f"\nMissing config file: {config_path}", flush=True)
        return False
    return True

def main():
    print("MetaTrader 5 Connection Diagnostic Tool", flush=True)
    print("======================================", flush=True)
    print(f"Timestamp: {datetime.now()}\n", flush=True)
    
    if not check_config_credentials():
        return
    
    try:
        check_python_environment()
        check_mt5_installation()
        connected = check_mt5_connection()
        
        if connected:
            print("\nBasic connection test successful!")
            print("Note: You still need to log in to your trading account to perform trading operations.")
        else:
            print("\nConnection test failed. Please check:")
            print("1. MetaTrader 5 terminal is running")
            print("2. You have a stable internet connection")
            print("3. Your MT5 terminal is properly installed")
    except Exception as e:
        print(f"\nError during diagnostic: {str(e)}")
    finally:
        if mt5.initialize():
            mt5.shutdown()

if __name__ == "__main__":
    main()
