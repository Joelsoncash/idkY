import unittest
from TheSSS.R1_V.rl_trader import RLTrader
from unittest.mock import MagicMock

class TestRV1(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.trader = RLTrader(self.mock_client, "EURUSD", "M1", "TheSSS/trading-backtrader-azure/data/historical_data.csv")
        
    def test_initialization(self):
        """Test RLTrader initialization"""
        self.trader.initialize_trainer()
        self.assertIsNotNone(self.trader.training_start)
        
    def test_training(self):
        """Test training progression"""
        self.trader.initialize_trainer()
        self.trader.run_trading()
            
        # Verify training completed
        self.assertIsNotNone(self.trader.training_end)
        self.assertGreater(self.trader.episodes, 0)

if __name__ == "__main__":
    unittest.main()
