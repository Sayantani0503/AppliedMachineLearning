from typing import Tuple

def score(text: str, model, threshold: float) -> Tuple[bool, float]:

    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")
    if not hasattr(model, 'predict_proba'):
        raise ValueError("Model must have a 'predict_proba' method.")
    if not isinstance(threshold, (int, float)) or not (0 <= threshold <= 1):
        raise ValueError("Threshold must be a float between 0 and 1.")

    propensity = model.predict_proba([text])[0][1]  # Assuming binary classification
    prediction = bool(propensity >= threshold)

    return prediction, propensity