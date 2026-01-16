import pytest
import numpy as np

from culib.field.df_field import init_df_field, init_df_field_3d
from culib.coils.circularcoil import CircularCoil
from culib.wires.roundwire import RoundWire
from culib.field.getters import (
    get_fixed_axis_query_3d,
    get_pos_1d_vs_pos_3d,
    get_field_at_pos,
    get_field_homo_at_pos,
    get_field_3d_at_pos,
    get_field_homo_3d_at_pos,
)


def test_invalid_axis():
    with pytest.raises(ValueError) as excinfo:
        get_fixed_axis_query_3d("Z", 12, 59, -366.6649)
    assert "axis is not in" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        get_pos_1d_vs_pos_3d("Z", (12, 59, -366.6649))
    assert "axis is not in" in str(excinfo.value)


def test_get_pos_1d_vs_pos_3d():
    assert get_pos_1d_vs_pos_3d("x_mm", (12, 59, -366.6649)) == 12
    assert get_pos_1d_vs_pos_3d("y_mm", (12, 59, -366.6649)) == 59
    assert get_pos_1d_vs_pos_3d("z_mm", (12, 59, -366.6649)) == -366.6649


def test_get_field_at_pos_nok_simplecases():
    # Test 1D but axis not specified
    with pytest.raises(ValueError) as excinfo:
        get_field_at_pos(
            df_field=init_df_field(10, 1),
            Baxis="Bx_total_mT",
            pos_mm=12,
        )
    assert "pos_mm is 1D but 'axis' not specified" in str(excinfo.value)

    # Test not 1D either 3D
    with pytest.raises(TypeError) as excinfo:
        get_field_at_pos(
            df_field=init_df_field(10, 1),
            Baxis="Bx_total_mT",
            pos_mm="I'm not a valid position",
        )
    assert "pos_mm is either 1d nor 3d" in str(excinfo.value)

    # Test Baxis column not in df_field
    with pytest.raises(KeyError) as excinfo:
        get_field_at_pos(
            df_field=init_df_field(10, 1),
            Baxis="NOPE_mT",
            pos_mm=-2,
            axis="x_mm",
        )
    assert "column not existing in df_field" in str(excinfo.value)

    with pytest.raises(KeyError) as excinfo:
        get_field_at_pos(
            df_field=init_df_field_3d(10, 1),
            Baxis="NOPE_mT",
            pos_mm=(0, -3, 2),
        )
    assert "column not existing in df_field" in str(excinfo.value)


def test_get_field_at_pos_nok_nosinglepositionindf(caplog):
    caplog.set_level("ERROR")

    # Test zero line found
    with pytest.raises(KeyError) as excinfo:
        get_field_at_pos(
            df_field=init_df_field(10, 1),
            Baxis="Bx_total_mT",
            pos_mm=69,
            axis="x_mm",
        )
    assert "zero line found" in str(excinfo.value)
    assert "zero line found" in caplog.text

    # Test more than one line found
    with pytest.raises(KeyError) as excinfo:
        df_field = init_df_field_3d(1, 0.01)
        get_field_at_pos(
            df_field=df_field,
            Baxis="Bx_total_mT",
            pos_mm=0,
            axis="x_mm",
        )
    assert "more than one line found" in str(excinfo.value)
    assert "more than one line found" in caplog.text


def test_get_field_homo_nok(caplog):
    my_coil = CircularCoil(
        axis="x_mm",
        wire=RoundWire(awg=22, t_insulation_mm=0.05),
        cur_A=12,
        r_out_mm=50 + 5,
        r_in_mm=50 - 5,
        L_mm=15,
        pos_mm=+50 / 2,
    )
    df_field_3d = init_df_field_3d(axis_length_mm=30, res_step_mm=1)
    df_field_3d = my_coil.calc_field_3d(df_field_3d)

    # Uncorrect pos 4D for df 3D
    pos_mm = (3, -12, 1, 666)
    with pytest.raises(TypeError) as excinfo:
        get_field_homo_at_pos(
            df_field_3d,
            axis="z_mm",
            Baxis="Bx_total_mT",
            pos_mm=pos_mm,
            homo_region_mm=5,
        )
    assert "tuple of 3" in str(excinfo.value)
    assert "tuple of 3" in caplog.text

    # Correct pos 1D for df 3D should raise error
    pos_mm = 12
    with pytest.raises(TypeError) as excinfo:
        get_field_homo_at_pos(
            df_field_3d,
            axis="x_mm",
            Baxis="Bx_total_mT",
            pos_mm=pos_mm,
            homo_region_mm=2,
        )
    assert "pos_mm as 3D" in str(excinfo.value)
    assert "pos_mm as 3D" in caplog.text


def test_get_field_and_homo_3d():
    # Define coils and geometry
    dict_coil_param_X = {
        "axis": "x_mm",
        "r_in_mm": 15,
        "r_out_mm": 59.6 / 2,
        "L_mm": 10,
        "wire": RoundWire(d_in_mm=0.8, t_insulation_mm=0.072),
        "n": 200,
        "cur_A": 3.5,
    }
    X_coils = [
        CircularCoil(**dict_coil_param_X, name="X_top_CS13", pos_mm=(36, 30, 0)),
        CircularCoil(**dict_coil_param_X, name="X_bot_CS13", pos_mm=(-36, 30, 0)),
        CircularCoil(**dict_coil_param_X, name="X_mid_CS13", pos_mm=(0, 30, 0)),
        CircularCoil(**dict_coil_param_X, name="X_top_CS24", pos_mm=(36, -30, 0)),
        CircularCoil(**dict_coil_param_X, name="X_bot_CS24", pos_mm=(-36, -30, 0)),
        CircularCoil(**dict_coil_param_X, name="X_mid_CS24", pos_mm=(0, -30, 0)),
    ]
    # Calc field
    pos_CS1_mm = (-18, 30, 0)
    homo_region_3d_mm = (0.5, 0.5, 0.5)
    start_pos_CS1_mm = tuple(np.array(pos_CS1_mm) - np.array(homo_region_3d_mm))
    stop_pos_CS1_mm = tuple(np.array(pos_CS1_mm) + np.array(homo_region_3d_mm))
    df_field = init_df_field_3d(
        start_mm=start_pos_CS1_mm,
        stop_mm=stop_pos_CS1_mm,
        res_step_mm=0.1,
    )
    for coil in X_coils:
        df_field = coil.calc_field_3d(df_field)

    # Check field at pos
    Bxyz = get_field_3d_at_pos(df_field, pos_CS1_mm)
    assert np.isclose(Bxyz[0], 20, atol=2)
    assert np.isclose(Bxyz[1], 0, atol=2)
    assert np.isclose(Bxyz[2], 0, atol=0.01)

    # Check homo
    homo_matrix = get_field_homo_3d_at_pos(df_field, pos_CS1_mm, 0.5)
    ## Bx main comp vs x,y,z
    assert 0 < homo_matrix[0][0] < 0.5
    assert 0 < homo_matrix[0][1] < 0.1
    assert 0 < homo_matrix[0][2] < 0.1
    ## By cross comp vs x,y,z
    assert 0 < homo_matrix[1][0] < 10
    assert 0 < homo_matrix[1][1] < 10
    assert 0 < homo_matrix[1][2] < 10
    ## Zero Bz as placed on z_mm=0
    assert np.isnan(homo_matrix[2]).all()
