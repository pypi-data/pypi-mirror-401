from culib.utils.logs import get_local_logger
from culib.wires.data_wires import WireShape
from culib.wires.basewire import (
    Wire,
    DEFAULT_MATERIAL,
    DEFAULT_T_INSULATION_MM,
    DEFAULT_TEMP_DEGC,
)


class SquareWire(Wire):
    """
    Class definition for Square Wire objects.
    Simply subclass of Wire object, with shape=SQUARE passed at init + protection to not change shape property
    """

    def __init__(
        self,
        d_in_mm: float = None,
        awg: int = None,
        r_curv_squarecorner_mm: float = None,
        t_insulation_mm: float = DEFAULT_T_INSULATION_MM,
        temp_degC: float = DEFAULT_TEMP_DEGC,
        material: str = DEFAULT_MATERIAL,
        is_autorecalc: bool = True,
        log_level: int | str = None,
    ):
        super().__init__(
            shape=WireShape.SQUARE,
            material=material,
            temp_degC=temp_degC,
            awg=awg,
            d_in_mm=d_in_mm,
            t_insulation_mm=t_insulation_mm,
            r_curv_squarecorner_mm=r_curv_squarecorner_mm,
            is_autorecalc=is_autorecalc,
            logger=get_local_logger("SquareWire", log_level=log_level),
        )

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        err_msg = "cannot modify shape of SquareWire object. Use general Wire object or RoundWire or FoilWire to have a wire with a different shape."
        self.log.error(err_msg)
        raise AttributeError(err_msg)
