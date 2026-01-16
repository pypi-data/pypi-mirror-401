import logging

import pytest

from culib.wires.data_wires import WireShape
from culib.wires.roundwire import RoundWire


def test_defined_with_both_awg_and_d_in_mm(caplog):
    caplog.set_level(logging.WARNING)
    awg = 12
    d_in_mm = 0.8
    my_wire = RoundWire(d_in_mm=d_in_mm, awg=awg, t_insulation_mm=0.05)
    assert "both d_in_mm and awg" in caplog.text.lower()
    assert my_wire.awg == awg
    assert my_wire.d_in_mm != d_in_mm


def test_change_shape_nok():
    my_wire = RoundWire(awg=12)
    assert my_wire.shape == WireShape.ROUND
    with pytest.raises(AttributeError):
        my_wire.shape = WireShape.SQUARE
    with pytest.raises(AttributeError):
        my_wire.shape = WireShape.FOIL


# def test_change_material():
#     my_wire = SquareWire(awg=12, material="copper")
#     eta_copper = my_wire.eta_linres_ohmperm
#     my_wire.material = "aluminum"
#     eta_aluminum = my_wire.eta_linres_ohmperm
#     assert eta_copper < eta_aluminum


# def test_change_awg():
#     my_wire = SquareWire(awg=12)
#     eta_big_awg = my_wire.eta_linres_ohmperm
#     my_wire.awg = 18
#     eta_small_awg = my_wire.eta_linres_ohmperm
#     assert eta_big_awg < eta_small_awg
#
#
# def test_change_d_in_mm():
#     my_wire = SquareWire(d_in_mm=0.8)
#     eta_small_diameter = my_wire.eta_linres_ohmperm
#     my_wire.d_in_mm = 1
#     eta_big_diameter = my_wire.eta_linres_ohmperm
#     assert eta_big_diameter < eta_small_diameter
#
#
# def test_change_t_insulation_mm():
#     my_wire = SquareWire(d_in_mm=0.8, t_insulation_mm=0.05)
#     d_out_mm_small_insulation = my_wire.d_out_mm
#     my_wire.t_insulation_mm = 0.1
#     d_out_mm_big_insulation = my_wire.d_out_mm
#     assert d_out_mm_small_insulation < d_out_mm_big_insulation
#
#
# def test_print_wire():
#     my_wire = SquareWire(d_in_mm=0.8)
#     print(my_wire)
