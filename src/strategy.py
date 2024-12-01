def generate_signals(data):
    """Generate buy/sell signals based on SMA crossover."""
    data['Signal'] = 0
    data.loc[data['SMA_50'] > data['SMA_200'], 'Signal'] = 1  # Buy
    data.loc[data['SMA_50'] <= data['SMA_200'], 'Signal'] = -1  # Sell
    return data

def backtest(data, initial_balance=10000):
    """Simulate backtesting for the strategy."""
    balance = initial_balance
    positions = 0
    data['Portfolio'] = balance

    trades = []  # Store trade details
    for i in range(1, len(data)):
        if data['Signal'].iloc[i] == 1 and positions == 0:
            # Buy
            positions = balance / data['Close'].iloc[i]
            balance = 0
            trades.append({'Date': data.index[i], 'Action': 'Buy', 'Price': data['Close'].iloc[i]})
        elif data['Signal'].iloc[i] == -1 and positions > 0:
            # Sell
            balance = positions * data['Close'].iloc[i]
            positions = 0
            trades.append({'Date': data.index[i], 'Action': 'Sell', 'Price': data['Close'].iloc[i]})
        data['Portfolio'].iloc[i] = balance + (positions * data['Close'].iloc[i])

    return data, trades


import numpy as np

def calculate_sharpe_ratio(data):
    """Calculate the Sharpe Ratio."""
    daily_returns = data['Portfolio'].pct_change().dropna()
    return daily_returns.mean() / daily_returns.std() * np.sqrt(252)  # Annualized Sharpe Ratio

def optimize_strategy(data):
    """Optimize SMA parameters."""
    best_params = None
    best_sharpe = -np.inf

    for short_window in range(10, 51, 10):
        for long_window in range(100, 201, 20):
            data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
            data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
            data['Signal'] = 0
            data.loc[data['SMA_Short'] > data['SMA_Long'], 'Signal'] = 1
            data.loc[data['SMA_Short'] <= data['SMA_Long'], 'Signal'] = -1

            backtest_results, _ = backtest(data)
            sharpe = calculate_sharpe_ratio(backtest_results)
            if sharpe > best_sharpe:
                best_sharpe = sharpe
                best_params = (short_window, long_window)

    return best_params, best_sharpe
