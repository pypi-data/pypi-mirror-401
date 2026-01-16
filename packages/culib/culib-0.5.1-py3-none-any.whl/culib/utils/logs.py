import logging

LOG_MASTER_NAME = "cul"
LOG_FORMAT_DEFAULT = "%(asctime)s - %(levelname)-7s - %(name)-28s - %(message)s"
LOG_DATEFORMAT_DEFAULT = "%d/%m/%Y %H:%M:%S"
LOG_FORMATTER_DEFAULT = logging.Formatter(
    fmt=LOG_FORMAT_DEFAULT, datefmt=LOG_DATEFORMAT_DEFAULT
)

# Mute loggings from culib if user did not config loggings
logging.getLogger(LOG_MASTER_NAME).addHandler(logging.NullHandler())


def init_logging(log_level: str | int = logging.WARNING, force: bool = False) -> None:
    """
    Initialize CULib loggings at given log_level.
    To be called after import if wanting to display logs of the lib.

    Parameters
    ----------
    log_level:str|int, optional
        Log level required as str compliant with logging lib (i.e: "INFO", "DEBUG", "ERROR"...) or int (i.e : 10, 40...). Default is "WARNING".
    force:bool, optional
         Force logging to use culib default log formats and level if already been set via call to logging.basicConfig(...). Default is False.

    Examples
    --------
    >>> import culib as cul
    >>> cul.init_logging("INFO")

    """

    # Set default settings of rootlogger
    logging.basicConfig(
        format=LOG_FORMAT_DEFAULT,
        datefmt=LOG_DATEFORMAT_DEFAULT,
        level=log_level,
        force=force,
    )

    # Set level of CULib only
    logging.getLogger(LOG_MASTER_NAME).setLevel(log_level)


def disable_logging() -> None:
    """
    Mute all loggings from CULib.

    Useful only if you already called logging.basicConfig(...) in your code, because CULib loggings are disabled by default if not initialized.

    Examples
    --------
    >>> import logging
    >>> import culib as cul

    >>> logging.basicConfig(level="INFO")
    >>> mylogger = logging.getLogger("mylogger")

    >>> cul.disable_logging()
    >>> mywire = cul.RoundWire(awg=12)

    >>> mylogger.warning("I'm doing stuff, CULib did not log anything")
    """
    logging.getLogger(LOG_MASTER_NAME).setLevel(logging.CRITICAL)


def get_local_logger(name: str, log_level: str | int = None) -> logging.Logger:
    """
    Create a dedicated logger, allowing to display a custom name of location in the log messages
    If log_level is given, the returned logger will be set to the requested level.
    Else it will use current log level of root logger.

    Parameters
    ----------
    name:str
        Logger name
    log_level:str
        Logger level

    Returns
    -------
    logger:logging.Logger
        Local logger

    Examples
    --------
    >>> logger = get_local_logger('my_function')
    >>> logger.warning('This is a local warning from blabla')

    >>> logger = get_local_logger('my_object_to_debug', log_level='DEBUG')
    """

    logger = logging.getLogger(f"{LOG_MASTER_NAME}.{name}")
    if log_level is not None:
        logger.setLevel(log_level)
    return logger
