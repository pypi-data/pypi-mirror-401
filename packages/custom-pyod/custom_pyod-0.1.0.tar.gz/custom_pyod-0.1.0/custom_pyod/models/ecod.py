import numpy as np
import polars as pl
from .base import BaseDetector
from ..utils import check_parameter

class ECOD(BaseDetector):
    """
    ECOD (Empirical Cumulative Distribution Functions Based Outlier Detection)
    """
    def __init__(self, contamination=0.1, n_jobs=1):
        super().__init__(contamination=contamination)
        self.n_jobs = n_jobs
        self.X_train_sorted = None

    def fit(self, X, y=None):
        """
        Fit detector.
        """
        # Convert to polars DataFrame if needed
        if isinstance(X, np.ndarray):
            X = pl.DataFrame(X)

        self.n_samples, self.n_features = X.shape

        # 1. Store sorted columns for ECDF lookup
        self.X_train_sorted = X.select([pl.col(c).sort() for c in X.columns])

        # 2. Calculate scores for training data
        # For training data, ranks are just 1..n

        n = self.n_samples

        # We need ranks for each column
        ranks = X.select([pl.col(c).rank(method='average') for c in X.columns])

        # Convert to numpy for calculation
        # ECOD formula: score = sum ( max(-log(U_l), -log(U_r)) )

        # U_l = rank / (n + 1)
        # U_r = (n + 1 - rank) / (n + 1)

        ranks_np = ranks.to_numpy()

        U_l_mat = ranks_np / (n + 1)
        U_r_mat = (n + 1 - ranks_np) / (n + 1)

        # Clip
        min_val = 1e-10
        max_val = 1.0 - 1e-10
        U_l_mat = np.clip(U_l_mat, min_val, max_val)
        U_r_mat = np.clip(U_r_mat, min_val, max_val)

        S_l = -np.log(U_l_mat)
        S_r = -np.log(U_r_mat)

        # Element-wise max, then sum across features
        self.decision_scores_ = np.maximum(S_l, S_r).sum(axis=1)

        self._process_decision_scores()
        return self

    def decision_function(self, X):
        """
        Predict raw anomaly score of X using the fitted detector.
        """
        if isinstance(X, np.ndarray):
            X = pl.DataFrame(X, schema=self.X_train_sorted.schema)

        X_np = X.to_numpy()
        X_train_sorted_np = self.X_train_sorted.to_numpy()

        n_samples_X = X.shape[0]
        n_train = self.n_samples

        U_l_mat = np.zeros((n_samples_X, self.n_features))
        U_r_mat = np.zeros((n_samples_X, self.n_features))

        for i in range(self.n_features):
            # Left tail: ratio of training samples <= x
            ranks = np.searchsorted(X_train_sorted_np[:, i], X_np[:, i], side='right')

            U_l_mat[:, i] = ranks / (n_train + 1)
            U_r_mat[:, i] = (n_train + 1 - ranks) / (n_train + 1)

        min_val = 1e-10
        max_val = 1.0 - 1e-10

        U_l_mat = np.clip(U_l_mat, min_val, max_val)
        U_r_mat = np.clip(U_r_mat, min_val, max_val)

        S_l = -np.log(U_l_mat)
        S_r = -np.log(U_r_mat)

        return np.maximum(S_l, S_r).sum(axis=1)
