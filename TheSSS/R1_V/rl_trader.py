import time
import subprocess
import json
import os
import logging
from datetime import datetime
import numpy as np
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

class RLTrader:
    def __init__(self, train_interval=1):
        # Load environment variables
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))
        
        # Configure logging
        self.log_dir = os.path.expanduser(os.getenv("LOG_DIR", "~/Downloads/rl_trader_logs"))
        os.makedirs(self.log_dir, exist_ok=True)
        self.logger = logging.getLogger('RLTrader')
        self.logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'rl_trader.log'),
            maxBytes=1e6,
            backupCount=3
        )
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        
        # Initialize trading parameters
        self.data_path = os.getenv("HISTORICAL_DATA_PATH", 
                                 "TheSSS/trading-backtrader-azure/data/historical_data.csv")
        self.train_interval = train_interval
        self.historical_data = self.load_historical_data()
        self.episodes = 0
        self.training_start = None
        self.training_end = None
        self.total_reward = 0.0
        self.prev_total_reward = 0.0

    def load_historical_data(self):
        import pandas as pd
        
        df = pd.read_csv(
            self.data_path,
            parse_dates=['timestamp'],
            index_col='timestamp',
            dayfirst=False,
            dtype={'open': 'float64', 'high': 'float64', 'low': 'float64', 'close': 'float64', 'volume': 'float64'}
        )
        
        required_cols = {'open', 'high', 'low', 'close', 'volume'}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
            
        df = df[
            (df['close'] > 0) &
            (df['volume'] >= 0) &
            (df['high'] >= df['low']) &
            (df['high'] >= df['open']) &
            (df['high'] >= df['close']) &
            (df['low'] <= df['open']) &
            (df['low'] <= df['close'])
        ].dropna()
        
        df = df[~df.index.duplicated(keep='first')]
        self.logger.info("Loaded %d validated historical records", len(df))
        return df
    
    def log_improvement(self, improvement_percentage):
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Episode {self.episodes}: Improvement of {improvement_percentage:.2f}% (Total Reward: {self.total_reward:.2f})\n"
        log_file = os.path.join(self.log_dir, "improvements.log")
        
        try:
            with open(log_file, "a", encoding="utf-8") as logfile:
                logfile.write(log_message)
            self.logger.info(f"Logged improvement: {log_message.strip()}")
        except Exception as e:
            self.logger.error(f"Failed to log improvement: {str(e)}")

    def run_trading(self):
        try:
            self.training_start = datetime.now()
            total_rows = len(self.historical_data)
            self.logger.info(f"Starting training session with {total_rows} historical records")
import time
import subprocess
import json
import os
import logging
from datetime import datetime
import numpy as np
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

class RLTrader:
    def __init__(self, train_interval=1):
        # Load environment variables
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))
        
        # Configure logging
        self.log_dir = os.path.expanduser(os.getenv("LOG_DIR", "~/Downloads/rl_trader_logs"))
        os.makedirs(self.log_dir, exist_ok=True)
        self.logger = logging.getLogger('RLTrader')
        self.logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'rl_trader.log'),
            maxBytes=1e6,
            backupCount=3
        )
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        
        # Initialize trading parameters
        self.data_path = os.getenv("HISTORICAL_DATA_PATH", 
                                 "TheSSS/trading-backtrader-azure/data/historical_data.csv")
        self.train_interval = train_interval
        self.historical_data = self.load_historical_data()
        self.episodes = 0
        self.training_start = None
        self.training_end = None
        self.total_reward = 0.0
        self.prev_total_reward = 0.0

    def load_historical_data(self):
        import pandas as pd
        
        df = pd.read_csv(
            self.data_path,
            parse_dates=['timestamp'],
            index_col='timestamp',
            dayfirst=False,
            dtype={'open': 'float64', 'high': 'float64', 'low': 'float64', 'close': 'float64', 'volume': 'float64'}
        )
        
        required_cols = {'open', 'high', 'low', 'close', 'volume'}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
            
        df = df[
            (df['close'] > 0) &
            (df['volume'] >= 0) &
            (df['high'] >= df['low']) &
            (df['high'] >= df['open']) &
            (df['high'] >= df['close']) &
            (df['low'] <= df['open']) &
            (df['low'] <= df['close'])
        ].dropna()
        
        df = df[~df.index.duplicated(keep='first')]
        print(f"Loaded {len(df)} validated historical records")
        return df
    
    def log_improvement(self, improvement_percentage):
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Episode {self.episodes}: Improvement of {improvement_percentage:.2f}% (Total Reward: {self.total_reward:.2f})\n"
        log_file = os.path.join(self.log_dir, "improvements.log")
        
        try:
            with open(log_file, "a", encoding="utf-8") as logfile:
                logfile.write(log_message)
            self.logger.info(f"Logged improvement: {log_message.strip()}")
        except Exception as e:
            self.logger.error(f"Failed to log improvement: {str(e)}")

    def run_trading(self):
        try:
            self.training_start = datetime.now()
            total_rows = len(self.historical_data)
            self.logger.info("Training session initialized with %d historical records", total_rows)
            sessions = []
            current_session = {'start': self.training_start, 'start_reward': self.total_reward, 'improvements': []}

            while (datetime.now() - self.training_start).total_seconds() < 1800:
                for timestamp, row in self.historical_data.iterrows():
                    if (datetime.now() - self.training_start).total_seconds() >= 1800:
                        self.logger.warning("Training halted after 30 minute limit - Completed %d episodes with final reward %.2f", self.episodes, self.total_reward)
                        break

                    self.episodes += 1
                    episode_reward = self.train(row)
                    
                    if self.episodes % 10 == 0:
                        elapsed = datetime.now() - self.training_start
                        self.logger.debug("Episode %d - Reward: %.2f | Elapsed: %s", self.episodes, self.total_reward, elapsed)
                    
                    progress = self.episodes / len(self.historical_data) * 100
                    self.logger.debug("Training progress: %.1f%%", progress)  # More frequent debug logging

                    if self.total_reward > self.prev_total_reward:
                        base = max(self.prev_total_reward, 1)
                        improvement = ((self.total_reward - self.prev_total_reward) / base) * 100.0
                        self.log_improvement(improvement)
                        current_session['improvements'].append({
                            'episode': self.episodes,
                            'timestamp': datetime.now().isoformat(),
                            'improvement': improvement,
                            'total_reward': self.total_reward
                        })
                        self.prev_total_reward = self.total_reward

                    time.sleep(self.train_interval)

                else:
                    self.logger.info("Completed full data cycle - Episode %d | Total Reward: %.2f", self.episodes, self.total_reward)
                    continue
                break

        except Exception as e:
            print(f"Critical error during training: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.training_end = datetime.now()
            current_session.update({
                'end': self.training_end,
                'end_reward': self.total_reward,
                'duration_seconds': (self.training_end - self.training_start).total_seconds()
            })
            sessions.append(current_session)
            print(f"Final training duration: {self.training_end - self.training_start}")
            print(f"Session Report:\n{json.dumps(sessions, indent=2, default=str)}")
        
    def train(self, row):
        current_state = self.get_market_state(row)
        action = self.get_action()
        next_state = self.get_market_state(row)
        
        episode_reward = self.calculate_reward(action, current_state, next_state)
        episode_reward = float(np.nan_to_num(episode_reward, nan=0.0))
        self.total_reward = np.nan_to_num(
            self.total_reward + float(episode_reward), 
            nan=0.0, 
            posinf=0.0, 
            neginf=0.0
        )
        
        self.logger.debug("""
=== Training Episode %d ===
Episode Reward: %.2f
Total Reward: %.2f
Elapsed Time: %s
============================
""", self.episodes, episode_reward, self.total_reward, datetime.now() - self.training_start)
        
        time.sleep(1)
        self.retrain_model()
        return episode_reward

    def retrain_model(self):
        if self.episodes % 5 != 0:
            return True

        self.logger.info("Starting validated model training cycle")
        try:
            model_check = subprocess.run(["ollama", "ps"], capture_output=True, text=True, timeout=30)
            if "deepseek-r1:1.5b" not in model_check.stdout:
                subprocess.run(["ollama", "run", "deepseek-r1:1.5b"], timeout=120, check=True)

            training_prompt = f"PPO_UPDATE:\nEPISODES={self.episodes}\nTOTAL_REWARD={self.total_reward:.2f}\nHYPERPARAMETERS:\nclip_range=0.1\nentropy_coeff=0.02\nbatch_size=16\ngamma=0.90\nexperience_window=500\n"
            
            log_path = os.path.join(self.log_dir, f"training_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")
            success = False
            proc = None
            logfile = None
            
            try:
                logfile = open(log_path, 'w')
                proc = subprocess.Popen(
                    ["ollama", "run", "deepseek-r1:1.5b"],
                    stdin=subprocess.PIPE,
                    stdout=logfile,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                try:
                    proc.stdin.write(training_prompt)
                    proc.stdin.flush()
                except (BrokenPipeError, OSError) as e:
                    self.logger.error("Training write failed: %s", str(e), exc_info=True)
                    return False
                finally:
                    proc.stdin.close()
                
                try:
                    exit_code = proc.wait(timeout=480)
                    success = exit_code == 0
                except subprocess.TimeoutExpired:
                    print("Training timeout after 8 minutes", flush=True)
                    proc.kill()
                
            except Exception as e:
                print(f"Training failed: {str(e)}", flush=True)
                return False
            finally:
                if proc and proc.poll() is None:
                    proc.terminate()
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                if logfile:
                    logfile.close()
                return success

        except Exception as e:
            print(f"Training failure: {str(e)[:500]}")
            return False

    def get_action(self):
        # Use modulo to wrap index within valid range
        idx = self.episodes % len(self.historical_data)
        state = self.get_market_state(self.historical_data.iloc[idx])
        state = self.clean_state(state)
    
        try:
            result = subprocess.run(
                ["ollama", "run", "deepseek-r1:1.5b", f"ACTION_QUERY: {json.dumps(state)}"],
                capture_output=True,
                text=True,
                check=True,
                timeout=15
            )
            action = result.stdout.strip().upper()
            if action in ("BUY", "SELL", "HOLD"):
                return action
                
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            pass
            
        if state['rsi'] < 30:
            return "BUY"
        elif state['rsi'] > 70:
            return "SELL"
        return "HOLD"
        
    def get_market_state(self, row):
        return {
            'price': row['close'],
            'spread': 0.0002,
            'volume': row['volume'],
            'rsi': row.get('rsi', self.calculate_rsi(row)),
            'macd': row.get('macd', self.calculate_macd(row))
        }

    def clean_state(self, state):
        for key, value in state.items():
            if isinstance(value, float) and np.isnan(value):
                state[key] = None
        return state

    def calculate_rsi(self, row):
        try:
            prices = self.historical_data['close']
            deltas = np.diff(prices)
            
            if len(deltas) < 14:
                return 50.0
            
            deltas_14 = deltas[:14]
            up_deltas = deltas_14[deltas_14 >= 0]
            down_deltas = deltas_14[deltas_14 < 0]
            
            up = up_deltas.mean() if len(up_deltas) > 0 else 0
            down = np.abs(down_deltas.mean()) if len(down_deltas) > 0 else 1e-9
            
            rs = up / down
            rsi = 100.0 - (100.0 / (1 + rs))
            return np.nan_to_num(rsi, nan=50.0)
        except Exception as e:
            self.logger.error("RSI calculation error: %s", str(e), exc_info=True)
            return 50.0

    def calculate_macd(self, row):
        try:
            prices = self.historical_data['close']
            if len(prices) < 26:
                return 0.0
                
            exp12 = prices.ewm(span=12, adjust=False, min_periods=12).mean()
            exp26 = prices.ewm(span=26, adjust=False, min_periods=26).mean()
            macd_value = exp12.iloc[-1] - exp26.iloc[-1]
            return np.nan_to_num(macd_value, nan=0.0)
        except Exception as e:
            self.logger.error("MACD calculation error: %s", str(e), exc_info=True)
            return 0.0

    def calculate_reward(self, action, state, next_state):
        try:
            # Get parameters from environment variables
            transaction_cost = float(os.getenv("TRANSACTION_COST", "0.0005"))
            risk_factor = float(os.getenv("RISK_ADJUSTMENT_FACTOR", "0.15"))
            vol_window = int(os.getenv("VOLATILITY_WINDOW", "14"))
            min_size = float(os.getenv("MIN_POSITION_SIZE", "0.01"))
            max_size = float(os.getenv("MAX_POSITION_SIZE", "1.0"))
            default_reward = float(os.getenv("DEFAULT_REWARD", "-0.1"))

            # Get price data with validation
            current_price = float(np.nan_to_num(state.get('price', 0.0)))
            next_price = float(np.nan_to_num(next_state.get('price', current_price)))
            
            # Calculate price movement and volatility
            price_move = next_price - current_price
            volatility = self.calculate_volatility(vol_window)
            
            # Transaction cost adjustment
            spread = float(np.nan_to_num(state.get('spread', 0.0002))) + transaction_cost
            
            # Risk-adjusted position sizing
            position_size = np.clip(
                risk_factor / max(volatility, 1e-5),  # Prevent division by zero
                min_size,
                max_size
            )
            
            # Reward calculation
            if action == 'BUY':
                pips = (price_move - spread) * 10000
            elif action == 'SELL':
                pips = (-price_move - spread) * 10000
            else:  # HOLD
                return default_reward
                
            # Apply volatility scaling and risk adjustment
            scaled_pips = pips * position_size
            risk_adjusted_reward = scaled_pips * (1 - risk_factor)
            
            # Final validation and clipping
            validated_reward = np.clip(
                np.nan_to_num(risk_adjusted_reward, nan=default_reward), 
                -1000.0, 
                1000.0
            )
            
            self.logger.debug(
                f"Reward calc: Action={action} | PriceMove={price_move:.4f} | "
                f"Volatility={volatility:.4f} | Size={position_size:.2f} | "
                f"FinalReward={validated_reward:.2f}"
            )
            
            return float(validated_reward)
            
        except KeyError as e:
            self.logger.error(f"Missing state key {e}, defaulting to 0 reward")
            return 0.0

if __name__ == "__main__":
    trader = RLTrader(train_interval=1)
    trader.logger.info("Starting RL trading session")
    try:
        trader.run_trading()
    except KeyboardInterrupt:
        trader.logger.warning("Training session interrupted by user input")
    finally:
        trader.logger.info("Training session completed")
