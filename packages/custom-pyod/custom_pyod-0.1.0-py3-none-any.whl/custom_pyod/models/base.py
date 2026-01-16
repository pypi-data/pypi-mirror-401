import numpy as np
import polars as pl
from sklearn.base import BaseEstimator, OutlierMixin
from sklearn.utils.validation import check_is_fitted
from abc import ABC, abstractmethod

class BaseDetector(BaseEstimator, OutlierMixin, ABC):
    """
    Base class for all outlier detection algorithms in custom_pyod.
    Inherits from sklearn BaseEstimator and OutlierMixin.
    """

    def __init__(self, contamination=0.1):
        if not (0. < contamination <= 0.5):
            raise ValueError("contamination must be in (0, 0.5], got: %f" % contamination)
        self.contamination = contamination
        self.offset_ = None
        self.threshold_ = None
        self.decision_scores_ = None
        self.labels_ = None

    @abstractmethod
    def fit(self, X, y=None):
        """
        Fit detector.
        """
        pass

    @abstractmethod
    def decision_function(self, X):
        """
        Predict raw anomaly score of X using the fitted detector.
        """
        pass

    def predict(self, X):
        """
        Predict if a particular sample is an outlier or not.

        Parameters
        ----------
        X : polars.DataFrame or numpy.ndarray
            The input samples.

        Returns
        -------
        outlier_labels : numpy.ndarray
            0 for inliers, 1 for outliers.
        """
        check_is_fitted(self, ['threshold_', 'offset_'])
        scores = self.decision_function(X)
        if isinstance(scores, pl.DataFrame) or isinstance(scores, pl.Series):
            scores = scores.to_numpy().ravel()
        return (scores > self.threshold_).astype(int)

    def fit_predict(self, X, y=None):
        """
        Fit detector and predict on X.
        """
        self.fit(X, y)
        return self.labels_

    def _process_decision_scores(self):
        """
        Internal function to calculate threshold_ and labels_ based on decision_scores_.
        Should be called at the end of fit().
        """
        if self.decision_scores_ is None:
            raise ValueError("decision_scores_ is not set.")

        # Determine threshold
        # We use numpy for quantile calculation for simplicity as decision_scores_ might be numpy or polars
        scores = self.decision_scores_
        if isinstance(scores, pl.Series):
            scores = scores.to_numpy()

        self.threshold_ = np.percentile(scores, 100 * (1 - self.contamination))
        self.offset_ = -self.threshold_

        self.labels_ = (scores > self.threshold_).astype(int)
        return self
