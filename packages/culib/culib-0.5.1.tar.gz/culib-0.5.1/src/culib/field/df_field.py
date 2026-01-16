from logging import Logger

import pandas as pd
import numpy as np

from culib.utils.logs import get_local_logger
from culib.field.validate import is_valid_pos_1d, is_valid_pos_3d, TUPLE_VALID_AXIS

DEFAULT_1D_AXIS_LENGTH_MM = 160
DEFAULT_1D_RES_STEP_MM = 0.05

DEFAULT_3D_AXIS_LENGTH_MM = 100
DEFAULT_3D_RES_STEP_MM = 1


def init_df_field(
    axis_length_mm: float = 160,
    res_step_mm: float = 0.05,
    start_mm: float = None,
    stop_mm: float = None,
) -> pd.DataFrame:
    """
    Prepare an empty df with axis columns and arrays for field calculation.
    Will prepare 3 x 1D axis (not a full 3D mesh).
    If start_mm and stop_mm specified, axis will be between [start_mm, stop_mm]. If not, axis will be [-axis_length_mm/2, +axis_length_mm/2].

    Parameters
    ----------
    axis_length_mm : float, optional
        Total length of the axis in mm. If start_mm and stop_mm are not specified, axis will be between [-axis_length_mm/2, +axis_length_mm/2]. Otherwise, it will be ignored. Default = 160
    res_step_mm : float, optional
        Resolution step wanted between 2 points in mm. Default = 0.05
    start_mm : float, optional
        Start of the axis in mm. If set, axis_length_mm will be ignored. Must specify stop_mm if used. Default = None
    stop_mm : float, optional
        End of the axis in mm. If set, axis_length_mm will be ignored. Must specify start_mm if used. Default = None

    Returns
    -------
    df_field : pd.DataFrame
        Dataframe containing 3 columns with spatial axis "x_mm", "y_mm" and "z_mm" + 3 columns with B field components "Bx_total_mT", "By_total_mT" and "Bz_total_mT", initialized at 0.
        Shape = (int(axis_length_mm/res_step_mm)+1, 6)

    Examples
    --------
    ## Get df_field with default values

    >>> df_field = init_df_field()

    ## Specify with custom start/stop values

    >>> df_field = init_df_field(start_mm = -3, stop_mm = 5.5, res_step_mm = 0.5)

    ## Specify with custom values for axis_length_mm

    >>> df_field = init_df_field(axis_length_mm = 100, res_step_mm = 0.1)

    """
    log = get_local_logger("init_df_field")

    # Manage if start and stop
    if start_mm is not None and stop_mm is not None:
        if start_mm < stop_mm:
            axis_length_mm = stop_mm - start_mm
        else:
            err_msg = f"start_mm >= stop_mm. Got start_mm={start_mm} and stop_mm={stop_mm}"  # fmt: skip
            log.error(err_msg)
            raise ValueError(err_msg)
    elif start_mm is None and stop_mm is None:
        # Behaviour with axis_length_mm
        start_mm = -axis_length_mm / 2
        stop_mm = axis_length_mm / 2
    else:
        if start_mm:
            err_msg = f"start_mm specified but not stop_mm. Got start_mm={start_mm} and stop_mm={stop_mm}"  # fmt: skip
        else:
            err_msg = f"stop_mm specified but not start_mm. Got start_mm={start_mm} and stop_mm={stop_mm}"  # fmt: skip
        log.error(err_msg)
        raise ValueError(err_msg)

    res_axis = int(axis_length_mm / res_step_mm) + 1

    df_field = pd.DataFrame()
    df_field["x_mm"] = np.linspace(start=start_mm, stop=stop_mm, num=res_axis)
    df_field["y_mm"] = np.linspace(start=start_mm, stop=stop_mm, num=res_axis)
    df_field["z_mm"] = np.linspace(start=start_mm, stop=stop_mm, num=res_axis)

    df_field["Bx_total_mT"] = 0
    df_field["By_total_mT"] = 0
    df_field["Bz_total_mT"] = 0

    return df_field


def init_df_field_3d(
    axis_length_mm: float | tuple[float, float, float] = 100,
    res_step_mm: float | tuple[float, float, float] = 1,
    start_mm: float | tuple[float, float, float] = None,
    stop_mm: float | tuple[float, float, float] = None,
) -> pd.DataFrame:
    """
    Prepare an empty df with axis columns and arrays for field calculation.
    Will prepare a full 3D mesh.
    If start_mm and stop_mm specified, axis will be between [start_mm, stop_mm]. Otherwise, axis will be between [-axis_length_mm/2, +axis_length_mm/2].
    start_mm and stop_mm can be specfied as 3D, so it can have different size of axis per dimension.

    Warnings
    --------
    WARNING : be careful with small res_step_mm, size of df is function of (length/res)^3 !

    Parameters
    ----------
    axis_length_mm : float, optional
        Total length of the axis in mm. If start_mm and stop_mm are not specified, axis will be between [-axis_length_mm/2, +axis_length_mm/2. Otherwise, it will be ignored. Default = 160
    res_step_mm : float, optional
        Resolution step wanted between 2 points in mm. Default = 1
    start_mm : float | tuple[float, float, float], optional
        Start of the axis in mm. If set, axis_length_mm will be ignored. Must specify stop_mm if used. Default = None
    stop_mm : float | tuple[float, float, float], optional
        End of the axis in mm. If set, axis_length_mm will be ignored. Must specify start_mm if used. Default = None

    Returns
    -------
    df_field : pd.DataFrame
        Dataframe containing 3 columns with spatial axis x_mm, y_mm and z_mm + 3 columns with B field components Bx_total_mT, By_total_mT and Bz_total_mT, initialized at 0.
        Shape = ((int(axis_length_mm/res_step_mm)+1)**3, 6)

    Examples
    --------
    ## Get df_field with default values

    >>> df_field_3d = init_df_field_3d()
    >>> df_field_3d.shape
    (1030301, 6)

    ## Specify with custom values for start/stop, common for each axis

    >>> df_field_3d = init_df_field_3d(start_mm = -15, stop_mm = -5, res_step_mm = 1)
    >>> df_field_3d.shape
    (1331, 6)

    ## Specify with custom values for start/stop, different for each axis

    >>> df_field_3d = init_df_field_3d(start_mm = (-5,-2,-3), stop_mm = (7, 10, 7), res_step_mm = 0.5)
    >>> df_field_3d.shape
    (13125, 6)

    ## Specify with one common low res_step_mm for every axis (and beware of HUGE size of df for small step !)

    >>> df_field_3d = init_df_field_3d(res_step_mm = 0.5)
    >>> df_field_3d.shape
    (8120601, 6)

    ## Specify a different resolution for each axis

    >>> df_field_3d = init_df_field_3d(axis_length_mm=50, res_step_mm = (1, 0.5, 5))
    >>> df_field_3d.shape
    (56661, 6)

    ## Specify different resolution and start/stop per axis

    >>> df_field_3d = init_df_field_3d(start_mm = (-5,-2,-3), stop_mm = (7, 10, 7), res_step_mm = (0.5, 0.25, 0.5))
    >>> df_field_3d.shape
    (25725, 6)

    -------

    """

    log = get_local_logger("init_df_field_3d")

    # Manage if start and stop
    if start_mm is not None and stop_mm is not None:
        ## Manage 1D
        if is_valid_pos_1d(start_mm, enable_raise=False) and is_valid_pos_1d(
            stop_mm, log=log, enable_raise=False
        ):
            start_x_mm = start_mm
            start_y_mm = start_mm
            start_z_mm = start_mm
            stop_x_mm = stop_mm
            stop_y_mm = stop_mm
            stop_z_mm = stop_mm
            if start_mm >= stop_mm:
                err_msg = f"start_mm >= stop_mm. Got start_mm={start_mm} and stop_mm={stop_mm}"  # fmt: skip
                log.error(err_msg)
                raise ValueError(err_msg)
        ## Manage 3D
        elif is_valid_pos_3d(start_mm, enable_raise=False) and is_valid_pos_3d(
            stop_mm, enable_raise=False
        ):
            start_x_mm = start_mm[0]
            start_y_mm = start_mm[1]
            start_z_mm = start_mm[2]
            stop_x_mm = stop_mm[0]
            stop_y_mm = stop_mm[1]
            stop_z_mm = stop_mm[2]
            err_msg = ""
            if start_x_mm > stop_x_mm:
                err_msg += f"start_x_mm > stop_x_mm. Got start_x_mm={start_x_mm} and stop_x_mm={stop_x_mm} \n"  # fmt: skip
            elif start_y_mm > stop_y_mm:
                err_msg += f"start_y_mm > stop_y_mm. Got start_y_mm={start_y_mm} and stop_y_mm={stop_y_mm} \n"  # fmt: skip
            elif start_z_mm > stop_z_mm:
                err_msg += f"start_z_mm > stop_z_mm. Got start_z_mm={start_z_mm} and stop_z_mm={stop_z_mm} \n"  # fmt: skip
            if err_msg != "":
                err_msg = err_msg[:-2]
                log.error(err_msg)
                raise ValueError(err_msg)
        else:
            err_msg = f"start_mm and stop_mm specified, but mismatch 1D/3D. Got start_mm={start_mm} and stop_mm={stop_mm}"
            log.error(err_msg)
            raise ValueError(err_msg)
    # Manage standard behaviour with axis_length_mm
    elif start_mm is None and stop_mm is None:
        start_mm = -axis_length_mm / 2
        stop_mm = axis_length_mm / 2
        start_x_mm = start_mm
        start_y_mm = start_mm
        start_z_mm = start_mm
        stop_x_mm = stop_mm
        stop_y_mm = stop_mm
        stop_z_mm = stop_mm
    else:
        if start_mm:
            err_msg = f"start_mm specified but not stop_mm. Got start_mm={start_mm} and stop_mm={stop_mm}"  # fmt: skip
        else:
            err_msg = f"stop_mm specified but not start_mm. Got start_mm={start_mm} and stop_mm={stop_mm}"  # fmt: skip
        log.error(err_msg)
        raise ValueError(err_msg)

    # Manage resolution
    if is_valid_pos_1d(res_step_mm, enable_raise=False):
        res_step_x_mm = res_step_mm
        res_step_y_mm = res_step_mm
        res_step_z_mm = res_step_mm
    elif is_valid_pos_3d(res_step_mm, enable_raise=False):
        res_step_x_mm = res_step_mm[0]
        res_step_y_mm = res_step_mm[1]
        res_step_z_mm = res_step_mm[2]
    else:
        err_msg = f"res_step_mm neither 1D nor 3D. Got res_step_mm={res_step_mm}"
        log.error(err_msg)
        raise ValueError(err_msg)

    res_axis_x = int((stop_x_mm - start_x_mm) / res_step_x_mm) + 1
    res_axis_y = int((stop_y_mm - start_y_mm) / res_step_y_mm) + 1
    res_axis_z = int((stop_z_mm - start_z_mm) / res_step_z_mm) + 1

    ser_axis_x = np.linspace(start=start_x_mm, stop=stop_x_mm, num=res_axis_x)
    ser_axis_y = np.linspace(start=start_y_mm, stop=stop_y_mm, num=res_axis_y)
    ser_axis_z = np.linspace(start=start_z_mm, stop=stop_z_mm, num=res_axis_z)

    df_x = pd.DataFrame(ser_axis_x, columns=["x_mm"])
    df_y = pd.DataFrame(ser_axis_y, columns=["y_mm"])
    df_z = pd.DataFrame(ser_axis_z, columns=["z_mm"])

    df_x["Bx_total_mT"] = 0
    df_y["Bx_total_mT"] = 0
    df_z["Bx_total_mT"] = 0

    df_xy = pd.merge(df_x, df_y, on="Bx_total_mT", how="outer")
    df_field = pd.merge(df_xy, df_z, on="Bx_total_mT", how="outer")

    df_field["By_total_mT"] = 0
    df_field["Bz_total_mT"] = 0

    # Reorder columns
    list_col = ["x_mm", "y_mm", "z_mm", "Bx_total_mT", "By_total_mT", "Bz_total_mT"]
    df_field = df_field[list_col]

    return df_field


def calc_total_fields(df_field: pd.DataFrame) -> pd.DataFrame:
    """
    Automatically recalculates Bx_total_mT, By_total_mT and Bz_total_mT from sum of all applicable columns
    (field superposition theorem)

    Parameters
    ----------
    df_field : pd.DataFrame
        Dataframe containing 3 columns with spatial axis x_mm, y_mm and z_mm + field components

    Returns
    -------
    df_field : pd.DataFrame
        Updated df_field with Bx_total_mT, By_total_mT and Bz_total_mT recalculated from all applicable columns

    Examples
    --------
    >>> from culib import get_field_at_pos, CircularCoil, RoundWire
    >>> df_field = init_df_field(axis_length_mm=250, res_step_mm=0.05)
    >>> G_coils_mm = 60  # Gap between coils centers in mm
    >>> dut_pos_mm = 30  # DUT position
    >>> hall5_coils_param = {
    ...     'r_out_mm': 14,
    ...     'r_in_mm': 5,
    ...     'L_mm': 30,
    ...     'n': 348,
    ...     'cur_A': 2.7,
    ...     'wire': RoundWire(d_in_mm=0.812),
    ... }
    >>> left_coil = CircularCoil(
    ...     axis='y_mm',
    ...     pos_mm=-G_coils_mm,
    ...     **hall5_coils_param)
    >>> df_field = left_coil.calc_field(df_field)
    >>> mid_coil = CircularCoil(
    ...    axis='y_mm',
    ...    pos_mm=0,
    ...    **hall5_coils_param)
    >>> df_field = mid_coil.calc_field(df_field)
    >>> right_coil = CircularCoil(
    ...     axis='y_mm',
    ...     pos_mm=+G_coils_mm,
    ...     **hall5_coils_param)
    >>> df_field = right_coil.calc_field(df_field)
    >>> df_field = calc_total_fields(df_field) # Will make the sum of df_field['By_left_coil_mT'] + df_field['By_mid_coil_mT'] + df_field['By_right_coil_mT']
    >>> get_field_at_pos(df_field, axis='y_mm', Baxis='By_total_mT', pos_mm=dut_pos_mm)
    5.33
    """

    # log = get_local_logger('init_df_field', **kwargs)
    list_Bx_fields_to_sum = [
        c
        for c in df_field.columns
        if (c.startswith("Bx_") and c != "Bx_total_mT" and c != "Bx_mT")
    ]
    list_By_fields_to_sum = [
        c
        for c in df_field.columns
        if (c.startswith("By_") and c != "By_total_mT" and c != "By_mT")
    ]
    list_Bz_fields_to_sum = [
        c
        for c in df_field.columns
        if (c.startswith("Bz_") and c != "Bz_total_mT" and c != "Bz_mT")
    ]

    if len(list_Bx_fields_to_sum) > 0:
        df_field["Bx_total_mT"] = 0
        for c in list_Bx_fields_to_sum:
            df_field["Bx_total_mT"] += df_field[c]

    if len(list_By_fields_to_sum) > 0:
        df_field["By_total_mT"] = 0
        for c in list_By_fields_to_sum:
            df_field["By_total_mT"] += df_field[c]

    if len(list_Bz_fields_to_sum) > 0:
        df_field["Bz_total_mT"] = 0
        for c in list_Bz_fields_to_sum:
            df_field["Bz_total_mT"] += df_field[c]

    return df_field


def is_df_field_1d(
    df_field: pd.DataFrame, enable_raise: bool = False, log: Logger = None
) -> bool:
    """
    >>> import culib as cul
    >>> df_1d = cul.init_df_field()
    >>> is_df_field_1d(df_1d)
    True
    >>> df_3d = cul.init_df_field_3d(10,1)
    >>> is_df_field_1d(df_3d)
    False
    """
    set_df_columns = {el for el in df_field.columns}
    is_all_axis_inside = set(TUPLE_VALID_AXIS).issubset(set_df_columns)

    if is_all_axis_inside:
        is_all_axis_equal = (df_field["x_mm"] == df_field["y_mm"]).all()
        if enable_raise and not is_all_axis_equal:
            if log is None:
                log = get_local_logger("is_df_field_1d")
            err_msg = "df_field is not a valid 1d"
            log.error(err_msg)
            raise TypeError(err_msg)
        return is_all_axis_equal
    else:
        return True


def is_df_field_3d(
    df_field: pd.DataFrame, enable_raise: bool = False, log: Logger = None
) -> bool:
    """
    >>> import culib as cul
    >>> df_1d = cul.init_df_field()
    >>> is_df_field_3d(df_1d)
    False
    >>> df_3d = cul.init_df_field_3d(10,1)
    >>> is_df_field_3d(df_3d)
    True
    """
    set_df_columns = {el for el in df_field.columns}
    is_all_axis_inside = set(TUPLE_VALID_AXIS).issubset(set_df_columns)

    # Manage logger
    if enable_raise and log is None:
        log = get_local_logger("is_df_field_3d")

    if is_all_axis_inside:
        is_all_axis_equal = (df_field["x_mm"] == df_field["y_mm"]).all()
        if enable_raise and is_all_axis_equal:
            err_msg = "df_field is not a valid 3d"
            log.error(err_msg)
            raise TypeError(err_msg)
        return not is_all_axis_equal
    else:
        if enable_raise:
            err_msg = "df_field is not a valid 3d (not all axis column inside)"
            log.error(err_msg)
            raise TypeError(err_msg)
        return False
