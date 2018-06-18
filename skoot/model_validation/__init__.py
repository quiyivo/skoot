# -*- coding: utf-8 -*-
#
# Author: Taylor Smith <taylor.smith@alkaline-ml.com>

from sklearn.pipeline import Pipeline
from sklearn.externals import six
from collections import defaultdict

from ._validator import DistHypothesisValidator, CustomValidator

__all__ = ["make_validated_pipeline",
           "CustomValidator",
           "DistHypothesisValidator"]


def make_validated_pipeline(*steps, **kwargs):
    """Construct a pipeline from the given estimators, inserting validation
    steps between each.

    Create a sklearn Pipeline object with a ``DistHypothesisValidator`` class
    between each transformation. Note that each validator will be applied to
    all columns. In order to create a more intricate validation class, you can
    manually build a pipeline with specified columns, actions and varying
    alpha values. This is simply a convenience function and a shorthand for
    the Pipeline constructor; it does not require, and does not permit,
    naming the estimators. Instead, their names will be set to the lowercase
    of their types automatically.

    Parameters
    ----------
    *steps : list of estimators.

    **kwargs : keyword args or dict, optional
        Any keyword arguments to pass to the validation constructor(s).

    Examples
    --------
    >>> from sklearn.naive_bayes import GaussianNB
    >>> from sklearn.preprocessing import StandardScaler
    >>> make_validated_pipeline(StandardScaler(), GaussianNB(priors=None))
    ...     # doctest: +NORMALIZE_WHITESPACE
    Pipeline(steps=[('standardscaler',
                     StandardScaler(copy=True, with_mean=True, with_std=True)),
                    ('disthypothesisvalidator',
                     DistHypothesisValidator(action='warn', alpha=0.05,
                                             as_df=True,
                                             categorical_strategy='ratio',
                                             cols=None)),
                    ('gaussiannb', GaussianNB(priors=None))])
    """
    alpha = kwargs.pop("alpha", 0.05)
    action = kwargs.pop("action", "warn")
    if kwargs:
        raise TypeError("Unknown keyword arguments: '{}'"
                        .format(list(kwargs.keys())[0]))

    # Insert the validators between each layer
    estimators = []
    for step in steps:
        # First, append the step
        estimators.append(step)

        # Then determine whether to tack a validator on there.
        # We only do this for transformer output
        if hasattr(step, "transform"):
            estimators.append(DistHypothesisValidator(cols=None, alpha=alpha,
                                                      action=action))

    return Pipeline(_name_estimators(estimators))


def _name_estimators(estimators):
    """Generate names for estimators.

    NOTE: This is actually a method from sklearn.pipeline, but it is
    a private method and we cannot count on it to remain as-is, so we copied
    it here for static use.
    """
    names = [type(estimator).__name__.lower() for estimator in estimators]
    namecount = defaultdict(int)
    for est, name in zip(estimators, names):
        namecount[name] += 1

    for k, v in list(six.iteritems(namecount)):
        if v == 1:
            del namecount[k]

    for i in reversed(range(len(estimators))):
        name = names[i]
        if name in namecount:
            names[i] += "-%d" % namecount[name]
            namecount[name] -= 1

    return list(zip(names, estimators))