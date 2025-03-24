import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model



def create_connect4_model(input_shape, output_units = 7):
    """
    Creates a FNN model for Connect4 move prediction with 3 hidden layers and two dropouts.
    """
    model = Sequential([
        Dense(128, activation='relu', input_shape=(input_shape,)),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(output_units, activation='softmax')
    ])

    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def train_model(X, y, epochs=20, batch_size=32):
    """
    Trains the supervised learning model
    """
    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

    # Create model
    model = create_connect4_model(input_shape=X.shape[1], output_units=7)  # 7 columns in Connect4

    # Train model
    history = model.fit(X_train, y_train,
                        epochs=epochs,
                        batch_size=batch_size,
                        validation_data=(X_val, y_val),
                        verbose=1)

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

def continue_training(model, X_new, y_new, epochs=10, batch_size=32):
    """
    Continues training an existing model with new data
    """
    # Split new data for validation
    X_train, X_val, y_train, y_val = train_test_split(X_new, y_new, test_size=0.2)

    # Continue training
    history = model.fit(X_train, y_train,
                        epochs=epochs,
                        batch_size=batch_size,
                        validation_data=(X_val, y_val),
                        verbose=1)
    return model, history
