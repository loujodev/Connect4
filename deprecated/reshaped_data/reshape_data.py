"""
Initially it was planned to train a FFN. That is why the games were recorded
in a 1D array which is not optimal for training a CNN.
This class reshapes the old data into a 2D format to make enable spatial awareness when training the CNN.
"""

import numpy as np


def convert_flattened_to_2d(input_path, output_path, rows=6, cols=7):

    data = np.load(input_path)
    X = data['X']
    y = data['y']

    X_reshaped = X.reshape(-1, rows, cols, 1)

    np.savez(output_path, X=X_reshaped, y=y)
    print(f"Successfully converted data to: {output_path}")




convert_flattened_to_2d(
    input_path='/deprecated/datasets/30000games_win_block.npz',
    output_path='/deprecated/reshaped_data/30000games_win_block.npz',
)