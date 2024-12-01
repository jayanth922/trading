import os
import pandas as pd
import yfinance as yf

def fetch_data(ticker, start_date, end_date, save_path):
    """Fetch historical data and save to the raw data folder."""
    data = yf.download(ticker, start=start_date, end=end_date)
    # Reset the index to include the 'Date' column explicitly
    data.reset_index(inplace=True)

    # Ensure no metadata rows are included
    if "Unnamed: 0" in data.columns or "AAPL" in data.iloc[0].to_list():
        data = data[1:]  # Skip the first row if it contains metadata

    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, f"{ticker}_raw.csv")
    data.to_csv(file_path, index=False)
    return file_path



def preprocess_data(file_path, save_path):
    """Preprocess data and save the processed file."""
    # Read the raw data
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {e}")
    
    # Debug: Print first few rows of data
    print("Raw data preview:\n", data.head())
    
    # Ensure 'Date' is present
    if 'Date' not in data.columns:
        raise ValueError("'Date' column is missing from the data.")
    
    # Set 'Date' as the index and parse dates
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    
    # Ensure numeric types for required columns
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')  # Convert to numeric, replace invalid with NaN
    
    # Drop rows with NaN values
    data.dropna(inplace=True)

    # Add features (SMA, RSI, Bollinger Bands)
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()
    data['RSI'] = calculate_rsi(data['Close'], 14)
    data['BB_Middle'] = data['Close'].rolling(window=20).mean()
    data['BB_Upper'] = data['BB_Middle'] + 2 * data['Close'].rolling(window=20).std()
    data['BB_Lower'] = data['BB_Middle'] - 2 * data['Close'].rolling(window=20).std()
    
    # Save the processed data
    os.makedirs(save_path, exist_ok=True)
    processed_file_path = os.path.join(save_path, f"{os.path.basename(file_path).split('_')[0]}_processed.csv")
    data.to_csv(processed_file_path)
    return processed_file_path




def calculate_rsi(series, period=14):
    """Calculate RSI indicator."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Example Usage
if __name__ == "__main__":
    raw_file = fetch_data("AAPL", "2021-01-01", "2023-11-28", "data/raw")
    preprocess_data(raw_file, "data/processed")
