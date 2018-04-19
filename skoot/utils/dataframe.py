# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pandas as pd
import numpy as np

__all__ = [
    'get_numeric_columns',
    'safe_drop_samples',
    'safe_mask_samples',
    'safe_vstack'
]


def get_numeric_columns(X):
    """Get all numeric columns from a pandas DataFrame.

    This function selects all numeric columns from a pandas
    DataFrame. A numeric column is defined as a column whose
    ``dtype`` is a ``np.number``.

    Parameters
    ----------
    X : pd.DataFrame
        The input dataframe.
    """
    return X.select_dtypes(include=[np.number])


def safe_drop_samples(X, drop_samples):
    """Drop samples (rows) from a matrix.

    Drop observations from a np.ndarray or pd.DataFrame. This
    produces a copy of data without the samples.

    Parameters
    ----------
    X : array-like, shape=(n_samples, n_features)
        The array from which to drop records.

    drop_samples : array-like, shape=(n_samples,)
        The indices to drop.
    """
    if isinstance(X, pd.DataFrame):
        return X.drop(drop_samples, axis=0)
    else:
        return np.delete(X, drop_samples, axis=0)


def safe_mask_samples(X, mask):
    """Select samples (rows) from a matrix from a mask.

    Select observations from a np.ndarray or pd.DataFrame by using
    a mask. This creates a copy of X, and allows us to use ``iloc``
    with a mask even though not natively supported by Pandas.

    Parameters
    ----------
    X : array-like, shape=(n_samples, n_features)
        The array from which to drop records.

    mask : array-like, shape=(n_samples,)
        The boolean mask.
    """
    mask = np.asarray(mask)
    if isinstance(X, pd.DataFrame):
        return X.iloc[X.index[mask]]
    else:
        return X[mask, :]


def safe_vstack(a, b):
    """Stack two arrays on top of one another.

    Safely handle vertical stacking of arrays. This works for
    either np.ndarrays or pd.DataFrames.

    Parameters
    ----------
    a : array-like, shape=(n_samples, n_features)
        The array that will be stacked on the top vertically.

    b : array-like, shape=(n_samples, n_features)
        The array that will be stacked below the other vertically.
    """
    # we can only pd.concat if they BOTH are DataFrames
    if all(isinstance(x, pd.DataFrame) for x in (a, b)):
        return pd.concat([a, b], axis=0)

    # otherwise, at least one of them is a numpy array (we think)
    return np.vstack([a, b])
