import pytest

from culib.wires.data_wires import WireShape
from culib.wires.foilwire import FoilWire


def test_change_shape_nok():
    my_wire = FoilWire(t_foil_mm=0.4, L_foil_mm=3, t_insulation_mm=0.05)
    assert my_wire.shape == WireShape.FOIL
    with pytest.raises(AttributeError):
        my_wire.shape = WireShape.SQUARE


def test_change_t_foil_mm():
    my_wire = FoilWire(t_foil_mm=0.4, L_foil_mm=3, t_insulation_mm=0.05)
    area_default = my_wire.section_area_mm2
    eta_default = my_wire.eta_linres_ohmperm

    my_wire.t_foil_mm = 0.6
    area_new = my_wire.section_area_mm2
    eta_new = my_wire.eta_linres_ohmperm

    assert area_new > area_default
    assert eta_new < eta_default


def test_change_t_foil_mm_uncorrect_type():
    with pytest.raises(TypeError) as excinfo:
        FoilWire(t_foil_mm="12", L_foil_mm=3)
    assert "not numeric" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        FoilWire(t_foil_mm=-4, L_foil_mm=3)
    assert "negative" in str(excinfo.value)


def test_change_L_foil_mm():
    my_wire = FoilWire(t_foil_mm=0.4, L_foil_mm=3, t_insulation_mm=0.05)
    area_default = my_wire.section_area_mm2
    eta_default = my_wire.eta_linres_ohmperm

    my_wire.L_foil_mm = 5
    area_new = my_wire.section_area_mm2
    eta_new = my_wire.eta_linres_ohmperm

    assert area_new > area_default
    assert eta_new < eta_default
