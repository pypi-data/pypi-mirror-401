import logging
from numbers import Number

import numpy as np

from culib.utils.logs import get_local_logger

ACCEPTED_INT_TYPES = (int, np.int32, np.int64)
ACCEPTED_NUM_TYPES = (Number,)


def validate_num_param(
    param: ACCEPTED_NUM_TYPES,
    param_name: str,
    param_long_name: str = "",
    log: logging.Logger = None,
) -> ACCEPTED_NUM_TYPES:
    """
    Check if param is a valid numeric value and returns it if OK.
    Raises error otherwise.

    Parameters
    ----------
    param
        Value to check
    param_name
        For logging purposes
    param_long_name
        For logging purpose
    log
        For logging purposes

    Returns
    -------
    param
        param if valid

    Raises
    -------
    TypeError
        If param is not numeric

    Examples
    --------
    >>> validate_num_param(12.69, "param", "awesome param")
    12.69

    """
    # Apply check
    if isinstance(param, ACCEPTED_NUM_TYPES):
        return param
    else:
        if param_long_name == "":
            param_long_name = param_name
        if log is None:
            log = get_local_logger("validate_num_param")
        err_msg = f"{param_long_name} specified is not numeric. Accepted types are {ACCEPTED_NUM_TYPES}. Got {param_name}={param}"
        log.error(err_msg)
        raise TypeError(err_msg)


def validate_positive_num_param(
    param: ACCEPTED_NUM_TYPES,
    param_name: str,
    param_long_name: str = "",
    log: logging.Logger = None,
) -> ACCEPTED_NUM_TYPES:
    """
    Check if param is a strictly positive numeric value and returns it if OK.
    Raises error otherwise.

    Parameters
    ----------
    param
        Value to check
    param_name
        For logging purposes
    param_long_name
        For logging purpose
    log
        For logging purposes

    Returns
    -------
    param
        param if is numeric >0

    Raises
    -------
    ValueError
        If param is not >0
    TypeError
        If param is not numeric

    Examples
    --------
    >>> validate_positive_num_param(12.69, "param", "awesome param")
    12.69
    >>> validate_positive_num_param(-50.5, "param", "awesome param")
    Traceback (most recent call last):
    ValueError: cannot set negative or null awesome param. Got param=-50.5

    """

    # Manage default params
    if param_long_name == "":
        param_long_name = param_name
    if log is None:
        log = get_local_logger("validate_positive_num_param")

    # Apply check
    if isinstance(param, ACCEPTED_NUM_TYPES):
        if param > 0:
            return param
        else:
            err_msg = f"cannot set negative or null {param_long_name}. Got {param_name}={param}"
            log.error(err_msg)
            raise ValueError(err_msg)
    else:
        err_msg = f"{param_long_name} specified is not numeric. Accepted types are {ACCEPTED_NUM_TYPES}. Got {param_name}={param}"
        log.error(err_msg)
        raise TypeError(err_msg)


def validate_positive_int_param(
    param: ACCEPTED_INT_TYPES,
    param_name: str,
    param_long_name: str = "",
    log: logging.Logger = None,
) -> ACCEPTED_NUM_TYPES:
    """
    Check if param is a strictly positive integer value and returns it if OK.
    Raises error otherwise.

    Parameters
    ----------
    param
        Value to check
    param_name
        For logging purposes
    param_long_name
        For logging purpose
    log
        For logging purposes

    Returns
    -------
    param
        param if is integer >0

    Raises
    -------
    ValueError
        If param is not >0
    TypeError
        If param is not integer

    Examples
    --------
    >>> validate_positive_int_param(12, "param", "awesome param")
    12
    >>> validate_positive_int_param(-50, "param", "awesome param")
    Traceback (most recent call last):
    ValueError: cannot set negative or null awesome param. Got param=-50

    """

    # Manage default params
    if param_long_name == "":
        param_long_name = param_name
    if log is None:
        log = get_local_logger("validate_positive_int_param")

    # Apply check
    if isinstance(param, ACCEPTED_INT_TYPES):
        if param > 0:
            return param
        else:
            err_msg = f"cannot set negative or null {param_long_name}. Got {param_name}={param}"
            log.error(err_msg)
            raise ValueError(err_msg)
    else:
        err_msg = f"{param_long_name} specified is not an integer. Accepted types are {ACCEPTED_INT_TYPES}. Got {param_name}={param}"
        log.error(err_msg)
        raise TypeError(err_msg)
