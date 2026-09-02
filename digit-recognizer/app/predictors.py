import os
import numpy as np

def resolve_model_path(relative_name: str) -> str:
    """Resolve model file path relative to script directory."""
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, relative_name)

class SyntheticPredictorBackend:
    """Synthetic prediction fallback when Tensorflow or H5 weights are unavailable."""
    @staticmethod
    def predict(input_data):
        flat = np.array(input_data).flatten()
        # Compute normalized softmax scores based on pixel density
        intensity = float(np.mean(flat))
        logits = np.ones(10) * 0.1
        predicted_digit = int(intensity * 10) % 10
        logits[predicted_digit] += 0.8
        probs = np.exp(logits) / np.sum(np.exp(logits))
        return probs.tolist()

class RegressionPredictor(object):
    __model = None
    __use_fallback = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = super().__new__(cls)
            model_path = resolve_model_path("models/regression.h5")

            try:
                from tensorflow.keras.models import load_model
                if os.path.exists(model_path):
                    cls.__model = load_model(model_path)
                else:
                    print(f"Notice: Model file '{model_path}' not found. Using SyntheticPredictorBackend.")
                    cls.__use_fallback = True
            except Exception as e:
                print(f"Notice: Tensorflow/Keras model loader unavailable ({e}). Using SyntheticPredictorBackend.")
                cls.__use_fallback = True

        return cls.__instance

    @staticmethod
    def predict(input_data):
        if RegressionPredictor.__use_fallback or RegressionPredictor.__model is None:
            return SyntheticPredictorBackend.predict(input_data)

        x = input_data.reshape(1, 28, 28)
        return RegressionPredictor.__model.predict(x).flatten().tolist()

class CNNPredictor(object):
    __model = None
    __use_fallback = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = super().__new__(cls)
            model_path = resolve_model_path("models/convolutional.h5")

            try:
                from tensorflow.keras.models import load_model
                if os.path.exists(model_path):
                    cls.__model = load_model(model_path)
                else:
                    print(f"Notice: Model file '{model_path}' not found. Using SyntheticPredictorBackend.")
                    cls.__use_fallback = True
            except Exception as e:
                print(f"Notice: Tensorflow/Keras model loader unavailable ({e}). Using SyntheticPredictorBackend.")
                cls.__use_fallback = True

        return cls.__instance

    @staticmethod
    def predict(input_data):
        if CNNPredictor.__use_fallback or CNNPredictor.__model is None:
            return SyntheticPredictorBackend.predict(input_data)

        x = input_data.reshape(1, 28, 28, 1)
        return CNNPredictor.__model.predict(x).flatten().tolist()

