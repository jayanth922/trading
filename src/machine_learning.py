from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import numpy as np

def prepare_lstm_data(data, window_size=60):
    """Prepare data for LSTM model."""
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data[['Close']])

    X, y = [], []
    for i in range(window_size, len(scaled_data)):
        X.append(scaled_data[i-window_size:i, 0])
        y.append(scaled_data[i, 0])

    return np.array(X), np.array(y), scaler

def train_lstm_model(X_train, y_train):
    """Train an LSTM model."""
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
        LSTM(units=50, return_sequences=False),
        Dense(units=25),
        Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=5, batch_size=32, verbose=1)
    return model

def predict_prices(model, X_test, scaler):
    """Predict future prices and reverse scaling."""
    predictions = model.predict(X_test)
    return scaler.inverse_transform(predictions)


from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

def prepare_classification_data(data):
    """Prepare data for signal classification."""
    data['Target'] = data['Signal'].shift(-1)  # Predict next day's signal
    data.dropna(inplace=True)

    features = ['SMA_50', 'SMA_200', 'RSI', 'BB_Upper', 'BB_Lower']
    X = data[features]
    y = data['Target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_xgb_classifier(X_train, y_train):
    """Train an XGBoost classifier."""
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)
    return model

