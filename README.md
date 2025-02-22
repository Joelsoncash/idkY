# MetaTrader 5 Python Trading Example

This project demonstrates how to use the MetaTrader 5 (MT5) Python package for connecting, retrieving account information, and executing trades. The project is structured to follow a clear development flow from planning to deployment.

---

## Project Outline & Checklist

### 1. Project Preparation & Requirements
**Documentation & Objectives**  
- Gather all relevant documentation (PDFs or other documents) that provide the theoretical framework of your trading model.  
- Define clear objectives such as automated trade entries/exits and risk management strategies.

**Impact on Later Steps**  
- These foundational documents will guide the design of the simulation environment.
- They ensure that every component aligns with your overarching goals.

### 2. Extract & Formalize Trading Strategy
**Trading Rules Extraction**  
- Use tools like `pdfplumber` or `PyPDF2` to extract trading rules from your documentation.

**Formalization & Specification**  
- Structure these rules by defining entry/exit conditions and risk management protocols.  
- Create a strategy specification document (e.g., pseudocode or flowcharts).

**Impact on Later Steps**  
- Directly implemented in the simulation environment (see Step 4) and influences model decision-making for training and backtesting.

### 3. Historical Data Pipeline
**Data Source Selection & Script Development**  
- Choose your data provider (MetaTrader 5, Yahoo Finance, etc.)  
- Develop Python scripts to fetch and preprocess historical market data.

**Data Formatting & Storage**  
- Store data in CSV or JSON format for easy ingestion by simulation and training modules.

**Impact on Later Steps**  
- Provides the data foundation for simulation, training, and backtesting your strategy.

---

## Overall Integration in the Project

**Foundation for Simulation & Model Training**  
- The insights and assets from steps 1–3 are integrated into the simulation environment (Step 4).  
- Formalized trading rules drive the decision-making logic while historical data provides a realistic market backdrop.

**Guiding Development & Testing**  
- These steps ensure that subsequent phases—from adapting the R1‑V framework to cloud deployment—are built on a well-defined strategy and robust data pipeline.

---

## Detailed Project Steps

### 4. Build the Trading Simulation Environment
- **Design Simulation Environment:** Create an environment (consider using an OpenAI Gym interface) to simulate market conditions.
- **Integrate Historical Data:** Feed your preprocessed market data into the simulation.
- **Implement Strategy Logic:** Code the trading rules from your documentation into the simulation’s reward functions.
- **Test Simulation:** Run simulations to validate that the environment behaves as expected.

### 5. Adapt the R1‑V Training Framework
- **Clone the R1‑V Repository:** Review its structure and isolate core components (e.g., training scripts like `grpo.py`).
- **Modify Data Loaders:** Replace image/text data loaders with modules that load your market data.
- **Customize Reward Functions:** Adapt the reward mechanism to reflect trading performance and risk metrics.
- **Adjust Model Architecture:** Tailor the model to accept market data inputs if necessary.

### 6. Model Development & Local Testing
- **Implement Your Trading Model:** Choose your approach (e.g., RL agent, LSTM-based predictor) and implement it.
- **Train on Subset of Data:** Run local training sessions to validate model behavior.
- **Backtest:** Evaluate model performance against historical data and strategy rules.

### 7. Azure Cloud Setup & Full-Scale Training
- **Sign in to Azure Portal:** Use your Azure trial to set up resources.
- **Create a GPU-Enabled VM:** For example, an Ubuntu 20.04 LTS VM with GPU (e.g., Standard_NC6).
- **Connect & Install Dependencies:** SSH into your VM and install CUDA-enabled PyTorch and other libraries.
- **Clone Your Repository:** Upload or clone your project repository (with integrated R1‑V components).
- **Run Full-Scale Training:** Execute the training script and monitor performance with proper checkpointing.

### 8. Integration with MetaTrader 5
- **Set Up MT5 API:** Ensure the MT5 Python package is installed on your environment.
- **Live Data Fetching Script:** Develop a script to retrieve live market data from MT5.
- **Order Execution Logic:** Code functions to execute orders using `mt5.order_send()`.
- **Test with a Demo Account:** Validate live performance in a paper trading mode.

### 9. Deployment, Monitoring & Maintenance
- **Deploy the Final System:** Consider containerization (e.g., with Docker) for the production environment.
- **Implement Monitoring & Alerts:** Use logging and monitoring tools to track system performance and errors.
- **Plan for Model Retraining:** Schedule periodic retraining sessions based on new data or performance decay.

### 10. Documentation & Future Enhancements
- **Document Every Step:** Maintain thorough documentation for setup, configuration, and operation.
- **User & Developer Guides:** Provide guides to assist future developers in understanding and extending the project.
- **Plan Enhancements:** Identify areas for improvements such as added features, improved risk management, or scalability.

---

## Trading Strategy: Breaking Resistance and Support Levels

### Overview
This strategy uses dynamic support and resistance levels on a 5‑minute chart—updated via recent price action—to trigger trades based on candle closes relative to these levels combined with a 40‑period Simple Moving Average (SMA). The system limits to up to 10 orders per chart and ensures new entries occur only if the price matches the initial trade level. Trades are closed when the signal reverses.

### 1. Resistance Breakout (MT5 Implementation)
- **Setting Resistance:**  
  - Scan the last 3 hours of price data on a 5‑minute chart.  
  - Draw a horizontal line at the daily matching highest high.
- **Trade Execution (Breakout):**  
  - Trigger a buy order when the price breaks above the resistance line and at least one M5 candle closes above the 40‑period SMA.
  - Execute an automatic take profit at the first sign of a negative candle, then reset the system.
- **Additional Condition:**  
  - If the price falls back below resistance and one candle closes below the moving average, execute a short order.  
  - If the next candle closes above the moving average, liquidate profits immediately.

### 2. Support Breakdown (MT4 Implementation)
- **Setting Support:**  
  - Scan the last trading day on a 5‑minute chart.  
  - Draw a horizontal line at the daily matching lowest low.
- **Trade Execution (Breakdown):**  
  - Trigger a sell order when the price breaks below support and a M5 candle closes below the 40‑period SMA.
  - Execute an automatic take profit at the first sign of a positive candle, then reset the system.
- **Additional Condition:**  
  - If the price rises above the support line and one candle closes above the moving average, execute a buy order.  
  - If a subsequent candle closes below the moving average, liquidate profits immediately.

### 3. Buy and Sell Logic Requirements
- **Buy Conditions:**
  - A 5‑minute candle must close on or above the support line and above the 40‑period SMA.
  - Alternatively, a 5‑minute candle must close on or above the resistance line and above the 40‑period SMA.
- **Sell Conditions:**
  - A 5‑minute candle must close on or below the support line and below the 40‑period SMA.
  - Alternatively, a 5‑minute candle must close on or below the resistance line and below the 40‑period SMA.
- **Order Management:**
  - Place up to 10 orders per chart at a time.
  - Prevent new entries unless the price matches the initial buy/sell level for that chart.
  - If the same chart reverses from a buy signal to a sell signal (or vice versa), take profit on the previous trade before opening a new one.
- **Support and Resistance Refresh:**
  - Resistance: Recalculate using the last 3 hours of data.
  - Support: Determine using the most recent trading day’s data.

---

## Prerequisites

- MetaTrader 5 desktop application installed and running
- Python 3.11+ (recommended: Anaconda distribution)
- MT5 account credentials (demo or live)
- Basic understanding of technical analysis concepts

## Project Structure
```
MT1.0/
├── config/
│   └── mt5_config.json       # MT5 connection settings
├── TheSSS/                   # Reinforcement learning components
│   ├── R1-V/                # Core trading algorithms
│   └── strategies/          # Strategy implementations
├── check_mt5_import.py       # MT5 Python package verification
├── main.py                   # Main execution script
├── mt5_live_data.py          # Real-time market data feed
├── mt5_terminal_check.py     # MT5 platform status monitor
├── requirements.txt          # Python dependencies
└── README.md                 # This documentation
```

## Configuration Setup

1. Edit `config/mt5_config.json`:
```json
{
  "login": YOUR_MT5_ACCOUNT_NUMBER,
  "password": "YOUR_MT5_PASSWORD",
  "server": "YOUR_BROKER_SERVER_NAME",
  "symbols": ["EURUSD","XAUUSD","GBPUSD"],
  "timeframe": "M5",
  "update_interval": 60
}
```

2. For Azure cloud integration:
```bash
az vm create --resource-group TradingGroup --name RL-Trader-VM --image UbuntuLTS --size Standard_NC6 --admin-username azureuser
```

## Code Examples

### Basic MT5 Connection
```python
import MetaTrader5 as mt5

def connect_mt5():
    if not mt5.initialize():
        print("MT5 initialization failed")
        mt5.shutdown()
        return False
    print(f"Connected to {mt5.terminal_info().name}")
    return True
```

### Live Trading Signal Check
```python
def check_breakout(symbol, timeframe):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 10)
    current_close = rates['close'][-1]
    resistance = calculate_dynamic_resistance(rates)
    
    if current_close > resistance and above_sma(40):
        return "BUY"
    elif current_close < resistance and below_sma(40):
        return "SELL"
    return "HOLD"
```

## Getting Started

1. Ensure MetaTrader 5 is installed and running
2. Configure your credentials in `config/mt5_config.json`
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the trading system:
   ```sh
   python main.py --mode live --risk 0.02
   ```

## Troubleshooting

Common Issues                        | Solutions
------------------------------------|-------------------------
`MetaTrader5 initialization failed` | 1. Verify MT5 is running<br>2. Check firewall settings<br>3. Validate login credentials
`No historical data available`      | 1. Confirm symbol is valid<br>2. Check broker permissions<br>3. Adjust timeframe
`Azure VM connection issues`        | 1. Verify SSH keys<br>2. Check network security groups<br>3. Confirm subscription status
# MetaTrader 5 Python Trading Example

This project demonstrates how to use the MetaTrader 5 (MT5) Python package for connecting, retrieving account information, and executing trades. The project is structured to follow a clear development flow from planning to deployment.

---

## Project Outline & Checklist

### 1. Project Preparation & Requirements
**Documentation & Objectives**  
- Gather all relevant documentation (PDFs or other documents) that provide the theoretical framework of your trading model.  
- Define clear objectives such as automated trade entries/exits and risk management strategies.

**Impact on Later Steps**  
- These foundational documents will guide the design of the simulation environment.
- They ensure that every component aligns with your overarching goals.

### 2. Extract & Formalize Trading Strategy
**Trading Rules Extraction**  
- Use tools like `pdfplumber` or `PyPDF2` to extract trading rules from your documentation.

**Formalization & Specification**  
- Structure these rules by defining entry/exit conditions and risk management protocols.  
- Create a strategy specification document (e.g., pseudocode or flowcharts).

**Impact on Later Steps**  
- Directly implemented in the simulation environment (see Step 4) and influences model decision-making for training and backtesting.

### 3. Historical Data Pipeline
**Data Source Selection & Script Development**  
- Choose your data provider (MetaTrader 5, Yahoo Finance, etc.)  
- Develop Python scripts to fetch and preprocess historical market data.

**Data Formatting & Storage**  
- Store data in CSV or JSON format for easy ingestion by simulation and training modules.

**Impact on Later Steps**  
- Provides the data foundation for simulation, training, and backtesting your strategy.

---

## Overall Integration in the Project

**Foundation for Simulation & Model Training**  
- The insights and assets from steps 1–3 are integrated into the simulation environment (Step 4).  
- Formalized trading rules drive the decision-making logic while historical data provides a realistic market backdrop.

**Guiding Development & Testing**  
- These steps ensure that subsequent phases—from adapting the R1‑V framework to cloud deployment—are built on a well-defined strategy and robust data pipeline.

---

## Detailed Project Steps

### 4. Build the Trading Simulation Environment
- **Design Simulation Environment:** Create an environment (consider using an OpenAI Gym interface) to simulate market conditions.
- **Integrate Historical Data:** Feed your preprocessed market data into the simulation.
- **Implement Strategy Logic:** Code the trading rules from your documentation into the simulation’s reward functions.
- **Test Simulation:** Run simulations to validate that the environment behaves as expected.

### 5. Adapt the R1‑V Training Framework
- **Clone the R1‑V Repository:** Review its structure and isolate core components (e.g., training scripts like `grpo.py`).
- **Modify Data Loaders:** Replace image/text data loaders with modules that load your market data.
- **Customize Reward Functions:** Adapt the reward mechanism to reflect trading performance and risk metrics.
- **Adjust Model Architecture:** Tailor the model to accept market data inputs if necessary.

### 6. Model Development & Local Testing
- **Implement Your Trading Model:** Choose your approach (e.g., RL agent, LSTM-based predictor) and implement it.
- **Train on Subset of Data:** Run local training sessions to validate model behavior.
- **Backtest:** Evaluate model performance against historical data and strategy rules.

### 7. Azure Cloud Setup & Full-Scale Training
- **Sign in to Azure Portal:** Use your Azure trial to set up resources.
- **Create a GPU-Enabled VM:** For example, an Ubuntu 20.04 LTS VM with GPU (e.g., Standard_NC6).
- **Connect & Install Dependencies:** SSH into your VM and install CUDA-enabled PyTorch and other libraries.
- **Clone Your Repository:** Upload or clone your project repository (with integrated R1‑V components).
- **Run Full-Scale Training:** Execute the training script and monitor performance with proper checkpointing.

### 8. Integration with MetaTrader 5
- **Set Up MT5 API:** Ensure the MT5 Python package is installed on your environment.
- **Live Data Fetching Script:** Develop a script to retrieve live market data from MT5.
- **Order Execution Logic:** Code functions to execute orders using `mt5.order_send()`.
- **Test with a Demo Account:** Validate live performance in a paper trading mode.

### 9. Deployment, Monitoring & Maintenance
- **Deploy the Final System:** Consider containerization (e.g., with Docker) for the production environment.
- **Implement Monitoring & Alerts:** Use logging and monitoring tools to track system performance and errors.
- **Plan for Model Retraining:** Schedule periodic retraining sessions based on new data or performance decay.

### 10. Documentation & Future Enhancements
- **Document Every Step:** Maintain thorough documentation for setup, configuration, and operation.
- **User & Developer Guides:** Provide guides to assist future developers in understanding and extending the project.
- **Plan Enhancements:** Identify areas for improvements such as added features, improved risk management, or scalability.

---

## Trading Strategy: Breaking Resistance and Support Levels

### Overview
This strategy uses dynamic support and resistance levels on a 5‑minute chart—updated via recent price action—to trigger trades based on candle closes relative to these levels combined with a 40‑period Simple Moving Average (SMA). The system limits to up to 10 orders per chart and ensures new entries occur only if the price matches the initial trade level. Trades are closed when the signal reverses.

### 1. Resistance Breakout (MT5 Implementation)
- **Setting Resistance:**  
  - Scan the last 3 hours of price data on a 5‑minute chart.  
  - Draw a horizontal line at the daily matching highest high.
- **Trade Execution (Breakout):**  
  - Trigger a buy order when the price breaks above the resistance line and at least one M5 candle closes above the 40‑period SMA.
  - Execute an automatic take profit at the first sign of a negative candle, then reset the system.
- **Additional Condition:**  
  - If the price falls back below resistance and one candle closes below the moving average, execute a short order.  
  - If the next candle closes above the moving average, liquidate profits immediately.

### 2. Support Breakdown (MT4 Implementation)
- **Setting Support:**  
  - Scan the last trading day on a 5‑minute chart.  
  - Draw a horizontal line at the daily matching lowest low.
- **Trade Execution (Breakdown):**  
  - Trigger a sell order when the price breaks below support and a M5 candle closes below the 40‑period SMA.
  - Execute an automatic take profit at the first sign of a positive candle, then reset the system.
- **Additional Condition:**  
  - If the price rises above the support line and one candle closes above the moving average, execute a buy order.  
  - If a subsequent candle closes below the moving average, liquidate profits immediately.

### 3. Buy and Sell Logic Requirements
- **Buy Conditions:**
  - A 5‑minute candle must close on or above the support line and above the 40‑period SMA.
  - Alternatively, a 5‑minute candle must close on or above the resistance line and above the 40‑period SMA.
- **Sell Conditions:**
  - A 5‑minute candle must close on or below the support line and below the 40‑period SMA.
  - Alternatively, a 5‑minute candle must close on or below the resistance line and below the 40‑period SMA.
- **Order Management:**
  - Place up to 10 orders per chart at a time.
  - Prevent new entries unless the price matches the initial buy/sell level for that chart.
  - If the same chart reverses from a buy signal to a sell signal (or vice versa), take profit on the previous trade before opening a new one.
- **Support and Resistance Refresh:**
  - Resistance: Recalculate using the last 3 hours of data.
  - Support: Determine using the most recent trading day’s data.

---

## Getting Started

1. Ensure MetaTrader 5 is installed and running.
2. Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```

3. Run the main script:

   ```sh
   python main.py
   ```

---

## Notes
- This project is for educational purposes; always test with a demo account first.
- Detailed diagnostics and testing utilities are available in other scripts provided in the repository.

---

Happy Trading!
