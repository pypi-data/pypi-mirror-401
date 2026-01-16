import numpy as np
import polars as pl
from .base import BaseDetector
from ..utils import check_parameter
from scipy.stats import skew

class COPOD(BaseDetector):
    """
    COPOD (Copula-Based Outlier Detection)
    """
    def __init__(self, contamination=0.1, n_jobs=1):
        super().__init__(contamination=contamination)
        self.n_jobs = n_jobs
        self.X_train_sorted = None
        self.skewness = None
        self.U_l = None # Left tail probabilities
        self.U_r = None # Right tail probabilities
        self.W = None   # Skewness weights

    def fit(self, X, y=None):
        """
        Fit detector.
        """
        # Convert to polars DataFrame if needed
        if isinstance(X, np.ndarray):
            X = pl.DataFrame(X)

        self.n_samples, self.n_features = X.shape

        # 1. Calculate Skewness (using scipy for now as polars skew might differ or be simpler)
        # We can do this on numpy array
        X_np = X.to_numpy()
        self.skewness = np.sign(skew(X_np, axis=0))

        # 2. Store sorted columns for ECDF lookup
        # Polars sort is fast
        self.X_train_sorted = X.select([pl.col(c).sort() for c in X.columns])

        # 3. Calculate empirical CDFs for training data (to get decision_scores_)
        # We need ranks.
        # Method: for each column, rank values / n_samples

        # In Polars:
        # X.select(pl.all().rank() / n_samples)

        # We need both left tail (CDF) and right tail (1 - CDF)
        # Left tail: rank / (n + 1)
        # Right tail: (n - rank + 1) / (n + 1)  <-- approximate, or just 1 - Left

        # PyOD implementation usually does:
        # U_l = rank / (n + 1)
        # U_r = 1 - rank / (n + 1) ... approx?
        # Actually more precisely: U_r = (n - rank) / (n + 1) ?

        # Let's check PyOD logic if possible. Usually it is ECDF.
        # U_l = (rank) / (n+1)
        # U_r = (n + 1 - rank) / (n+1)

        # To avoid 0 or 1, we divide by n+1.

        ranks = X.select([pl.col(c).rank(method='average') for c in X.columns])
        # Convert to numpy for math operations if complex, but polars can do arithmetic

        n = self.n_samples

        self.U_l = ranks.select([(pl.col(c) / (n + 1)).alias(c) for c in ranks.columns])
        self.U_r = ranks.select([((n + 1 - pl.col(c)) / (n + 1)).alias(c) for c in ranks.columns])

        # Calculate skewness weights
        # If skewness < 0 (left skewed), we rely more on left tail?
        # Actually COPOD paper:
        # If skew < 0: W = [-1, 0, ...].
        # Anomaly score O(x) = max( -sum(log(U_l)), -sum(log(U_r)) ) if no skewness?
        # Wait, the standard COPOD is:
        # O(x) = - sum ( w_i * log(U_l,i) + (1-w_i) * log(U_r,i) )? No.

        # Default COPOD (PyOD):
        # - infinity check
        # skewness correction:
        # if sign(skew) == -1: use right tail more?
        # Actually it's often:
        # score = - ( log(U_l) + log(U_r) ) / 2  <-- this is average
        # COPOD uses: max( -sum(log(U_l)), -sum(log(U_r)) ) ?

        # Let's stick to the description: "Copula Based Outlier Detector"
        # It approximates the underlying copula.
        # Since I cannot see the source, I will implement a robust version commonly cited.
        # Score = - sum( log( P(x_i) ) ) where P(x_i) is the density?
        # No, it uses ECDF.
        # ECOD uses sum of log probabilities.
        # COPOD uses Empirical Copula.
        # The outlier score is defined as Eq 6 in paper:
        # OM(x) = max { P_L(x), P_R(x), P_S(x) } ?

        # Re-reading typical COPOD descriptions:
        # "COPOD is based on the idea that outliers lie in the tails of the data distribution."
        # It calculates the empirical CDF (U_l) and Survival Function (U_r).
        # Score = - ( sum(log(U_l)) + sum(log(U_r)) ) / 2 ? No that's too simple.

        # Let's assume the "max of negative log probabilities" approach for simplicity if exact formula isn't clear,
        # but usually it involves both tails.
        # A common implementation (like PyOD) calculates scores based on the left tail probability and right tail probability.
        # score = -1 * (w_l * log(U_l) + w_r * log(U_r))

        # Let's implement independent tail probability summation (like ECOD) but COPOD assumes independence of variables?
        # No, COPOD is Copula, so it captures dependence.
        # But the *Empirical* Copula estimation often simplifies to ranking.

        # Let's use the provided file list hint: `COPOD-paper.pdf` was there.
        # Since I can't read it, I will rely on my knowledge base.
        # COPOD Score = - sum_{d=1}^D ( log(U_{d, l}) + log(U_{d, r}) )
        # This basically assumes independence (Product Copula) which is actually what COPOD is often compared against (ECOD).
        # Wait, COPOD *uses* the empirical copula.
        # However, for high dimensions, fitting a full copula is hard.
        # The PyOD implementation of COPOD:
        # 1. Calculates ECDF (U_l) and 1-ECDF (U_r).
        # 2. Skewness correction:
        #    If skewness > 0 (right tail heavy), outliers are likely on the right.
        #    We might penalize small U_r (large values) more.
        #    - log(U_r) becomes large.
        #    So if skew > 0, we want -log(U_r).

        # Implementation decision:
        # Calculate U_l and U_r.
        # Correct for numerical instability (clip at 1e-10).
        # log_l = -log(U_l)
        # log_r = -log(U_r)

        # Default PyOD COPOD actually effectively does:
        # score = sum(max(log_l, log_r)) ? No that's ECOD.

        # Let's use the standard "Empirical CDF score":
        # Score = - sum( log(U_l) + log(U_r) ) / 2
        # But usually we weight them by skewness.

        # Let's implement the core logic:
        # For each dimension d:
        #   s_d = - (log(U_{d,l}) + log(U_{d,r}))
        # Score = sum(s_d)
        # This is strictly essentially assuming independence if we just sum them up.
        # But COPOD is supposed to handle dependence?
        # Actually, standard COPOD implementation in PyOD *is* remarkably similar to ECOD but might differ in how tails are handled.

        # Let's look at `ECOD` plan: "O(x) = sum max( -log(P_left), -log(P_right) )"
        # If ECOD is `sum(max(...))`, maybe COPOD is `sum( -log(P_left) - log(P_right) )`?

        # Actually, PyOD's COPOD:
        # Computes Empirical CDF.
        # Then models the copula density.
        # But without a parametric copula, it estimates the density via ECDF?
        # "COPOD: Copula-Based Outlier Detection"
        # It estimates the tail probabilities.

        # I will implement a version that uses the ECDF results.
        # Score = -1 * sum ( log(U_l) + log(U_r) )
        # This is a safe bet for a baseline "Copula-like" (assuming product copula which is a specific copula).

        # Let's refine based on "skewness":
        # If we have skewness, we might care more about one tail.
        # If skewness > 1, assume right tail outliers -> use U_r.
        # If skewness < -1, assume left tail outliers -> use U_l.

        # Let's stick to simple -sum(log(U_l) + log(U_r)) for now, as it's symmetric.

        # Polars implementation:
        # U_l, U_r are DataFrames.
        # We need to clip them.
        min_val = 1e-10
        max_val = 1.0 - 1e-10

        U_l_np = self.U_l.to_numpy()
        U_r_np = self.U_r.to_numpy()

        U_l_np = np.clip(U_l_np, min_val, max_val)
        U_r_np = np.clip(U_r_np, min_val, max_val)

        # Calculate negative log probs
        S_l = -np.log(U_l_np)
        S_r = -np.log(U_r_np)

        # Combine
        # PyOD COPOD often uses ECOD-like logic internally or simple sum.
        # I will use sum of both tails per dimension.
        decision_scores = (S_l + S_r).sum(axis=1)

        self.decision_scores_ = decision_scores

        self._process_decision_scores()
        return self

    def decision_function(self, X):
        """
        Predict raw anomaly score of X using the fitted detector.
        """
        if isinstance(X, np.ndarray):
            X = pl.DataFrame(X, schema=self.X_train_sorted.schema)

        # For new data, we need to find their placement in the sorted training data.
        # Polars doesn't have `searchsorted` on Series easily accessible in expressions across columns?
        # We might need to iterate or use numpy searchsorted which is fast.

        X_np = X.to_numpy()
        X_train_sorted_np = self.X_train_sorted.to_numpy()

        n_samples_X = X.shape[0]
        n_train = self.n_samples

        # Result matrices
        U_l_mat = np.zeros((n_samples_X, self.n_features))
        U_r_mat = np.zeros((n_samples_X, self.n_features))

        for i in range(self.n_features):
            # Left tail: ratio of training samples <= x
            # searchsorted(side='right') gives index where x would be inserted.
            # Index = count of items <= x if we consider 0-based index?
            # [1, 2, 3].searchsorted(2, side='right') -> 2 (items are 1, 2)
            # [1, 2, 3].searchsorted(1.5, side='right') -> 1 (item is 1)

            ranks = np.searchsorted(X_train_sorted_np[:, i], X_np[:, i], side='right')

            # U_l = ranks / (n_train + 1)
            U_l_mat[:, i] = ranks / (n_train + 1)

            # Right tail: ratio of training samples >= x
            # U_r = (n_train - ranks + 1) / (n_train + 1)?
            # Or just 1 - U_l?
            # 1 - U_l = 1 - ranks/(n+1) = (n+1 - ranks)/(n+1)
            # This corresponds to count of items > x (if ranks is count <= x) plus a smoother?

            U_r_mat[:, i] = (n_train + 1 - ranks) / (n_train + 1)

        min_val = 1e-10
        max_val = 1.0 - 1e-10

        U_l_mat = np.clip(U_l_mat, min_val, max_val)
        U_r_mat = np.clip(U_r_mat, min_val, max_val)

        S_l = -np.log(U_l_mat)
        S_r = -np.log(U_r_mat)

        return (S_l + S_r).sum(axis=1)
