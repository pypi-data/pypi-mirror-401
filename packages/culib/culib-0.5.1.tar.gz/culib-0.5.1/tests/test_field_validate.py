import pytest

from culib.field.validate import is_valid_pos_1d, is_valid_pos_3d, is_valid_axis


def test_is_valid_pos_1d_nok_log():
    with pytest.raises(TypeError):
        is_valid_pos_1d("nope_I_am_a_string", enable_raise=True)


def test_is_valid_pos_3d_nok_log():
    # Type error
    assert not is_valid_pos_3d("nope_I_am_a_string", enable_raise=False)
    with pytest.raises(TypeError):
        is_valid_pos_3d("nope_I_am_a_string", enable_raise=True)

    # 2D dimension
    assert not is_valid_pos_3d((12, -69), enable_raise=False)
    with pytest.raises(ValueError):
        is_valid_pos_3d((12, -69), enable_raise=True)

    # 3D dimension with one element not correct type
    assert not is_valid_pos_3d((12, -69, "42"), enable_raise=False)
    with pytest.raises(TypeError):
        is_valid_pos_3d((12, -69, "42"), enable_raise=True)


def test_is_valid_axis_nok_log():
    # Type error
    assert not is_valid_axis(12, enable_raise=False)
    with pytest.raises(TypeError):
        is_valid_axis(12, enable_raise=True)

    # Not correct axis name
    assert not is_valid_axis("x", enable_raise=False)
    assert not is_valid_axis("AXIS", enable_raise=False)
    with pytest.raises(ValueError):
        is_valid_axis("Z", enable_raise=True)
