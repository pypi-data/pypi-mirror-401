import logging
from decimal import Decimal

import pytest

from culib.wires.basewire import Wire


def test_defined_with_both_awg_and_d_in_mm(caplog):
    caplog.set_level(logging.WARNING)
    awg = 12
    d_in_mm = 0.8
    my_wire = Wire(d_in_mm=d_in_mm, awg=awg, shape="round", t_insulation_mm=0.05)
    assert "both d_in_mm and awg" in caplog.text.lower()
    assert my_wire.awg == awg
    assert my_wire.d_in_mm != d_in_mm


def test_change_shape():
    my_wire = Wire(awg=12, shape="round")
    eta_round = my_wire.eta_linres_ohmperm
    my_wire.shape = "square"
    eta_square = my_wire.eta_linres_ohmperm
    assert eta_round > eta_square


def test_change_material():
    my_wire = Wire(awg=12, shape="round", material="copper")
    eta_copper = my_wire.eta_linres_ohmperm
    my_wire.material = "aluminum"
    eta_aluminum = my_wire.eta_linres_ohmperm
    assert eta_copper < eta_aluminum


def test_change_awg():
    my_wire = Wire(awg=12, shape="round")
    eta_big_awg = my_wire.eta_linres_ohmperm
    my_wire.awg = 18
    eta_small_awg = my_wire.eta_linres_ohmperm
    assert eta_big_awg < eta_small_awg


def test_change_d_in_mm():
    my_wire = Wire(d_in_mm=0.8, shape="round")
    eta_small_diameter = my_wire.eta_linres_ohmperm
    my_wire.d_in_mm = 1
    eta_big_diameter = my_wire.eta_linres_ohmperm
    assert eta_big_diameter < eta_small_diameter


def test_change_d_in_mm_with_awg_defined():
    my_wire = Wire(awg=12, shape="round")
    with pytest.raises(ValueError) as excinfo:
        my_wire.d_in_mm = 0.5
    assert "AWG number is already defined" in str(excinfo.value)


def test_change_t_insulation_mm():
    my_wire = Wire(d_in_mm=0.8, shape="round", t_insulation_mm=0.05)
    d_out_mm_small_insulation = my_wire.d_out_mm
    my_wire.t_insulation_mm = 0.1
    d_out_mm_big_insulation = my_wire.d_out_mm
    assert d_out_mm_small_insulation < d_out_mm_big_insulation


def test_change_r_curv_squarecorner_mm():
    my_wire = Wire(d_in_mm=0.8, shape="square", t_insulation_mm=0.05)

    r_curv_squarecorner_mm_default = my_wire.r_curv_squarecorner_mm
    area_default = my_wire.section_area_mm2
    eta_default = my_wire.eta_linres_ohmperm

    my_wire.r_curv_squarecorner_mm = r_curv_squarecorner_mm_default * 1.5
    r_curv_squarecorner_mm_increased = my_wire.r_curv_squarecorner_mm
    area_new = my_wire.section_area_mm2
    eta_new = my_wire.eta_linres_ohmperm

    assert r_curv_squarecorner_mm_increased > r_curv_squarecorner_mm_default
    assert area_new < area_default
    assert eta_new > eta_default


def test_change_is_autorecalc():
    my_wire = Wire(d_in_mm=0.8, shape="round", t_insulation_mm=0.1, is_autorecalc=False)
    initial_eta = my_wire.eta_linres_ohmperm
    my_wire.d_in_mm = 1.2
    assert my_wire.eta_linres_ohmperm == initial_eta

    my_wire.is_autorecalc = True
    assert my_wire.eta_linres_ohmperm != initial_eta


def test_change_impossible_attributes():
    my_wire = Wire(d_in_mm=0.8, shape="round", t_insulation_mm=0.05)
    with pytest.raises(AttributeError):
        my_wire.t_insulation_recommended_mm = 12
    with pytest.raises(AttributeError):
        my_wire.d_out_mm = 12
    with pytest.raises(AttributeError):
        my_wire.section_area_mm2 = 12
    with pytest.raises(AttributeError):
        my_wire.temp_coef_resistivity_perdegC = 12
    with pytest.raises(AttributeError):
        my_wire.rho_resistivity_meterohm = 12
    with pytest.raises(AttributeError):
        my_wire.eta_linres_ohmperm = 12
    with pytest.raises(AttributeError):
        my_wire.mass_lindensity_gperm = 12


def test_change_impossible_attributes_foil(caplog):
    my_wire = Wire(d_in_mm=0.8, shape="round", t_insulation_mm=0.05)
    caplog.set_level("WARNING")
    my_wire.L_foil_mm = 12
    assert "L_foil_mm changed but current wire shape is" in caplog.text
    my_wire.t_foil_mm = 12
    assert "t_foil_mm changed but current wire shape is" in caplog.text


def test_define_foil_uncorrect(caplog):
    caplog.set_level("WARNING")
    with pytest.raises(ValueError) as excinfo:
        Wire(d_in_mm=0.8, shape="foil", t_insulation_mm=0.05)

    expected_err_msg = "foil wire selected but L_foil_mm or t_foil_mm not specified"
    assert expected_err_msg in str(excinfo.value)
    assert expected_err_msg in caplog.text


def test_unknown_shape():
    with pytest.raises(ValueError) as excinfo:
        my_wire = Wire(d_in_mm=0.8, shape="zoboidal", t_insulation_mm=0.05)
    assert "unknown wire shape" in str(excinfo.value)

    my_wire = Wire(d_in_mm=1.2, shape="round")
    my_wire._shape = "zoboidal"
    with pytest.raises(NotImplementedError) as excinfo:
        my_wire.r_curv_squarecorner_mm = 0.1
    assert "unknown wire shape" in str(excinfo.value)


def test_unknown_material():
    my_wire = Wire(d_in_mm=0.8, shape="round", t_insulation_mm=0.05)
    with pytest.raises(ValueError):
        my_wire.material = "wood"


def test_unknown_awg():
    my_wire = Wire(awg=12, shape="round", t_insulation_mm=0.05)
    with pytest.raises(KeyError) as excinfo:
        my_wire.awg = 666
    assert "unsupported AWG number" in str(excinfo.value)


def test_print_wire():
    my_wire = Wire(d_in_mm=0.8, shape="square")
    print(my_wire)
    my_wire_repr = str(my_wire)
    assert my_wire.material in my_wire_repr
    assert f"{my_wire.t_insulation_recommended_mm:.3f}" in my_wire_repr
    assert f"{round(my_wire.r_curv_squarecorner_mm, 3)}" in my_wire_repr
    assert f"{my_wire.temp_coef_resistivity_perdegC:.3f}" in my_wire_repr
    assert f"{Decimal(my_wire.rho_resistivity_meterohm):.3e}" in my_wire_repr


def test_trigger_coil_param_recalc_return_none():
    my_wire = Wire(d_in_mm=0.8, shape="round")
    return_val = my_wire.trigger_all_coil_param_recalc_func()
    assert return_val is None
    return_val = my_wire.trigger_elec_coil_param_recalc_func()
    assert return_val is None
