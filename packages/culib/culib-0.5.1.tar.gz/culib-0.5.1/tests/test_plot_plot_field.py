import pytest

from culib import init_df_field, RoundWire, CircularCoil, RectangularCoil, plot_field
from tests.conftest import get_absolute_path


@pytest.fixture
def example_df_field():
    df_field = init_df_field()

    coil_A = CircularCoil(
        axis="z_mm",
        r_in_mm=20,
        r_out_mm=80,
        L_mm=20,
        pos_mm=-30,
        wire=RoundWire(awg=22),
        cur_A=4.69,
    )
    df_field = coil_A.calc_field(df_field)
    coil_B = RectangularCoil(
        axis="z_mm",
        X_in_mm=42,
        Y_in_mm=82,
        T_mm=6,
        L_mm=20,
        pos_mm=+30,
        wire=RoundWire(awg=28),
        cur_A=6.56,
    )
    df_field = coil_B.calc_field(df_field)

    return df_field


def test_plot_zoom_on_pos_noargs_setdefault(example_df_field, caplog):
    caplog.set_level("WARNING")
    plot_field(
        example_df_field,
        axis="z_mm",
        Baxis="Bz_total_mT",
        is_zoom_on_pos=True,
    )
    assert "is_zoom_on_pos selected but pos_mm not defined" in caplog.text
    assert "is_zoom_on_pos selected but homo_region_mm not defined" in caplog.text


def test_Baxis_uncorrect_type(example_df_field, caplog):
    caplog.set_level("ERROR")
    df_field = example_df_field
    with pytest.raises(TypeError) as excinfo:
        plot_field(
            df_field,
            axis="z_mm",
            Baxis=12,  # ("Bz_total_mT"),
            is_zoom_on_pos=True,
            pos_mm=12,
        )
    assert "unknown type" in str(excinfo.value)
    assert "unknown type" in caplog.text


def test_not_found_Baxis_homo(example_df_field, caplog):
    caplog.set_level("WARNING")
    df_field = example_df_field
    df_field = df_field.rename(columns={"Bz_total_mT": "Bz"})
    plot_field(
        df_field,
        axis="z_mm",
        Baxis="Bz",
        is_zoom_on_pos=True,
        pos_mm=12,
    )
    assert "did not find column representing total field for homogeneity" in caplog.text


def test_no_save_filename(example_df_field, caplog):
    caplog.set_level("ERROR")
    plot_field(
        example_df_field,
        axis="z_mm",
        Baxis="Bz_total_mT",
        is_save=True,
        savepath_png=get_absolute_path(__file__, "/data/output_plots/"),
    )
    assert "is_save selected but save_filename not specified" in caplog.text
