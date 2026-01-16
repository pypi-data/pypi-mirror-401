from pathlib import Path


def get_absolute_path(current_file: str | Path, rel_path: str | Path) -> Path:
    """
    Get an absolute path of a relative position from current module/package

    Examples
    --------
    # To be called like this :

    >>> conf_file = get_absolute_path(__file__, "../../../data/config.toml")

    Parameters
    ----------
    current_file: str|Path
        Must be __file__
    rel_path: str|Path
        The relative path wanted

    Returns
    -------
    abs_path : Path
        Resolved absolute path from relative "rel_path"
    """
    return (Path(current_file).parent / Path(rel_path)).resolve()
