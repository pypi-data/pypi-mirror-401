import pandas as pd
import pytest

from culib.field.df_field import (
    init_df_field,
    init_df_field_3d,
    # calc_total_fields,
    is_df_field_1d,
    is_df_field_3d,
)

# from culib.coils.circularcoil import CircularCoil
# from culib.wires.roundwire import RoundWire


def test_is_df_field_1d_nok(caplog):
    caplog.set_level("ERROR")

    # With df_1d
    with pytest.raises(TypeError) as excinfo:
        is_df_field_1d(
            df_field=init_df_field_3d(),
            enable_raise=True,
            log=None,
        )
    assert "not a valid 1d" in str(excinfo.value)
    assert "not a valid 1d" in caplog.text


def test_is_df_field_3d_nok(caplog):
    caplog.set_level("ERROR")

    # With df_1d
    with pytest.raises(TypeError) as excinfo:
        is_df_field_3d(
            df_field=init_df_field(),
            enable_raise=True,
            log=None,
        )
    assert "not a valid 3d" in str(excinfo.value)
    assert "not a valid 3d" in caplog.text

    # Not all axis columns inside
    with pytest.raises(TypeError) as excinfo:
        is_df_field_3d(
            df_field=init_df_field_3d(5, 1).drop(columns=["x_mm"]),
            enable_raise=True,
            log=None,
        )
    assert "not a valid 3d" in str(excinfo.value)
    assert "not a valid 3d" in caplog.text

    # Not a df_field
    assert not is_df_field_3d(
        pd.DataFrame(
            {
                "yes": [12, 3],
                "col2": ["a", "b"],
            }
        )
    )
