from src.data_processing import fetch_data, preprocess_data
from src.strategy import generate_signals
from src.backtesting import backtest
from src.enhanced_dashboard import create_enhanced_dashboard
import pandas as pd
import numpy as np


# Step 1: Fetch raw data and preprocess it
print("Fetching data...")
raw_file = fetch_data("AAPL", "2021-01-01", "2023-11-28", "data/raw")
processed_file = preprocess_data(raw_file, "data/processed")

# Step 2: Load processed data
print("Loading processed data...")
data = pd.read_csv(processed_file, index_col='Date', parse_dates=True)

# Step 3: Generate trading signals
print("Generating trading signals...")
data = generate_signals(data)

# Step 4: Backtest the trading strategy
print("Running backtest...")
data = backtest(data)

# Step 5: Calculate performance metrics
print("Calculating performance metrics...")
sharpe_ratio = data['Portfolio'].pct_change().mean() / data['Portfolio'].pct_change().std() * np.sqrt(252)
max_drawdown = ((data['Portfolio'] - data['Portfolio'].cummax()) / data['Portfolio'].cummax()).min()
win_rate = len(data[data['Signal'] == 1]) / len(data[data['Signal'] != 0]) * 100

metrics = {
    'sharpe': round(sharpe_ratio, 2),
    'drawdown': f"{round(max_drawdown * 100, 2)}%",
    'win_rate': round(win_rate, 2)
}

# Step 6: Use best strategy parameters (from optimization)
best_params = (50, 200)  # SMA Short = 50, SMA Long = 200 (final optimized settings)

# Step 7: Generate natural language suggestions
suggestions = (
    f"The model suggests a {metrics['win_rate']}% win rate with a maximum drawdown of {metrics['drawdown']}. "
    f"The strategy appears to have strong upward momentum based on the current parameters: "
    f"SMA Short Window = {best_params[0]} and SMA Long Window = {best_params[1]}."
)

# Step 8: Create the enhanced dashboard
print("Launching dashboard...")
create_enhanced_dashboard(data, metrics=metrics, suggestions=suggestions, best_params=best_params)
