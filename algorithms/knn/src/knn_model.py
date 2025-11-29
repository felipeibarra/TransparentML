"""
K-Nearest Neighbors (KNN) Classifier
=====================================
Pure NumPy implementation from scratch.

Author: TransparentML Team
Version: 1.0.0
License: MIT
"""

import numpy as np
from typing import Optional, Tuple, List
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KNNClassifier:
    """
    K-Nearest Neighbors classifier implementation.
    
    Parameters
    ----------
    k : int, default=5
        Number of neighbors to consider
    distance_metric : str, default='euclidean'
        Distance metric to use ('euclidean', 'manhattan', 'minkowski')
    weights : str, default='uniform'
        Weight function ('uniform' or 'distance')
    p : int, default=2
        Power parameter for Minkowski metric
        
    Attributes
    ----------
    X_train : ndarray of shape (n_samples, n_features)
        Training data
    y_train : ndarray of shape (n_samples,)
        Training labels
    classes_ : ndarray
        Unique classes in training data
    """
    
    def __init__(
        self, 
        k: int = 5,
        distance_metric: str = 'euclidean',
        weights: str = 'uniform',
        p: int = 2
    ):
        self.k = k
        self.distance_metric = distance_metric
        self.weights = weights
        self.p = p
        self.X_train = None
        self.y_train = None
        self.classes_ = None
        
        logger.info(f"Initialized KNN with k={k}, metric={distance_metric}, weights={weights}")
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'KNNClassifier':
        """
        Fit the KNN classifier.
        
        In KNN, fitting just stores the training data.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data
        y : array-like of shape (n_samples,)
            Target labels
            
        Returns
        -------
        self : KNNClassifier
            Fitted classifier
        """
        self.X_train = np.array(X)
        self.y_train = np.array(y)
        self.classes_ = np.unique(y)
        
        logger.info(f"Fitted KNN with {len(X)} samples, {X.shape[1]} features, {len(self.classes_)} classes")
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels for samples in X.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples
            
        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predicted class labels
        """
        X = np.array(X)
        predictions = np.array([self._predict_single(x) for x in X])
        
        logger.info(f"Predicted {len(predictions)} samples")
        
        return predictions
    
    def _predict_single(self, x: np.ndarray) -> int:
        """Predict class for a single sample."""
        # Calculate distances to all training samples
        distances = self._calculate_distances(x)
        
        # Get k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = self.y_train[k_indices]
        k_nearest_distances = distances[k_indices]
        
        # Vote based on weights
        if self.weights == 'uniform':
            # Simple majority vote
            most_common = Counter(k_nearest_labels).most_common(1)
            return most_common[0][0]
        else:  # distance-weighted
            # Weight by inverse distance
            weights = 1 / (k_nearest_distances + 1e-10)
            weighted_votes = {}
            
            for label, weight in zip(k_nearest_labels, weights):
                weighted_votes[label] = weighted_votes.get(label, 0) + weight
            
            return max(weighted_votes, key=weighted_votes.get)
    
    def _calculate_distances(self, x: np.ndarray) -> np.ndarray:
        """
        Calculate distances from x to all training samples.
        
        Parameters
        ----------
        x : array of shape (n_features,)
            Query point
            
        Returns
        -------
        distances : array of shape (n_samples,)
            Distances to all training samples
        """
        if self.distance_metric == 'euclidean':
            return np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
        
        elif self.distance_metric == 'manhattan':
            return np.sum(np.abs(self.X_train - x), axis=1)
        
        elif self.distance_metric == 'minkowski':
            return np.power(np.sum(np.abs(self.X_train - x) ** self.p, axis=1), 1/self.p)
        
        else:
            raise ValueError(f"Unknown distance metric: {self.distance_metric}")
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities for samples in X.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples
            
        Returns
        -------
        proba : ndarray of shape (n_samples, n_classes)
            Class probabilities for each sample
        """
        X = np.array(X)
        probas = np.array([self._predict_proba_single(x) for x in X])
        
        return probas
    
    def _predict_proba_single(self, x: np.ndarray) -> np.ndarray:
        """Predict class probabilities for a single sample."""
        # Calculate distances
        distances = self._calculate_distances(x)
        
        # Get k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = self.y_train[k_indices]
        k_nearest_distances = distances[k_indices]
        
        # Calculate probabilities
        proba = np.zeros(len(self.classes_))
        
        if self.weights == 'uniform':
            # Count votes for each class
            for label in k_nearest_labels:
                class_idx = np.where(self.classes_ == label)[0][0]
                proba[class_idx] += 1
            proba /= self.k
        else:  # distance-weighted
            # Weight by inverse distance
            weights = 1 / (k_nearest_distances + 1e-10)
            for label, weight in zip(k_nearest_labels, weights):
                class_idx = np.where(self.classes_ == label)[0][0]
                proba[class_idx] += weight
            proba /= proba.sum()
        
        return proba
    
    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate accuracy score.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples
        y : array-like of shape (n_samples,)
            True labels
            
        Returns
        -------
        score : float
            Accuracy score
        """
        predictions = self.predict(X)
        accuracy = np.mean(predictions == y)
        
        logger.info(f"Accuracy: {accuracy:.4f}")
        
        return accuracy
    
    def get_params(self) -> dict:
        """Get parameters of the model."""
        return {
            'k': self.k,
            'distance_metric': self.distance_metric,
            'weights': self.weights,
            'p': self.p
        }
    
    def set_params(self, **params) -> 'KNNClassifier':
        """Set parameters of the model."""
        for key, value in params.items():
            setattr(self, key, value)
        return self


class KNNRegressor:
    """
    K-Nearest Neighbors regressor implementation.
    
    Parameters
    ----------
    k : int, default=5
        Number of neighbors to consider
    distance_metric : str, default='euclidean'
        Distance metric to use
    weights : str, default='uniform'
        Weight function ('uniform' or 'distance')
    """
    
    def __init__(
        self,
        k: int = 5,
        distance_metric: str = 'euclidean',
        weights: str = 'uniform'
    ):
        self.k = k
        self.distance_metric = distance_metric
        self.weights = weights
        self.X_train = None
        self.y_train = None
        
        logger.info(f"Initialized KNN Regressor with k={k}")
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> 'KNNRegressor':
        """Fit the KNN regressor."""
        self.X_train = np.array(X)
        self.y_train = np.array(y)
        
        logger.info(f"Fitted KNN Regressor with {len(X)} samples")
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict values for samples in X."""
        X = np.array(X)
        predictions = np.array([self._predict_single(x) for x in X])
        
        return predictions
    
    def _predict_single(self, x: np.ndarray) -> float:
        """Predict value for a single sample."""
        # Calculate distances
        if self.distance_metric == 'euclidean':
            distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
        else:
            distances = np.sum(np.abs(self.X_train - x), axis=1)
        
        # Get k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_values = self.y_train[k_indices]
        
        if self.weights == 'uniform':
            return np.mean(k_nearest_values)
        else:  # distance-weighted
            k_nearest_distances = distances[k_indices]
            weights = 1 / (k_nearest_distances + 1e-10)
            return np.average(k_nearest_values, weights=weights)
    
    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Calculate R² score."""
        predictions = self.predict(X)
        ss_res = np.sum((y - predictions) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        
        logger.info(f"R² Score: {r2:.4f}")
        
        return r2


if __name__ == "__main__":
    # Test with Iris dataset
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    
    # Load data
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Train
    knn = KNNClassifier(k=5)
    knn.fit(X_train, y_train)
    
    # Evaluate
    train_score = knn.score(X_train, y_train)
    test_score = knn.score(X_test, y_test)
    
    print(f"\nKNN Classifier Results:")
    print(f"Train Accuracy: {train_score:.4f}")
    print(f"Test Accuracy: {test_score:.4f}")
    
    # Test probabilities
    probas = knn.predict_proba(X_test[:5])
    print(f"\nProbabilities for first 5 samples:")
    print(probas)
