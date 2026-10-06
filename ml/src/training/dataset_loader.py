"""Dataset loading and preprocessing utilities for gesture datasets."""

import os
from typing import Optional, Tuple
import numpy as np
import pandas as pd
from ml.src.config import ml_settings


class GestureDatasetLoader:
    """Loads landmark CSV or NumPy dataset files for training."""

    def __init__(self, datasets_dir: Optional[str] = None):
        self.datasets_dir = datasets_dir or ml_settings.DATASETS_DIR

    def load_csv(self, filename: str) -> Tuple[np.ndarray, np.ndarray]:
        """Load feature matrix X and label vector y from CSV file."""
        file_path = os.path.join(self.datasets_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset file not found: {file_path}")

        df = pd.read_csv(file_path)
        # Assuming last column is the label
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        return X, y

    def save_landmarks_to_csv(
        self,
        features: np.ndarray,
        labels: np.ndarray,
        output_filename: str,
    ) -> str:
        """Export collected landmarks to CSV."""
        os.makedirs(self.datasets_dir, exist_ok=True)
        out_path = os.path.join(self.datasets_dir, output_filename)
        data = np.hstack((features, labels.reshape(-1, 1)))
        pd.DataFrame(data).to_csv(out_path, index=False)
        return out_path
