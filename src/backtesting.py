def backtest(data, initial_balance=10000):
    """Simulate backtesting for the strategy and calculate metrics."""
    balance = initial_balance
    positions = 0
    data['Portfolio'] = balance

    for i in range(1, len(data)):
        if data['Signal'].iloc[i] == 1 and positions == 0:
            # Buy
            positions = balance / data['Close'].iloc[i]
            balance = 0
        elif data['Signal'].iloc[i] == -1 and positions > 0:
            # Sell
            balance = positions * data['Close'].iloc[i]
            positions = 0
        data['Portfolio'].iloc[i] = balance + (positions * data['Close'].iloc[i])

    # Calculate cumulative returns
    data['Daily Returns'] = data['Portfolio'].pct_change()
    data['Cumulative Returns'] = (1 + data['Daily Returns']).cumprod() - 1

    # Calculate drawdown
    data['Cumulative Max'] = data['Portfolio'].cummax()
    data['Drawdown'] = (data['Portfolio'] - data['Cumulative Max']) / data['Cumulative Max']

    return data
