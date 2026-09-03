import os
import sys

# Must set environment variable BEFORE importing Keras
os.environ["KERAS_BACKEND"] = "tensorflow"

import numpy as np

def load_mnist_data():
    """Load MNIST dataset or generate synthetic fallback dataset offline."""
    try:
        import keras
        print("Loading MNIST dataset from Keras...")
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        return (x_train, y_train), (x_test, y_test)
    except Exception as e:
        print(f"Notice: Could not download MNIST dataset ({e}). Generating synthetic dataset fallback...")
        np.random.seed(42)
        x_train = np.random.randint(0, 256, (1000, 28, 28), dtype=np.uint8)
        y_train = np.random.randint(0, 10, (1000,), dtype=np.uint8)
        x_test = np.random.randint(0, 256, (200, 28, 28), dtype=np.uint8)
        y_test = np.random.randint(0, 10, (200,), dtype=np.uint8)
        return (x_train, y_train), (x_test, y_test)

def train_and_evaluate_mnist(epochs_num: int = 2):
    try:
        import keras
    except ImportError:
        print("Error: Keras is required. Install via 'pip install keras tensorflow'.")
        return

    (x_train, y_train), (x_test, y_test) = load_mnist_data()
    print("Shape of x_train, y_train, x_test, y_test: ", x_train.shape, y_train.shape, x_test.shape, y_test.shape)

    # Reshaping Data
    x_train = x_train.reshape((x_train.shape[0], 28 * 28)).astype('float32') / 255
    x_test = x_test.reshape((x_test.shape[0], 28 * 28)).astype('float32') / 255
    print("Shape after reshaping: ", x_train.shape, y_train.shape, x_test.shape, y_test.shape)

    # Creating model
    model = keras.models.Sequential([
        keras.layers.InputLayer(input_shape=(28 * 28,)),
        keras.layers.Dense(512, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10, activation='softmax')
    ])

    print(model.summary())

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss=keras.losses.SparseCategoricalCrossentropy(),
        metrics=[keras.metrics.SparseCategoricalAccuracy(name='accuracy')]
    )

    # Training the model
    batch_size = 64
    callbacks = [keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)]

    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs_num, validation_split=0.2, callbacks=callbacks)

    # Evaluating on test data
    test_loss, test_accuracy = model.evaluate(x_test, y_test)
    print("Test Loss: ", test_loss)
    print("Test Accuracy: ", test_accuracy)
    return test_accuracy

def main():
    epochs_val = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    train_and_evaluate_mnist(epochs_val)

if __name__ == '__main__':
    main()