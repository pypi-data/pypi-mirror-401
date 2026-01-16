import numpy as np
import pytest

from culib.coils.basecoil import DUMMY_COIL_NAME
from culib.coils.circularcoil import CircularCoil
from culib.wires.basewire import Wire
from culib.wires.roundwire import RoundWire
from culib.wires.foilwire import FoilWire
from culib.field.df_field import init_df_field, init_df_field_3d


@pytest.fixture
def example_coil_ok_minimal_def():
    return CircularCoil(
        axis="x_mm",
        r_in_mm=45,
        r_out_mm=62,
        L_mm=78,
        wire=RoundWire(awg=16),
    )


@pytest.fixture
def example_coil_ok_foilwire_def():
    return CircularCoil(
        axis="x_mm",
        r_in_mm=45,
        r_out_mm=62,
        L_mm=78,
        wire=FoilWire(t_foil_mm=0.2, L_foil_mm=5),
    )


def test_create_unnamed_coil(example_coil_ok_minimal_def):
    params = {
        "axis": "x_mm",
        "r_in_mm": 45,
        "r_out_mm": 57,
        "L_mm": 78,
        "wire": RoundWire(awg=16),
    }
    assert DUMMY_COIL_NAME in str(CircularCoil(**params))


def test_change_r_in_mm_ok(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    original_r_out_mm = mycoil.r_out_mm
    original_T_mm = mycoil.T_mm
    original_res_ohm = mycoil.res_ohm

    mycoil.r_in_mm = mycoil.r_in_mm + 5  # Increase

    assert mycoil.T_mm < original_T_mm
    assert mycoil.res_ohm < original_res_ohm
    assert mycoil.r_out_mm == original_r_out_mm


def test_change_r_out_mm_ok(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    original_r_in_mm = mycoil.r_in_mm
    original_T_mm = mycoil.T_mm
    original_res_ohm = mycoil.res_ohm

    mycoil.r_out_mm = mycoil.r_out_mm + 5  # Increase

    assert mycoil.T_mm > original_T_mm
    assert mycoil.res_ohm > original_res_ohm
    assert mycoil.r_in_mm == original_r_in_mm


def test_change_r_in_mm_nok(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def

    with pytest.raises(ValueError) as excinfo:
        mycoil.r_in_mm = mycoil.r_out_mm + 5  # Increase
    assert "outer radius is not greater than inner radius" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        mycoil.r_in_mm = -12
    assert "negative or null inner radius" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        mycoil.r_in_mm = "12"
    assert "not numeric" in str(excinfo.value)


def test_change_r_out_mm_nok(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def

    with pytest.raises(ValueError) as excinfo:
        mycoil.r_out_mm = mycoil.r_in_mm - 5  # Increase
    assert "outer radius is not greater than inner radius" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        mycoil.r_out_mm = -12
    assert "negative or null outer radius" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        mycoil.r_out_mm = "12"
    assert "not numeric" in str(excinfo.value)


def test_change_L_mm_ok(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    original_T_mm = mycoil.T_mm
    original_r_out_mm = mycoil.r_out_mm
    original_r_in_mm = mycoil.r_in_mm
    original_res_ohm = mycoil.res_ohm
    original_L_mm = mycoil.L_mm

    mycoil.L_mm = mycoil.L_mm + 5  # Increase L

    assert mycoil.T_mm == original_T_mm
    assert mycoil.r_out_mm == original_r_out_mm
    assert mycoil.res_ohm > original_res_ohm
    assert mycoil.r_in_mm == original_r_in_mm
    assert mycoil.L_mm > original_L_mm


def test_change_impossible_param(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    with pytest.raises(AttributeError):
        mycoil.r_mm = 100
    with pytest.raises(AttributeError):
        mycoil.T_mm = 100


def test_create_coil_then_modif_foilwire():
    mycoil = CircularCoil(
        axis="x_mm",
        r_in_mm=45,
        r_out_mm=57,
        L_mm=78,
        wire=RoundWire(awg=16),
    )
    original_res_ohm = mycoil.res_ohm
    original_n = mycoil.n

    # Change wire to foil
    mycoil.wire = FoilWire(t_foil_mm=0.1, L_foil_mm=1.5)

    assert original_res_ohm != mycoil.res_ohm
    assert original_n != mycoil.n


def test_create_coil_direct_with_foilwire(example_coil_ok_foilwire_def):
    mycoil = example_coil_ok_foilwire_def
    mycoil.cur_A = 10
    B_center_default_mT = mycoil.calc_field_at_center()
    B_center_approximation_mT = mycoil.calc_field_at_center(method="approximation")
    # Assert approximation is OK at 5%
    assert np.isclose(B_center_default_mT, B_center_approximation_mT, rtol=5e-2)

    # Try to redo all calc with volume
    mycoil = CircularCoil(
        axis="x_mm",
        r_in_mm=45,
        r_out_mm=62,
        L_mm=78,
        cur_A=10,
        wire=FoilWire(t_foil_mm=0.2, L_foil_mm=5),
        method_calc_total_wire_length="volume",
    )
    B_center_volume_mT = mycoil.calc_field_at_center()
    assert np.isclose(B_center_default_mT, B_center_volume_mT, rtol=5e-9)


def test_create_coil_unknown_wire(caplog):
    caplog.set_level("ERROR")
    with pytest.raises(ValueError) as excinfo:
        CircularCoil(
            axis="x_mm",
            r_in_mm=45,
            r_out_mm=57,
            L_mm=78,
            wire=Wire(awg=16, shape="Timmy"),
        )
    assert "unknown wire" in str(excinfo.value)
    assert "unknown wire" in caplog.text


def test_calc_with_unknown_wire():
    mycoil = CircularCoil(
        axis="x_mm",
        r_in_mm=45,
        r_out_mm=57,
        L_mm=78,
        wire=Wire(awg=16, shape="round"),
        is_autorecalc=False,
    )
    mycoil.wire._shape = "blblbl"

    with pytest.raises(NotImplementedError) as excinfo:
        mycoil.calc_volume()
    assert "unknown wire" in str(excinfo.value)

    with pytest.raises(NotImplementedError) as excinfo:
        mycoil.calc_n()
    assert "unknown wire" in str(excinfo.value)

    with pytest.raises(NotImplementedError) as excinfo:
        mycoil.calc_inductance()
    assert "unknown wire" in str(excinfo.value)

    mycoil.method_calc_total_wire_length = "volume"
    with pytest.raises((ValueError, NotImplementedError)) as excinfo:
        mycoil.calc_total_wire_length()
    assert "unknown wire" in str(excinfo.value)


def test_calc_volume(example_coil_ok_minimal_def):
    mycoil = example_coil_ok_minimal_def
    res_ohm_default = mycoil.res_ohm

    mycoil.method_calc_total_wire_length = "volume"
    res_ohm_volume = mycoil.res_ohm

    # Assert match is OK at 5%
    assert np.isclose(res_ohm_default, res_ohm_volume, rtol=5e-2)

    # Try with uknown method
    with pytest.raises(ValueError) as excinfo:
        mycoil.method_calc_total_wire_length = "blblbl"
    assert "unknown method" in str(excinfo.value)


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
