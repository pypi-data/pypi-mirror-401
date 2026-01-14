import numpy as np


def pad_parameters(dataset, missing_params=[], desired_params=None, axis=-1):
    """
    Pads columns with NaNs in desired places. If `desired_params` is None, padded columns are
    appended at the end.
    
    Parameters
    ----------
    dataset: array
        Dataset to be padded.
    axis: int
        Axis along which to add padded columns.
    missing_params: list
        A list of parameter names present in `desired_params`, but for which entries are missing
        from `dataset`.
    desired_params: list
        A list of all desired parameter names, both present and missing.

    Returns
    -------
    padded_dataset: array
        Dataset with colomns padded.
    """
    padded_dataset = np.copy(dataset)
    
    if desired_params is None:
        idx = [dataset.shape[axis]+i for i in range(len(missing_params))]
    else:
        if dataset.shape[axis] + len(missing_params) < len(desired_params):
            raise Exception('not enough missing parameters given')
        if dataset.shape[axis] + len(missing_params) > len(desired_params):
            raise Exception('too many missing parameters given')
        idx = np.argwhere(np.in1d(desired_params, missing_params)).flatten()
    
    for i in idx:
        padded_dataset = np.insert(padded_dataset, i, np.nan, axis=axis)
    return padded_dataset


def gen_credible_interval(dataset, interval=0.9, pm_format=True):
    """
    Wrapper for numpy.quantile that generates median and credible intervalse.

    Parameters
    ----------
    dataset: array
        Dataset to generate credible intervals from.
    interval: float, optional
        Credible interval to compute (e.g., interval=0.9 returns 90% credible intervals).
    pm_format: bool, optional
        Whether to use median (+/-) formatting, or median (lower/higher-bound) formatting.

    Returns
    -------
    median: float or array
        Median of dataset.
    lower or minus:
        Lower bound of credible interval or, if `pm_format=True`, difference between lower bound
        and median.
    upper or plus:
        Upper bound of credible interval or, if `pm_format=True`, difference between upper bound
        and median.
    """
    lower, median, upper = np.quantile(
        dataset,
        q=(0.5*(1. - interval), 0.5, 0.5*(1. + interval))
    )
    if pm_format:
        minus = median - lower
        plus = upper - median
        return median, plus, minus
    return median, upper, lower
