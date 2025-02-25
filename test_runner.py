#!/usr/bin/env python3
import unittest
from TheSSS.R1_V.rl_trader import RLTrader

if __name__ == '__main__':
    loader = unittest.TestLoader()
    # Discover all files matching test*.py recursively
    suite = loader.discover(start_dir='.', pattern='test*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    exit(not result.wasSuccessful())
