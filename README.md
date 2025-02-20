# MetaTrader 5 Python Trading Example

This project demonstrates how to use the MetaTrader 5 (MT5) Python package to connect to MT5, retrieve account information, and place trades.

## Prerequisites

1. Install MetaTrader 5 platform
   - Download from the official website: https://www.metatrader5.com/en/download
   - Complete the installation
   - Set up a demo account through your broker

2. Install Python (if not already installed)
   - Download Python from: https://www.python.org/downloads/
   - During installation, make sure to check "Add Python to PATH"
   - Verify installation by opening a command prompt and typing: `python --version`

3. Install Required Packages
```bash
pip install -r requirements.txt
```

## Project Structure

- `main.py`: Main script demonstrating MT5 connection and trading functionality
- `requirements.txt`: List of required Python packages

## Features

The example script demonstrates:
- Connecting to MetaTrader 5
- Retrieving account information
- Placing a market order
- Error handling and proper shutdown

## Usage

1. Make sure MetaTrader 5 is running and you're logged into your account
2. Run the script:
```bash
python main.py
```

## Example Output

When run successfully, you should see output similar to:
```
Connected to MetaTrader 5

Account Information:
Login: [your account number]
Balance: [your balance]
Equity: [your equity]
Margin: [your margin]
Free Margin: [your free margin]
Currency: [your account currency]

Placing market buy order for EURUSD
Order placed successfully:
Order ID: [order number]
Execution Price: [execution price]
Execution Time: [execution timestamp]
```

## Troubleshooting

1. If you get "ModuleNotFoundError: No module named 'MetaTrader5'":
   - Verify Python is installed correctly
   - Run `pip install MetaTrader5` manually

2. If the script fails to connect:
   - Ensure MetaTrader 5 is running
   - Verify you're logged into your account
   - Check if your broker supports API trading

3. If orders fail:
   - Verify you have sufficient margin
   - Check if the symbol is available for trading
   - Ensure trading is allowed during current market hours

## Important Notes

- This is a basic example for educational purposes
- Always test with a demo account first
- Implement proper risk management before live trading
- Consider adding additional error handling for production use
