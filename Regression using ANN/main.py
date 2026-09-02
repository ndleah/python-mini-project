import os
import sys
import numpy as np
import pandas as pd

def generate_synthetic_ccpp_data(n_samples: int = 1000):
    """Generate synthetic Combined Cycle Power Plant dataset."""
    np.random.seed(42)
    AT = np.random.uniform(1.8, 37.1, n_samples)
    V = np.random.uniform(25.3, 81.6, n_samples)
    AP = np.random.uniform(992.8, 1033.3, n_samples)
    RH = np.random.uniform(25.5, 100.1, n_samples)

    # Physical formula approximation for electrical energy output PE
    PE = 490 - (1.7 * AT) - (0.3 * V) + (0.1 * (AP - 1000)) + (0.05 * RH) + np.random.normal(0, 2, n_samples)

    return pd.DataFrame({'AT': AT, 'V': V, 'AP': AP, 'RH': RH, 'PE': PE})

def build_and_train_ann(df: pd.DataFrame):
    """Train Artificial Neural Network for regression."""
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values

    try:
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import mean_squared_error, r2_score
    except ImportError:
        print("Error: scikit-learn is required. Install via 'pip install scikit-learn'.")
        return None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Try Keras / TensorFlow first, fallback to MLPRegressor
    try:
        import tensorflow as tf
        print("Training ANN using TensorFlow Keras Sequential model...")
        ann = tf.keras.models.Sequential([
            tf.keras.layers.Dense(units=6, activation='relu', input_shape=(4,)),
            tf.keras.layers.Dense(units=6, activation='relu'),
            tf.keras.layers.Dense(units=1)
        ])
        ann.compile(optimizer='adam', loss='mean_squared_error')
        ann.fit(X_train_scaled, y_train, batch_size=32, epochs=50, verbose=0)
        y_pred = ann.predict(X_test_scaled).flatten()
    except Exception as e:
        print(f"Notice: TensorFlow unavailable ({e}). Using sklearn MLPRegressor fallback.")
        from sklearn.neural_network import MLPRegressor
        ann = MLPRegressor(hidden_layer_sizes=(6, 6), max_iter=500, random_state=42)
        ann.fit(X_train_scaled, y_train)
        y_pred = ann.predict(X_test_scaled)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Model Trained Successfully!")
    print(f"Test Mean Squared Error (MSE): {mse:.2f}")
    print(f"Test R2 Score: {r2:.4f}")

    return ann

def main():
    data_path = os.path.join(os.path.dirname(__file__), "Folds5x2_pp.xlsx")
    if os.path.exists(data_path):
        try:
            print(f"Loading dataset from '{data_path}'...")
            df = pd.read_excel(data_path)
        except Exception as err:
            print(f"Warning: Failed to load excel dataset ({err}). Generating synthetic data...")
            df = generate_synthetic_ccpp_data()
    else:
        print("Dataset file 'Folds5x2_pp.xlsx' not found. Using synthetic CCPP dataset...")
        df = generate_synthetic_ccpp_data()

    build_and_train_ann(df)

if __name__ == '__main__':
    main()
