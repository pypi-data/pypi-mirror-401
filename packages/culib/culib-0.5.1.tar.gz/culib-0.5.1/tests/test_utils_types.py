import pytest

from culib.utils.types import (
    validate_num_param,
    validate_positive_num_param,
    validate_positive_int_param,
)


def test_validate_num_param_nok(caplog):
    caplog.set_level("ERROR")

    with pytest.raises(TypeError) as excinfo:
        validate_num_param("string", "param", "my_num_param_but_nope")
    assert "is not numeric" in str(excinfo.value)
    assert "is not numeric" in caplog.text

    with pytest.raises(TypeError) as excinfo:
        validate_num_param(["coucou", 12], "param")
    assert "param specified is not numeric" in str(excinfo.value)
    assert "param specified is not numeric" in caplog.text


def test_validate_positive_num_param_nok(caplog):
    caplog.set_level("ERROR")

    # Type NOK, long name defined
    with pytest.raises(TypeError) as excinfo:
        validate_positive_num_param("nope", "param", "awesome param")
    assert "awesome param specified is not numeric" in str(excinfo.value)
    assert "awesome param specified is not numeric" in caplog.text

    # Type NOK, long name NOT defined
    with pytest.raises(TypeError) as excinfo:
        validate_positive_num_param("nope", "param")
    assert "param specified is not numeric" in str(excinfo.value)
    assert "param specified is not numeric" in caplog.text


def test_validate_positive_int_param_nok(caplog):
    caplog.set_level("ERROR")

    # Type NOK, long name defined
    with pytest.raises(TypeError) as excinfo:
        validate_positive_int_param("nope", "param", "awesome param")
    assert "awesome param specified is not an integer" in str(excinfo.value)
    assert "awesome param specified is not an integer" in caplog.text

    # Type NOK, long name NOT defined
    with pytest.raises(TypeError) as excinfo:
        validate_positive_int_param("nope", "param")
    assert "param specified is not an integer" in str(excinfo.value)
    assert "param specified is not an integer" in caplog.text
