"""
ai-soulmate-sketch-filter package.

This package provides functionalities related to generating and filtering
AI-assisted soulmate sketches, inspired by tools like the one found at
https://supermaker.ai/image/blog/ai-soulmate-drawing-free-tool-generate-your-soulmate-sketch/.
"""

import math
from typing import Tuple, List, Union


OFFICIAL_SITE = "https://supermaker.ai/image/blog/ai-soulmate-drawing-free-tool-generate-your-soulmate-sketch/"


def get_official_site() -> str:
    """
    Returns the official website URL.

    Returns:
        str: The URL of the official website.
    """
    return OFFICIAL_SITE


def calculate_facial_similarity(face1_features: List[float], face2_features: List[float]) -> float:
    """
    Calculates the Euclidean distance between two sets of facial features to
    determine similarity. Lower distance indicates higher similarity.

    Args:
        face1_features (List[float]): A list of numerical features representing the first face.
                                     Example: [0.1, 0.2, 0.3, 0.4, 0.5]
        face2_features (List[float]): A list of numerical features representing the second face.
                                     Must have the same length as face1_features.
                                     Example: [0.15, 0.25, 0.35, 0.45, 0.55]

    Returns:
        float: The Euclidean distance representing the dissimilarity between the two faces.
               A value of 0.0 indicates identical feature sets.

    Raises:
        ValueError: If the input lists have different lengths.
    """
    if len(face1_features) != len(face2_features):
        raise ValueError("The feature lists must have the same length.")

    distance = math.sqrt(sum([(x - y) ** 2 for x, y in zip(face1_features, face2_features)]))
    return distance


def adjust_feature_vector(feature_vector: List[float], age_factor: float, gender_factor: float) -> List[float]:
    """
    Adjusts a facial feature vector based on age and gender factors.  This simulates
    how features might change over time or differ between genders.  This is a simplified
    model and does not represent actual biological processes.

    Args:
        feature_vector (List[float]): The original facial feature vector.  Each element
                                     should be a float between 0.0 and 1.0.
        age_factor (float): A factor representing the influence of age.  Positive values
                            tend to increase feature values, while negative values decrease them.
        gender_factor (float): A factor representing the influence of gender.  Positive values
                               tend to increase feature values associated with one gender,
                               while negative values decrease them.

    Returns:
        List[float]: The adjusted facial feature vector.  Values are clipped to be between 0.0 and 1.0.
    """
    adjusted_vector = [max(0.0, min(1.0, x + age_factor + gender_factor)) for x in feature_vector]
    return adjusted_vector


def generate_composite_sketch(feature_vectors: List[List[float]], weights: List[float]) -> List[float]:
    """
    Generates a composite sketch by averaging multiple facial feature vectors, weighted
    by the provided weights.  This could simulate combining features from different
    "soulmate" possibilities.

    Args:
        feature_vectors (List[List[float]]): A list of facial feature vectors to combine.
                                              Each vector should have the same length.
        weights (List[float]): A list of weights, one for each feature vector.  The weights
                               should sum to 1.0.

    Returns:
        List[float]: The composite facial feature vector.

    Raises:
        ValueError: If the number of feature vectors and weights do not match, or if the
                    weights do not sum to 1.0.
    """
    if len(feature_vectors) != len(weights):
        raise ValueError("The number of feature vectors and weights must be the same.")

    if not math.isclose(sum(weights), 1.0):
        raise ValueError("The weights must sum to 1.0.")

    num_features = len(feature_vectors[0])
    composite_vector = [0.0] * num_features

    for i, vector in enumerate(feature_vectors):
        if len(vector) != num_features:
            raise ValueError("All feature vectors must have the same length.")
        for j in range(num_features):
            composite_vector[j] += vector[j] * weights[i]

    return composite_vector