import unittest
import numpy as np
import polars as pl
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from custom_pyod.models.copod import COPOD
from custom_pyod.models.ecod import ECOD

class TestModels(unittest.TestCase):
    def setUp(self):
        self.n_train = 200
        self.n_test = 100
        self.n_features = 5
        self.contamination = 0.1

        # Generate data
        X, y = make_blobs(n_samples=self.n_train + self.n_test, centers=1, n_features=self.n_features, random_state=42)

        # Add outliers
        n_outliers = int((self.n_train + self.n_test) * self.contamination)
        rng = np.random.RandomState(42)
        outliers = rng.uniform(low=-10, high=10, size=(n_outliers, self.n_features))

        # X with outliers
        self.X = np.vstack([X[:-n_outliers], outliers])
        self.y = np.hstack([np.zeros(len(X) - n_outliers), np.ones(n_outliers)])

        # Split
        self.X_train = self.X[:self.n_train]
        self.X_test = self.X[self.n_train:]
        self.y_train = self.y[:self.n_train]
        self.y_test = self.y[self.n_train:]

        # Polars version
        self.X_train_pl = pl.DataFrame(self.X_train)
        self.X_test_pl = pl.DataFrame(self.X_test)

    def test_copod_fit_predict(self):
        clf = COPOD(contamination=self.contamination)
        clf.fit(self.X_train_pl)

        # Check fitted attributes
        self.assertIsNotNone(clf.threshold_)
        self.assertIsNotNone(clf.decision_scores_)

        # Predict
        pred_labels = clf.predict(self.X_test_pl)
        pred_scores = clf.decision_function(self.X_test_pl)

        self.assertEqual(len(pred_labels), self.n_test)
        self.assertEqual(len(pred_scores), self.n_test)

        # Check basic performance (ROC AUC roughly)
        # Or simply check if outliers have higher scores
        # We know the last few samples in X_test might be outliers if indices preserved?
        # Actually random split logic above wasn't perfect shuffle but appended outliers at end.
        # But we sliced.
        # Let's just check shape and type.
        self.assertIsInstance(pred_labels, np.ndarray)
        self.assertIsInstance(pred_scores, np.ndarray)

    def test_ecod_fit_predict(self):
        clf = ECOD(contamination=self.contamination)
        clf.fit(self.X_train_pl)

        self.assertIsNotNone(clf.threshold_)
        self.assertIsNotNone(clf.decision_scores_)

        pred_labels = clf.predict(self.X_test_pl)
        pred_scores = clf.decision_function(self.X_test_pl)

        self.assertEqual(len(pred_labels), self.n_test)
        self.assertEqual(len(pred_scores), self.n_test)

    def test_sklearn_pipeline_compatibility(self):
        # Test pipeline
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', COPOD(contamination=self.contamination))
        ])

        pipeline.fit(self.X_train) # Input numpy to pipeline
        preds = pipeline.predict(self.X_test)

        self.assertEqual(len(preds), self.n_test)

        pipeline_ecod = Pipeline([
            ('scaler', StandardScaler()),
            ('model', ECOD(contamination=self.contamination))
        ])
        pipeline_ecod.fit(self.X_train)
        preds_ecod = pipeline_ecod.predict(self.X_test)
        self.assertEqual(len(preds_ecod), self.n_test)

if __name__ == '__main__':
    unittest.main()
