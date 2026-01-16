import logging

import pytest

from culib.field.df_field import init_df_field, init_df_field_3d
from culib.plot.df_plot import prepare_df_plot_field


@pytest.fixture
def get_df_field_1d():
    df_field = init_df_field()
    return df_field


@pytest.fixture
def get_df_field_3d():
    df_field = init_df_field_3d()
    return df_field


def test_df_3d_pos_1d_ok(get_df_field_3d):
    for ax in ["x_mm", "y_mm", "z_mm"]:
        prepare_df_plot_field(
            df_field=get_df_field_3d,
            axis=ax,
            Baxis=["Bx_total_mT", "By_total_mT", "Bz_total_mT"],
            pos_mm=12,
            homo_region_mm=1,
        )


def test_df_1d_pos_3d_nok(get_df_field_1d):
    with pytest.raises(TypeError):
        prepare_df_plot_field(
            df_field=get_df_field_1d,
            axis="x_mm",
            Baxis=["Bx_total_mT", "By_total_mT", "Bz_total_mT"],
            pos_mm=(12, -1, 0),
            homo_region_mm=1,
        )


def test_df_3d_pos_3d_size_exceeds_limit(caplog):
    df_field = init_df_field_3d(res_step_mm=1)
    # Check warning log message has been output
    with caplog.at_level(logging.WARNING):
        prepare_df_plot_field(
            df_field=df_field,
            axis="x_mm",
            Baxis=["Bx_total_mT", "By_total_mT", "Bz_total_mT"],
            pos_mm=(1, 1, 1),
            homo_region_mm=1,
            nb_plot_samples=50,
        )
        assert "above max nb_plot_samples" in caplog.text


def test_zoom_but_no_pos(get_df_field_3d):
    with pytest.raises(TypeError):
        prepare_df_plot_field(
            df_field=get_df_field_3d,
            axis="x_mm",
            Baxis=["Bx_total_mT", "By_total_mT", "Bz_total_mT"],
            is_zoom_on_pos=True,
        )


def test_empty_df_after_query(caplog):
    pos_mm = (-1, -4, -12)
    df_field_without_pos = init_df_field_3d(
        start_mm=(0, 0, 0),
        stop_mm=(10, 10, 10),
        res_step_mm=1,
    )
    caplog.set_level(logging.ERROR)
    with pytest.raises(KeyError):
        prepare_df_plot_field(
            df_field=df_field_without_pos,
            axis="x_mm",
            Baxis=["Bx_total_mT", "By_total_mT", "Bz_total_mT"],
            pos_mm=pos_mm,
            homo_region_mm=5,
        )
    assert "empty df found after query" in caplog.text
