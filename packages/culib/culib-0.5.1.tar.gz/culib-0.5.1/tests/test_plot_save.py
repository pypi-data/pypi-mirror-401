from pathlib import Path

import pytest

from culib import init_df_field, RoundWire, RectangularCoil, plot_field
from culib.plot.save import save_chart_as_html, save_chart_as_png, save_chart
from tests.conftest import get_absolute_path


@pytest.fixture
def example_chart():
    df_field = init_df_field()

    coil_A = RectangularCoil(
        axis="z_mm",
        X_in_mm=42,
        Y_in_mm=82,
        T_mm=6,
        L_mm=20,
        pos_mm=-30,
        wire=RoundWire(awg=22),
        cur_A=6.56,
    )
    df_field = coil_A.calc_field(df_field)
    coil_B = RectangularCoil(
        axis="z_mm",
        X_in_mm=42,
        Y_in_mm=82,
        T_mm=6,
        L_mm=20,
        pos_mm=+30,
        wire=RoundWire(awg=22),
        cur_A=6.56,
    )
    df_field = coil_B.calc_field(df_field)

    return plot_field(
        df_field,
        axis="z_mm",
        Baxis="Bz_total_mT",
        title="Main field along main axis of coil A + coil B",
        subtitle=f"My param = 12, AWG = {coil_A.wire.awg}, Distance btw coils (mm) = {coil_B.pos_mm - coil_A.pos_mm}",
    )


@pytest.mark.save
def test_save_chart_as_html_pathlib_ok(example_chart):
    savepath = get_absolute_path(__file__, "data/output_plots/interactive_html")
    save_chart_as_html(
        chart=example_chart,
        filename="example_chart",
        savepath=savepath,
    )


@pytest.mark.save
def test_save_chart_as_html_pathlib_nok(example_chart):
    savepath = Path("./tests/data/output_plots/UNKNOWN_DIRECTORY/")
    with pytest.raises(NotADirectoryError):
        save_chart_as_html(
            chart=example_chart,
            filename="impossible_example_chart",
            savepath=savepath,
            force=False,
        )


@pytest.mark.save
def test_save_chart_as_html_force_path_creation(example_chart):
    savepath = get_absolute_path(__file__, "data/output_plots/FORCED_directory/")
    filename = "forced_example_chart"
    save_chart_as_html(
        chart=example_chart,
        filename=filename,
        savepath=savepath,
        force=True,
    )
    # Check created file is well existing
    savefile = savepath / f"{filename}.html"
    assert savefile.exists()
    # Delete file and FORCED_directory
    for f in savepath.glob("*"):
        f.unlink()
    savepath.rmdir()


@pytest.mark.save
def test_save_chart_as_html_uncorrect_type_savepath(example_chart):
    with pytest.raises(TypeError):
        save_chart_as_html(
            chart=example_chart,
            filename="impossible_chart",
            savepath=12,
            force=True,
        )


@pytest.mark.save
def test_save_chart_as_png_pathlib_ok(example_chart):
    savepath = get_absolute_path(__file__, "data/output_plots/")
    save_chart_as_png(
        chart=example_chart,
        filename="example_chart",
        savepath=savepath,
    )


@pytest.mark.save
def test_save_chart_as_png_pathlib_nok(example_chart):
    savepath = Path("./tests/data/output_plots/UNKNOWN_DIRECTORY/")
    with pytest.raises(NotADirectoryError):
        save_chart_as_png(
            chart=example_chart,
            filename="impossible_example_chart",
            savepath=savepath,
            force=False,
        )


@pytest.mark.save
def test_save_chart_as_png_uncorrect_type_savepath(example_chart):
    with pytest.raises(TypeError):
        save_chart_as_png(
            chart=example_chart,
            filename="impossible_chart",
            savepath=12,
            force=True,
        )


@pytest.mark.save
def test_save_chart_ok(example_chart):
    savepath_png = get_absolute_path(__file__, "data/output_plots/")
    savepath_html = get_absolute_path(__file__, "data/output_plots/interactive_html")
    save_chart(
        chart=example_chart,
        filename="full_example_chart",
        savepath_png=savepath_png,
        savepath_html=savepath_html,
        scale_factor=2,
    )


@pytest.mark.save
def test_save_chart_no_savepath(example_chart, caplog):
    caplog.set_level("ERROR")
    with pytest.raises(ValueError):
        save_chart(
            chart=example_chart,
            filename="full_example_chart",
            scale_factor=2,
        )
    assert "no savepath specified" in caplog.text
