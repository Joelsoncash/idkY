import os
import subprocess
import sys
import platform

def check_mt5_terminal():
    terminal_path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
    
    print("MetaTrader5 Terminal Check")
    print("=" * 40)
    
    # Check file existence
    if not os.path.exists(terminal_path):
        print(f"Error: MetaTrader5 terminal not found at {terminal_path}")
        return False
    
    # System and file details
    print(f"Terminal Path: {terminal_path}")
    print(f"Operating System: {platform.platform()}")
    print(f"Python Version: {sys.version}")
    
    # File details
    file_stats = os.stat(terminal_path)
    print(f"File Size: {file_stats.st_size} bytes")
    print(f"Last Modified: {os.path.getmtime(terminal_path)}")
    
    # Attempt to run terminal (without blocking)
    try:
        print("\nAttempting to launch MetaTrader5 terminal...")
        subprocess.Popen([terminal_path])
        print("Terminal launch initiated successfully.")
    except Exception as e:
        print(f"Error launching terminal: {e}")
        return False
    
    return True

if __name__ == "__main__":
    result = check_mt5_terminal()
    sys.exit(0 if result else 1)
