from logging import Logger
from pathlib import Path

from culib.utils.logs import get_local_logger


def create_savepath(savepath: Path, force: bool, log: Logger):
    if force:
        warn_msg = f"savepath specified does not exist and force=True, will create specified directory : {savepath}"
        log.warning(warn_msg)
        savepath.mkdir(parents=True)
        log.debug("created directory succesfully")
    else:
        err_msg = f"savepath specified does not exist and force=False, please make sure to create the folder before saving your graph. savepath={savepath}"
        log.error(err_msg)
        raise NotADirectoryError(err_msg)


def save_chart_as_html(
    chart,
    filename: str,
    savepath: Path | str,
    scale_factor=1.0,
    force: bool = True,
):
    """
    ex:
    """
    log = get_local_logger("save_chart_as_html")

    if isinstance(savepath, Path):
        savefilepath = (savepath / filename).with_suffix(".html")
    elif isinstance(savepath, str):
        savepath = Path(savepath)
        filename = filename.split(".html")[0]
        savefilepath = (savepath / Path(filename)).with_suffix(".html")
    else:
        err_msg = f"savepath not a string nor a pathlib.Path, savepath={savepath}"
        log.error(err_msg)
        raise TypeError(err_msg)

    if not savepath.exists():
        create_savepath(savepath, force, log)

    chart.save(savefilepath, scale_factor=scale_factor)
    log.info(f"successfully saved as .html version in {savefilepath}")


def save_chart_as_png(
    chart,
    filename: str,
    savepath: Path | str,
    scale_factor=1.0,
    force: bool = True,
):
    """
    ex:
    """
    log = get_local_logger("save_chart_as_png")

    if isinstance(savepath, Path):
        savefilepath = (savepath / filename).with_suffix(".png")
    elif isinstance(savepath, str):
        savepath = Path(savepath)
        filename = filename.split(".png")[0]
        savefilepath = (savepath / Path(filename)).with_suffix(".png")
    else:
        err_msg = f"savepath not a string nor a pathlib.Path, savepath={savepath}"
        log.error(err_msg)
        raise TypeError(err_msg)

    if not savepath.exists():
        create_savepath(savepath, force, log)

    chart.save(savefilepath, scale_factor=scale_factor)
    log.info(f"successfully saved as .png version in {savefilepath}")


def save_chart(
    chart,
    filename: str,
    savepath_png: Path | str = None,
    savepath_html: Path | str = None,
    scale_factor: float = 1.0,
    force: bool = True,
):
    log = get_local_logger("save_chart")
    # Check
    if savepath_png is None and savepath_html is None:
        err_msg = "no savepath specified for both png and html"
        log.error(err_msg)
        raise ValueError(err_msg)
    # Save as html
    if savepath_html is not None:
        save_chart_as_html(
            chart,
            filename,
            savepath_html,
            scale_factor=scale_factor,
            force=force,
        )
    # Save as png
    if savepath_png is not None:
        save_chart_as_png(
            chart,
            filename,
            savepath_png,
            scale_factor=scale_factor,
            force=force,
        )
