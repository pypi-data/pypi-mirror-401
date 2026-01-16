import polars as pl
import numpy as np

def check_parameter(param, low, high, param_name='parameter', include_left=False, include_right=False):
    """
    Check if value is between low and high.
    """
    if include_left and include_right:
        if not (low <= param <= high):
            raise ValueError(f"{param_name} must be in [{low}, {high}]. Got {param}")
    elif include_left:
        if not (low <= param < high):
            raise ValueError(f"{param_name} must be in [{low}, {high}). Got {param}")
    elif include_right:
        if not (low < param <= high):
            raise ValueError(f"{param_name} must be in ({low}, {high}]. Got {param}")
    else:
        if not (low < param < high):
            raise ValueError(f"{param_name} must be in ({low}, {high}). Got {param}")
    return True

def get_ecdf(X):
    """
    Calculate the empirical CDF of X.
    X should be a Polars DataFrame.
    Returns a dictionary or similar structure where each key is a column name
    and the value is the sorted values of that column (for ECOD/COPOD lookup).

    Actually, for COPOD/ECOD, we often need the tail probabilities.
    Standard implementation:
    1. Sort each dimension.
    2. Use `searchsorted` to find ranks of new data.

    This function will return the sorted columns as a new DataFrame or dict of arrays.
    """
    if isinstance(X, np.ndarray):
        X = pl.DataFrame(X)

    return X.select([pl.col(c).sort() for c in X.columns])
