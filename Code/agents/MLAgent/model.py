import os
import tensorflow as tf
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Conv2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from matplotlib import pyplot as plt
from Code.environment.constants import AMOUNT_ROWS, AMOUNT_COLUMNS
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau


def build_connect4_cnn(input_shape=(AMOUNT_ROWS, AMOUNT_COLUMNS, 3), num_classes=AMOUNT_COLUMNS):
    model = Sequential([
        Input(shape=input_shape),

        Conv2D(64, (3, 3), activation='relu'),
        Conv2D(128, (3, 3), activation='relu'),
        Conv2D(128, (3, 3), activation='relu'),
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])

    optimizer = Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()
    return model


def train_model(model, X_train, y_train, epochs=15, batch_size=32, validation_split=0.15, callbacks=[]):
    """
    Trains a given Keras model on given training data.


    :param model : the model to train
    :param X_train: training data (board states)
    :param y_train: training labels (chosen move in that given board state)
    :param epochs: amount of training epochs.
    :param batch_size: size of the batches
    :param validation_split: ratio of validation data to the total data set.

    Returns:
        tf.keras.callbacks.History: Das History-Objekt des Trainingsprozesses.
    """
    print(f"Start trainign fro {epochs} epochs.")
    history = model.fit(X_train, y_train,
                        epochs=epochs,
                        batch_size=batch_size,
                        validation_split=validation_split,
                        shuffle=True,
                        callbacks=callbacks)
    print("Training complete.")
    return history


def save_trained_model(model, filename="connect4_cnn_model.keras"):
    """
    Saves a trained Keras model on given training data.


    :param model: the model to save.
    :param filename: the filename where the model will be saved.
    """
    try:
        model.save(filename)
        print(f"Model successfully saved to: {filename}")
    except Exception as e:
        print(f"Error while saving the model {e}")


def load_trained_model(filename="connect4_cnn_model.keras"):
    """
    loads a saved Keras model from disk

    :param filename: filename where the model is saved.

    :return tf.keras.Model: the loaded model, None if no model was found.
    """
    if not os.path.exists(filename):
        print(f"Could not find model{filename}")
        return None
    try:
        model = tf.keras.models.load_model(filename)
        print(f"Successfully loaded model from{filename}")
        # model.compile(...)
        return model
    except Exception as e:
        print(f"Model not found: {e}")
        return None


def plot_training_loss(history):
    """
    Plots just the training and validation loss over epochs.


    :param history: The History object returned by model.fit() .
    """

    plt.figure(figsize=(8, 5))  # Adjust figure size for a single plot

    # Plot training loss
    plt.plot(history.history['loss'], label='Training Loss')

    plt.plot(history.history['val_loss'], label='Validation Loss')

    # Add titles and labels
    plt.title('Model Training Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()