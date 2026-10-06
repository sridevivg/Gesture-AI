"""Model evaluation and metrics generation."""

from typing import Any, Dict
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix


def evaluate_classifier(
    model: Any, X_test: np.ndarray, y_test: np.ndarray
) -> Dict[str, Any]:
    """Compute precision, recall, f1-score, and confusion matrix."""
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    conf_mat = confusion_matrix(y_test, y_pred).tolist()

    return {
        "classification_report": report,
        "confusion_matrix": conf_mat,
    }
