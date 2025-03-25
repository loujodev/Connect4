import tensorflow as tf
from keras.callbacks import ReduceLROnPlateau
from keras.src.layers import BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model


def create_connect4_model(input_shape, output_units=7):
    model = Sequential([
        # Input layer with batch normalization
        Dense(256, activation='relu', input_shape=(input_shape,)),
        BatchNormalization(),
        Dropout(0.3),  # Slightly higher dropout

        # Hidden layer 1
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),

        # Hidden layer 2
        Dense(64, activation='relu'),
        BatchNormalization(),

        # Output layer
        Dense(output_units, activation='softmax')  # 7 possible moves
    ])

    model.compile(optimizer=Adam(learning_rate=0.0001),
                  loss='sparse_categorical_crossentropy',  # Changed from binary
                  metrics=['accuracy'])
    return model


def train_model(X, y, epochs=30, batch_size=32):
    """
    Trains the supervised learning model
    """
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.15, random_state=42)


    model = create_connect4_model(input_shape=X.shape[1], output_units=7)  # 7 columns in Connect4
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2,
                                  patience=5, min_lr=0.001)

    history = model.fit(X_train, y_train,
                        epochs=epochs,
                        batch_size=batch_size,
                        validation_data=(X_val, y_val),
                        verbose=1,
                        callbacks=[reduce_lr])

    return model, history

def continue_training(model, X_new, y_new, epochs=30, batch_size=32):
    """
    Continues training an existing model with new data
    """
    # Split new data for validation
    X_train, X_val, y_train, y_val = train_test_split(X_new, y_new, test_size=0.15)

    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2,
                                  patience=5, min_lr=0.001)
    # Continue training
    history = model.fit(X_train, y_train,
                        epochs=epochs,
                        batch_size=batch_size,
                        validation_data=(X_val, y_val),
                        verbose=1,
                        callbacks=[reduce_lr])
    return model, history


def save_model(model, filename='connect4_model'):
    """
    Saves the trained model to disk
    """
    model.save(filename)
    print(f"Model saved to {filename}")


def load_saved_model(filename='connect4_model'):
    """
    Loads a saved model from disk
    """
    model = load_model(filename)
    print(f"Model loaded from {filename}")
    return model

