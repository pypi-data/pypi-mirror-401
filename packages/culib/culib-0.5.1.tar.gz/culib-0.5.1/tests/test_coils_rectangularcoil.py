import numpy as np
import pytest

from culib.coils.basecoil import DUMMY_COIL_NAME
from culib.coils.rectangularcoil import RectangularCoil
from culib.wires.basewire import Wire
from culib.wires.roundwire import RoundWire
from culib.wires.foilwire import FoilWire
from culib.field.df_field import init_df_field, init_df_field_3d


@pytest.fixture
def example_coil_ok_minimal_def():
    return RectangularCoil(
        axis="x_mm",
        X_in_mm=45,
        Y_in_mm=57,
        T_mm=2.5,
        L_mm=78,
        wire=RoundWire(awg=16),
    )


def test_create_unnamed_coil(example_coil_ok_minimal_def):
    params = {
        "axis": "x_mm",
        "X_in_mm": 45,
        "Y_in_mm": 57,
        "T_mm": 2.5,
        "L_mm": 78,
        "wire": RoundWire(awg=16),
    }
    assert DUMMY_COIL_NAME in str(RectangularCoil(**params))


def test_change_X_in_mm_ok(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    original_X_out_mm = mycoil.X_out_mm
    original_res_ohm = mycoil.res_ohm
    mycoil.X_in_mm = mycoil.X_in_mm + 5  # Increase X_in
    assert mycoil.X_out_mm > original_X_out_mm
    assert mycoil.res_ohm > original_res_ohm


def test_change_X_impossible(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    with pytest.raises(AttributeError):
        mycoil.X_out_mm = 100
    with pytest.raises(AttributeError):
        mycoil.X_mm = 60


def test_change_Y_in_mm_ok(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    original_Y_out_mm = mycoil.Y_out_mm
    original_res_ohm = mycoil.res_ohm
    mycoil.Y_in_mm = mycoil.Y_in_mm + 5  # Increase Y_in
    assert mycoil.Y_out_mm > original_Y_out_mm
    assert mycoil.res_ohm > original_res_ohm


def test_change_Y_impossible(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    with pytest.raises(AttributeError):
        mycoil.Y_out_mm = 100
    with pytest.raises(AttributeError):
        mycoil.Y_mm = 60


def test_change_T_mm_ok(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    original_T_mm = mycoil.T_mm
    original_X_out_mm = mycoil.X_out_mm
    original_X_in_mm = mycoil.X_in_mm
    original_res_ohm = mycoil.res_ohm
    original_L_mm = mycoil.L_mm

    mycoil.T_mm = mycoil.T_mm + 5  # Increase T

    assert mycoil.T_mm > original_T_mm
    assert mycoil.X_out_mm > original_X_out_mm
    assert mycoil.res_ohm > original_res_ohm
    assert mycoil.X_in_mm == original_X_in_mm
    assert mycoil.L_mm == original_L_mm


def test_change_L_mm_ok(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    original_T_mm = mycoil.T_mm
    original_X_out_mm = mycoil.X_out_mm
    original_X_in_mm = mycoil.X_in_mm
    original_res_ohm = mycoil.res_ohm
    original_L_mm = mycoil.L_mm

    mycoil.L_mm = mycoil.L_mm + 5  # Increase L

    assert mycoil.T_mm == original_T_mm
    assert mycoil.X_out_mm == original_X_out_mm
    assert mycoil.res_ohm > original_res_ohm
    assert mycoil.X_in_mm == original_X_in_mm
    assert mycoil.L_mm > original_L_mm


def test_change_geom_param_negative(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    with pytest.raises(ValueError):
        mycoil.X_in_mm = -12
    with pytest.raises(ValueError):
        mycoil.Y_in_mm = -12
    with pytest.raises(ValueError):
        mycoil.T_mm = -12
    with pytest.raises(ValueError):
        mycoil.L_mm = -12


def test_change_geom_param_uncorrect_type(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    with pytest.raises(TypeError):
        mycoil.X_in_mm = "12"
    with pytest.raises(TypeError):
        mycoil.Y_in_mm = "-12"
    with pytest.raises(TypeError):
        mycoil.T_mm = "-12"
    with pytest.raises(TypeError):
        mycoil.L_mm = "-12"


def test_create_coil_foilwire():
    mycoil = RectangularCoil(
        axis="x_mm",
        X_in_mm=45,
        Y_in_mm=57,
        T_mm=2.5,
        L_mm=78,
        wire=RoundWire(awg=16),
    )
    original_res_ohm = mycoil.res_ohm
    original_n = mycoil.n

    # Change wire to foil
    mycoil.wire = FoilWire(t_foil_mm=0.1, L_foil_mm=1.5)

    assert original_res_ohm != mycoil.res_ohm
    assert original_n != mycoil.n


def test_create_coil_unknown_wire(caplog):
    caplog.set_level("ERROR")
    with pytest.raises(ValueError) as excinfo:
        RectangularCoil(
            axis="x_mm",
            X_in_mm=45,
            Y_in_mm=57,
            T_mm=2.5,
            L_mm=78,
            wire=Wire(awg=16, shape="Timmy"),
        )
    assert "unknown wire" in str(excinfo.value)
    assert "unknown wire" in caplog.text


def test_calc_with_unknown_wire():
    mycoil = RectangularCoil(
        axis="y_mm",
        X_in_mm=35,
        Y_in_mm=57,
        T_mm=6.5,
        L_mm=78,
        wire=Wire(awg=16, shape="round"),
        is_autorecalc=False,
    )
    mycoil.wire._shape = "blblbl"

    with pytest.raises((ValueError, NotImplementedError)) as excinfo:
        mycoil.calc_n()
    assert "unknown wire" in str(excinfo.value)

    with pytest.raises((ValueError, NotImplementedError)) as excinfo:
        mycoil.calc_inductance()
    assert "unknown wire" in str(excinfo.value)


def test_unknown_method_calc_total_wire_length():
    with pytest.raises(ValueError) as excinfo:
        RectangularCoil(
            axis="x_mm",
            X_in_mm=45,
            Y_in_mm=57,
            T_mm=2.5,
            L_mm=78,
            wire=Wire(awg=16, shape="round"),
            method_calc_total_wire_length="blblbl",
        )
    assert "unknown method" in str(excinfo.value)

    with pytest.raises(NotImplementedError) as excinfo:
        RectangularCoil(
            axis="x_mm",
            X_in_mm=45,
            Y_in_mm=57,
            T_mm=2.5,
            L_mm=78,
            wire=Wire(awg=16, shape="round"),
            method_calc_total_wire_length="volume",
        )
    assert "not implemented" in str(excinfo.value)


def test_calc_field_missing_params(example_coil_ok_minimal_def):
    # Try calc field with undefined current
    mycoil = example_coil_ok_minimal_def

    assert mycoil.cur_A is None

    # Calc field 1D
    df_field = init_df_field()
    with pytest.raises(AttributeError) as excinfo:
        df_field = mycoil.calc_field(df_field)
    assert "missing" in str(excinfo.value)
    assert "cur_A" in str(excinfo.value)

    # Calc field 3D
    df_field = init_df_field_3d(axis_length_mm=10, res_step_mm=1)
    with pytest.raises(AttributeError) as excinfo:
        df_field = mycoil.calc_field_3d(df_field)
    assert "missing" in str(excinfo.value)
    assert "cur_A" in str(excinfo.value)

    # Calc field at center approximation
    with pytest.raises(AttributeError) as excinfo:
        mycoil.calc_field_at_center(method="approximation")
    assert "missing" in str(excinfo.value)
    assert "cur_A" in str(excinfo.value)


def test_calc_field_at_center(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    mycoil.cur_A = 10
    B_center_default_mT = mycoil.calc_field_at_center()
    B_center_approximation_mT = mycoil.calc_field_at_center(method="approximation")
    # Assert approximation is OK at 5%
    assert np.isclose(B_center_default_mT, B_center_approximation_mT, rtol=5e-2)

    # Test unknown method
    with pytest.raises(ValueError) as excinfo:
        mycoil.calc_field_at_center(method="TIMMY")
    assert "unknown method" in str(excinfo.value)
