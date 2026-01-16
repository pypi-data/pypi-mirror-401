import pytest

from culib.coils.basecoil import BaseCoil, DUMMY_COIL_NAME
from culib.wires.roundwire import RoundWire
from culib.utils.logs import LOG_MASTER_NAME


@pytest.fixture
def example_coil_ok_minimal_def():
    return BaseCoil(
        axis="x_mm",
        wire=RoundWire(awg=16),
    )


def test_create_unnamed_coil():
    params = {
        "axis": "z_mm",
        "wire": RoundWire(awg=16),
    }
    assert DUMMY_COIL_NAME in str(BaseCoil(**params))


def test_print_basecoil(example_coil_ok_minimal_def):
    print(example_coil_ok_minimal_def)


def test_create_basecoil_without_logger(example_coil_ok_minimal_def):
    my_coil = BaseCoil(
        axis="x_mm",
        wire=RoundWire(awg=16),
    )
    assert f"<Logger {LOG_MASTER_NAME}.my_coil.BaseCoil" in str(my_coil.log)
    assert f"<Logger {LOG_MASTER_NAME}.my_coil.BaseCoil" in str(my_coil.wire.log)


def test_get_attributes_minimal_def_ok():
    # Create minimal coil
    my_wire = RoundWire(awg=16)
    c = BaseCoil(
        axis="x_mm",
        wire=my_wire,
    )

    # Assert all attributes are accessible and set to default values
    assert c.is_autorecalc is True
    assert c.log_level is not None
    assert c.axis == "x_mm"
    assert c.pos_mm == 0 or c.pos_mm == (0, 0, 0)
    assert c.pos_x_mm == 0
    assert c.pos_y_mm == 0
    assert c.pos_z_mm == 0
    assert c.n is None
    assert c.n_layer is None
    assert c.n_length is None
    assert c.cur_A is None
    assert c.wire == my_wire
    assert c.method_calc_total_wire_length == "default"
    assert c.temp_degC == 20
    assert c.wire.temp_degC == 20
    assert c.weight_g is None

    # Assert calc functions do nothing at this stage for BaseCoil
    assert c.calc_n() is None
    assert c.calc_total_wire_length() is None
    assert c.calc_res() is None
    assert c.calc_voltage() is None
    assert c.calc_power() is None
    assert c.calc_inductance() is None
    assert c.calc_time_constant() is None
    assert c.calc_weight() is None

    # Assert nothing changed after calls to calc_ functions, still at default values
    assert c.is_autorecalc is True
    assert c.log_level is not None
    assert c.axis == "x_mm"
    assert c.pos_mm == 0 or c.pos_mm == (0, 0, 0)
    assert c.pos_x_mm == 0
    assert c.pos_y_mm == 0
    assert c.pos_z_mm == 0
    assert c.n is None
    assert c.n_layer is None
    assert c.n_length is None
    assert c.cur_A is None
    assert c.wire == my_wire
    assert c.method_calc_total_wire_length == "default"
    assert c.temp_degC == 20
    assert c.wire.temp_degC == 20
    assert c.weight_g is None


def test_uncorrect_wire(caplog, example_coil_ok_minimal_def):
    # Test error at creation
    with pytest.raises(TypeError) as excinfo:
        my_coil = BaseCoil(
            axis="x_mm",
            wire=16,
        )
    assert "wire specified" in str(excinfo.value)

    # Test error after modification
    my_coil = example_coil_ok_minimal_def
    caplog.set_level("ERROR")
    with pytest.raises(TypeError) as excinfo:
        my_coil.wire = 16
    assert "wire specified is not" in str(excinfo.value)
    assert "wire specified is not" in caplog.text


def test_uncorrect_n(caplog, example_coil_ok_minimal_def):
    # Test error at creation
    with pytest.raises(TypeError) as excinfo:
        my_coil = BaseCoil(
            axis="x_mm",
            wire=RoundWire(awg=16),
            n=98.2,
        )
    assert "not an integer" in str(excinfo.value)

    # Test error after modification
    my_coil = example_coil_ok_minimal_def
    caplog.set_level("ERROR")
    with pytest.raises(ValueError) as excinfo:
        my_coil.n = -12
    assert "negative" in str(excinfo.value)
    assert "negative" in caplog.text


def test_correct_pos_mm(caplog, example_coil_ok_minimal_def):
    my_coil = BaseCoil(
        axis="y_mm",
        wire=RoundWire(awg=16),
    )

    # Test set to 3D pos
    my_coil.pos_mm = (12, -656.66, 0.0005)
    assert my_coil.pos_mm == (12, -656.66, 0.0005)
    assert my_coil.pos_x_mm == 12
    assert my_coil.pos_y_mm == -656.66
    assert my_coil.pos_z_mm == 0.0005

    # Test set to 1D pos
    my_coil.pos_mm = -69
    assert my_coil.pos_mm == -69
    assert my_coil.pos_x_mm == 0
    assert my_coil.pos_y_mm == -69  # Because y_mm axis
    assert my_coil.pos_z_mm == 0

    # Test set one coordinate only
    my_coil.pos_x_mm = 23
    assert my_coil.pos_mm == -69
    assert my_coil.pos_x_mm == 23
    assert my_coil.pos_y_mm == -69
    assert my_coil.pos_z_mm == 0


def test_uncorrect_pos_mm(caplog):
    # Test error after modification
    my_coil = BaseCoil(
        axis="y_mm",
        wire=RoundWire(awg=16),
    )
    caplog.set_level("ERROR")

    # Test type error on 3D pos
    with pytest.raises(TypeError) as excinfo:
        my_coil.pos_mm = (22, -6.6, "12")
    assert "not numeric" in str(excinfo.value)
    assert "not numeric" in caplog.text

    # Test type error on 1D pos
    with pytest.raises(TypeError) as excinfo:
        my_coil.pos_x_mm = "22"
    assert "not a valid 1d" in str(excinfo.value)
    assert "not a valid 1d" in caplog.text


# TODO : test_set_attributes
