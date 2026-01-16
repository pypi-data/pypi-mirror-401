# TODO (prio 2) : add utilities to create new wire type (or modifying resistivity values..)

import logging
from types import MethodType
from decimal import Decimal

import numpy as np

from culib.utils.logs import get_local_logger
from culib.utils.types import validate_positive_num_param, validate_num_param
from culib.wires.data_wires import (
    WireShape,
    Material,
    LIST_WIRE_MATERIALS,
    LIST_WIRE_SHAPES,
    DICT_D_WIRE_IN_MM_VS_AWG,
    DICT_RHO_RESISTIVITY_METEROHM_VS_MATERIAL,
    DICT_TEMP_COEF_RESISTIVITY_PERDEGC_VS_MATERIAL,
    DICT_MASS_DENSITY_GPERCM3_VS_MATERIAL,
    get_recommended_insulation_thickness,
)

# Define defaults parameters
DEFAULT_SHAPE = WireShape.ROUND
DEFAULT_MATERIAL = Material.COPPER
DEFAULT_T_INSULATION_MM = 0.05
DEFAULT_TEMP_DEGC = 20


class Wire:
    """
    Class definition for Wire objects to attach to Coil objects.
    Minimum requirements for declaring a wire is to declare wire inner diameter without insulation d_in_mm OR awg (American Wire Gauge) number, defining a d_in_mm.
    For 'foil' wire, need to define t_foil_mm and L_foil_mm. Advise is to use culib FoilWire() object directly.
    Automatic recalc if change (and triggers automatic recalc of coil parameters when accessed from a coil (i.e mycoil.wire.awg = 12)

    Parameters
    ----------
    awg : int, optional
        American Wire Gauge number for defining INNER diameter of wire, WITHOUT insulation (purely the conductor)
        Use awg OR d_in_mm. If both d_in_mm and awg are given, will take awg as default.
        For 'square' wire, it means the length of the square side. For 'foil' wire, it's useless.
    d_in_mm : float, optional
        INNER diameter of wire conductor, WITHOUT insulation (purely the conductor)
        Use awg OR d_in_mm. If both d_in_mm and awg are given, will take awg as default.
        For 'square' wire, it means the length of the square side. For 'foil' wire, it's useless.
    t_insulation_mm : float, optional
        Thickness of insulation material, in mm. Default is 0.05mm (corresponding to a safe choice for class 3 of AWG20)
    shape : str|culib.WireShape, optional
        Shape of the wire cross section. Supported are 'round', 'square' and 'foil'. Default is 'round'.
    material : str|culib.Material, optional
        Material of the conductor wire. Supported are 'copper' and 'aluminum'. Default is 'copper'.
    temp_degC : float, optional
        Wire temperature for calculating resistivity, in degC. Default is 20degC
    r_curv_squarecorner_mm : float, optional
        Radius of curvature of rounded corners for a 'square' shaped wire, in mm. If not specified, default will be 15% of d_in_mm.
        Unused for other shapes.
    L_foil_mm : float, optional
        Length of the foil wire, in mm. Unused for other shapes.
    t_foil_mm : float, optional
        Thickness of the foil wire, in mm. Unused for other shapes.
    is_autorecalc : bool, optional
        Enable or disable automatic wire parameters calculation. Default is True.
        If False, need to manually call calculation sequences for getting a wire parameter.
        Use it if you know what you are doing.

    Attributes
    ----------
    Params
        All parameters given at init +
    d_out_mm : float
        Calculated diameter WITH insulation layer, in mm.
    t_insulation_recommended_mm : float
        Recommended wire insulation thickness vs wire size, for the maximum grade 3 insulation, in mm
    section_area_mm2 : float
        Section area of conductor, without insulation, in mm^2
    temp_coef_resistivity_perdegC : float
        Coefficient of resistivity raise vs temperature, in 1/degC. Function of (material)
    rho_resistivity_meterohm : float
        Material electrical resistivity, in m.Ohm. Function of (material, temp_degC).
    eta_linres_meterperohm : float
        Wire lineic electrical resistivity, in m/Ohm. Function of (material, section_area_mm2, temp_degC).
    mass_lindensity_gperm : float
        Wire lineic mass density, in g/m. Function of (material, section_area_mm2).

    Examples
    --------
    ## Define a wire, to attach it on a coil

    >>> import culib as cul
    >>> my_awg_wire = cul.wires.Wire(awg=20, shape='round', t_insulation_mm=0.05)
    >>> my_coil = cul.CircularCoil(
    ...     wire = my_awg_wire,
    ...     axis = 'x_mm',
    ...     r_out_mm = 50+5,
    ...     r_in_mm = 50-5,
    ...     L_mm = 15,
    ...     pos_mm = -50/2,
    ... )

    ## Get section area of AWG 12 round wire

    >>> cul.wires.Wire(awg=12, shape='round').section_area_mm2
    3.310

    ## Define a square shaped wire out of aluminum

    >>> my_wire = cul.wires.Wire(material='aluminum', d_in_mm=1.024, shape='square', r_curv_squarecorner_mm = 0.16)

    ## Get lineic resistivity of a FOIL wire

    >>> cul.wires.Wire(shape='foil', t_foil_mm = 0.1, L_foil_mm = 5).eta_linres_ohmperm
    0.0336

    ## Oops I forgot to declare inner size of my round wire

    >>> my_wire = cul.wires.Wire(shape='round', t_insulation_mm=0.1)
    Traceback (most recent call last):
    ValueError: neither d_in_mm nor AWG are specified. Must define one or another at least.

    """

    def __init__(
        self,
        awg: int | str = None,
        d_in_mm: float = None,
        t_insulation_mm: float = DEFAULT_T_INSULATION_MM,
        shape: str | WireShape = DEFAULT_SHAPE,
        material: str | Material = DEFAULT_MATERIAL,
        temp_degC: float = DEFAULT_TEMP_DEGC,
        r_curv_squarecorner_mm: float = None,
        L_foil_mm: float = None,
        t_foil_mm: float = None,
        is_autorecalc: bool = True,
        logger: logging.Logger = None,
    ):
        self.log = logger if logger else get_local_logger("Wire")

        # Get as-is attributes
        self._is_autorecalc = is_autorecalc
        self._validate_temp_degC(temp_degC)  # Will set self._temp_degC
        self._validate_shape(shape)  # Will set self._shape
        self._validate_material(material)  # Will set self,_material

        ## Manage firsts deductions from shapes
        if self._shape in (WireShape.ROUND, WireShape.SQUARE):
            if d_in_mm is None and awg is None:
                err_msg = "neither d_in_mm nor AWG are specified. Must define one or another at least."
                self.log.error(err_msg)
                raise ValueError(err_msg)
            elif d_in_mm is not None and awg is None:
                self.log.debug("selected d_in_mm as definition (not AWG)")
                self._validate_d_in_mm(d_in_mm)
                self._awg = None
            elif awg is not None:
                if d_in_mm is not None:
                    self.log.warning("both d_in_mm and AWG are given. Taking AWG as default definition.")  # fmt:skip
                self.log.debug("selected AWG as wire definition, deducting d_in_mm from data_wires dict")  # fmt:skip
                self._validate_awg(awg)
                self._validate_d_in_mm(DICT_D_WIRE_IN_MM_VS_AWG[awg])
        elif self._shape in (WireShape.FOIL):
            if L_foil_mm is None or t_foil_mm is None:
                err_msg = "foil wire selected but L_foil_mm or t_foil_mm not specified"
                self.log.error(err_msg)
                raise ValueError(err_msg)
            self._validate_L_foil_mm(L_foil_mm)
            self._validate_t_foil_mm(t_foil_mm)

        ## Manage specifc square shape
        self._validate_r_curv_squarecorner_mm(r_curv_squarecorner_mm)

        ## Manage insulation thickness
        self._t_insulation_recommended_mm = self.get_recommended_insulation_thickness()
        self._validate_t_insulation_mm(t_insulation_mm)

        # Deduct parameters from calc
        self.calc_d_out_mm()
        self.calc_section_area_mm2()
        self.get_temp_coef_resistivity_perdegC()
        self.calc_rho_resistivity_meterohm()
        self.calc_eta_linres_ohmperm()
        self.calc_mass_lindensity_gperm()

    ### PROPERTIES ###
    @property
    def is_autorecalc(self):
        return self._is_autorecalc

    @is_autorecalc.setter
    def is_autorecalc(self, value):
        self._is_autorecalc = value
        if self._is_autorecalc:
            self.calc_d_out_mm()
            self.calc_section_area_mm2()
            self.get_temp_coef_resistivity_perdegC()
            self.calc_rho_resistivity_meterohm()
            self.calc_eta_linres_ohmperm()
            self.calc_mass_lindensity_gperm()
            self.trigger_all_coil_param_recalc_func()

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._validate_shape(value)
        if self.is_autorecalc:
            self._validate_r_curv_squarecorner_mm(self._r_curv_squarecorner_mm)
            self.calc_d_out_mm()
            self.calc_section_area_mm2()
            self.calc_eta_linres_ohmperm()
            self.calc_mass_lindensity_gperm()
            self.trigger_all_coil_param_recalc_func()

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        self._validate_material(value)
        if self.is_autorecalc:
            self.get_temp_coef_resistivity_perdegC()
            self.calc_rho_resistivity_meterohm()
            self.calc_eta_linres_ohmperm()
            self.calc_mass_lindensity_gperm()
            self.trigger_all_coil_param_recalc_func()

    @property
    def temp_degC(self):
        return self._temp_degC

    @temp_degC.setter
    def temp_degC(self, value):
        self._validate_temp_degC(value)
        if self.is_autorecalc:
            self.calc_rho_resistivity_meterohm()
            self.calc_eta_linres_ohmperm()
            self.trigger_elec_coil_param_recalc_func()

    @property
    def awg(self):
        return self._awg

    @awg.setter
    def awg(self, value):
        self._validate_awg(value)
        if self.is_autorecalc:
            self._d_in_mm = DICT_D_WIRE_IN_MM_VS_AWG[value]
            self._t_insulation_recommended_mm = get_recommended_insulation_thickness(
                self._d_in_mm
            )
            self._validate_r_curv_squarecorner_mm(self._r_curv_squarecorner_mm)
            self.calc_d_out_mm()
            self.calc_section_area_mm2()
            self.calc_eta_linres_ohmperm()
            self.calc_mass_lindensity_gperm()
            self.trigger_all_coil_param_recalc_func()

    @property
    def d_in_mm(self):
        return self._d_in_mm

    @d_in_mm.setter
    def d_in_mm(self, value):
        if self.awg is not None:
            err_msg = "an AWG number is already defined. Change AWG or create another wire if you want to change directly d_in_mm"
            raise ValueError(err_msg)
        else:
            self._validate_d_in_mm(value)
            if self.is_autorecalc:
                self._t_insulation_recommended_mm = (
                    get_recommended_insulation_thickness(value)
                )
                self._validate_t_insulation_mm(self._t_insulation_mm)
                self.calc_d_out_mm()
                self.calc_section_area_mm2()
                self.calc_eta_linres_ohmperm()
                self.calc_mass_lindensity_gperm()
                self.trigger_all_coil_param_recalc_func()

    @property
    def t_insulation_mm(self):
        return self._t_insulation_mm

    @t_insulation_mm.setter
    def t_insulation_mm(self, value):
        self._validate_t_insulation_mm(value)
        if self.is_autorecalc:
            self.calc_d_out_mm()
            self.trigger_all_coil_param_recalc_func()

    @property
    def t_insulation_recommended_mm(self):
        self._t_insulation_recommended_mm = self.get_recommended_insulation_thickness()
        return self._t_insulation_recommended_mm

    @t_insulation_recommended_mm.setter
    def t_insulation_recommended_mm(self, value):
        err_msg = "cannot set t_insulation_recommended_mm directly"
        self.log.error(err_msg)
        raise AttributeError(err_msg)

    @property
    def r_curv_squarecorner_mm(self):
        return self._r_curv_squarecorner_mm

    @r_curv_squarecorner_mm.setter
    def r_curv_squarecorner_mm(self, value):
        self._validate_r_curv_squarecorner_mm(value)
        if self.is_autorecalc:
            self.calc_section_area_mm2()
            self.calc_eta_linres_ohmperm()
            self.calc_mass_lindensity_gperm()
            self.trigger_all_coil_param_recalc_func()

    @property
    def L_foil_mm(self):
        return self._L_foil_mm

    @L_foil_mm.setter
    def L_foil_mm(self, value):
        if self._shape != WireShape.FOIL:
            self.log.warning(f"L_foil_mm changed but current wire shape is {self._shape}. Skipping operation. Consider using dedicated FoilWire() object for liability.")  # fmt:skip
        else:
            self._validate_L_foil_mm(value)
            if self.is_autorecalc:
                self._t_insulation_recommended_mm = (
                    get_recommended_insulation_thickness(value / 10)
                )
                self._validate_t_insulation_mm(self._t_insulation_mm)
                self.calc_section_area_mm2()
                self.calc_eta_linres_ohmperm()
                self.calc_mass_lindensity_gperm()
                self.trigger_all_coil_param_recalc_func()

    @property
    def t_foil_mm(self):
        return self._t_foil_mm

    @t_foil_mm.setter
    def t_foil_mm(self, value):
        if self._shape != WireShape.FOIL:
            self.log.warning(f"t_foil_mm changed but current wire shape is {self.shape}. Skipping operation. Consider using dedicated FoilWire() object for liability.")  # fmt:skip
        else:
            self._validate_t_foil_mm(value)
            if self.is_autorecalc:
                self.calc_section_area_mm2()
                self.calc_eta_linres_ohmperm()
                self.calc_mass_lindensity_gperm()
                self.trigger_all_coil_param_recalc_func()

    @property
    def d_out_mm(self):
        return self._d_out_mm

    @d_out_mm.setter
    def d_out_mm(self, value):
        err_msg = "cannot set d_out_mm directly. It's a function of d_in_mm and t_insulation_mm. Consider changing them to change d_out_mm."
        self.log.error(err_msg)
        raise AttributeError(err_msg)

    @property
    def section_area_mm2(self):
        return self._section_area_mm2

    @section_area_mm2.setter
    def section_area_mm2(self, value):
        err_msg = "cannot set section_area_mm2 directly. It's a function of shape and d_in_mm / foils params. Consider changing them to change section_area_mm2."
        self.log.error(err_msg)
        raise AttributeError(err_msg)

    @property
    def temp_coef_resistivity_perdegC(self):
        return self._temp_coef_resistivity_perdegC

    @temp_coef_resistivity_perdegC.setter
    def temp_coef_resistivity_perdegC(self, value):
        err_msg = "cannot set temp_coef_resistivity_perdegC directly. It's a function of material. Consider changing it to change temp_coef_resistivity_perdegC."
        self.log.error(err_msg)
        raise AttributeError(err_msg)

    @property
    def rho_resistivity_meterohm(self):
        return self._rho_resistivity_meterohm

    @rho_resistivity_meterohm.setter
    def rho_resistivity_meterohm(self, value):
        err_msg = "cannot set rho_resistivity_meterohm directly. It's a function of material and temp_degC. Consider changing them to change rho_resistivity_meterohm."
        self.log.error(err_msg)
        raise AttributeError(err_msg)

    @property
    def eta_linres_ohmperm(self):
        return self._eta_linres_ohmperm

    @eta_linres_ohmperm.setter
    def eta_linres_ohmperm(self, value):
        err_msg = "cannot set eta_linres_ohmperm directly. It's a function of material, shape, temp_degC and d_in_mm / foils params. Consider changing them to change eta_linres_ohmperm."
        self.log.error(err_msg)
        raise AttributeError(err_msg)

    @property
    def mass_lindensity_gperm(self):
        return self._mass_lindensity_gperm

    @mass_lindensity_gperm.setter
    def mass_lindensity_gperm(self, value):
        err_msg = "cannot set mass_lindensity_kgperm directly. It's a function of material, shape and d_in_mm / foils params. Consider changing them to change mass_lindensity_kgperm."
        self.log.error(err_msg)
        raise AttributeError(err_msg)

    ### METHODS ###
    # Define generic methods for representing the wire as a dict of all its parameters
    def __repr__(self):
        ret_dict = self.__dict__.copy()

        # List keys to remove (attached functions otherwise will create mess...)
        list_func_keys_to_remove = [
            key for key in ret_dict if isinstance(ret_dict[key], MethodType)
        ]
        for key in list_func_keys_to_remove:
            ret_dict.pop(key)
        # Remove the '_' prefix at the beginning of "private" params for readability
        list_keys_to_correct = [key for key in ret_dict if key.startswith("_")]
        for key in list_keys_to_correct:
            ret_dict[key[1:]] = ret_dict[key]
            ret_dict.pop(key)
        # Round floats for readability (up to 3 digits after comma, otherwise display as scientific notation)
        for key in ret_dict.keys():
            if type(ret_dict[key]) in (float, np.float64):
                rounded_value = round(ret_dict[key], 3)
                if rounded_value != 0.0:
                    ret_dict[key] = rounded_value
                else:
                    ret_dict[key] = f"{Decimal(ret_dict[key]):.3e}"
        # Sort alphabetically and return dict as str
        ret_dict = dict(sorted(ret_dict.items()))

        return str(ret_dict).replace(",", ",\n")

    # Define inputs validation methods
    def _validate_shape(self, shape) -> None:
        shape = shape.lower()
        if shape in LIST_WIRE_SHAPES:
            self._shape = shape
        else:
            err_msg = f"unknown wire shape selected. Supported wire shapes are : {LIST_WIRE_SHAPES}. Gave : {shape}"
            self.log.error(err_msg)
            raise ValueError(err_msg)

    def _validate_material(self, material) -> None:
        material = material.lower()
        if material in LIST_WIRE_MATERIALS:
            self._material = material
        else:
            err_msg = f"unknown wire material selected. Supported wire material are : {LIST_WIRE_MATERIALS}. Gave : {material}"
            self.log.error(err_msg)
            raise ValueError(err_msg)

    def _validate_temp_degC(self, temp_degC) -> None:
        self._temp_degC = validate_num_param(
            temp_degC, "temp_degC", "wire temperature", self.log
        )

    def _validate_d_in_mm(self, d_in_mm) -> None:
        self._d_in_mm = validate_positive_num_param(
            d_in_mm, "d_in_mm", "inner diameter", self.log
        )

    def _validate_awg(self, awg) -> None:
        if awg in DICT_D_WIRE_IN_MM_VS_AWG.keys():
            self._awg = awg
        else:
            err_msg = f"unsupported AWG number specified (AWG {awg}). Supported are int from {min(DICT_D_WIRE_IN_MM_VS_AWG.keys())} to {max(DICT_D_WIRE_IN_MM_VS_AWG.keys())}"
            self.log.error(err_msg)
            raise KeyError(err_msg)

    def _validate_t_insulation_mm(
        self, t_insulation_mm: float, is_check_recommendation: bool = True
    ) -> None:
        # if t_insulation_mm is not None:
        self._t_insulation_mm = validate_positive_num_param(
            t_insulation_mm, "t_insulation_mm", "insulation thickness", self.log
        )
        if is_check_recommendation:
            if self._t_insulation_mm < self._t_insulation_recommended_mm:
                warn_msg = f"insulation thickness specified ({self._t_insulation_mm:.3f} mm) is lower than recommendation by IEC norms {self._t_insulation_recommended_mm:.3f} mm for this case. Consider increasing it."
                self.log.warning(warn_msg)

    def _validate_r_curv_squarecorner_mm(self, r_curv_squarecorner_mm) -> None:
        # If required (for SQUARE shape) : calc default if None and check it's valid
        if self._shape == WireShape.SQUARE:
            if r_curv_squarecorner_mm is None:
                r_curv_squarecorner_mm = 0.15 * self.d_in_mm
                self.log.warning(f"selected wire shape '{self.shape}' but did not specified radius of curvature of rounded corners. Taking default 15% of d_in_mm : r_curv_squarecorner_mm = {r_curv_squarecorner_mm:.3f}")  # fmt:skip
            self._r_curv_squarecorner_mm = validate_positive_num_param(
                r_curv_squarecorner_mm,
                "r_curv_squarecorner_mm",
                "radius of curvature",
                self.log,
            )
        # For other shapes: let as is (no valid needed as won't be used), can be None
        else:
            self._r_curv_squarecorner_mm = r_curv_squarecorner_mm

    def _validate_L_foil_mm(self, L_foil_mm) -> None:
        self._L_foil_mm = validate_positive_num_param(
            L_foil_mm, "L_foil_mm", "foil length", self.log
        )

    def _validate_t_foil_mm(self, t_foil_mm) -> None:
        self._t_foil_mm = validate_positive_num_param(
            t_foil_mm, "t_foil_mm", "foil thickness", self.log
        )

    # Define calc methods from inputs
    def calc_d_out_mm(self) -> float:
        """
        Calc outer diamater from inner diameter and insulation thickness.
        Stores it in wire attribute "d_out_mm" and returns it in mm.
        """
        if self._shape in (WireShape.ROUND, WireShape.SQUARE):
            self._d_out_mm = self._d_in_mm + 2 * self._t_insulation_mm
            return self._d_out_mm

    def calc_section_area_mm2(self) -> float:
        """
        Calc conductor area (without insulation) from shape and geometric dimensions.
        Stores it in wire attribute "section_area_mm2" and returns it in mm^2.
        """
        if self._shape == WireShape.ROUND:
            self._section_area_mm2 = np.pi / 4 * self._d_in_mm**2
        elif self._shape == WireShape.SQUARE:
            self._section_area_mm2 = self._d_in_mm**2 - 0.8584 * self._r_curv_squarecorner_mm**2  # fmt:skip
        elif self._shape == WireShape.FOIL:
            self._section_area_mm2 = self._t_foil_mm * self._L_foil_mm
        else:
            err_msg = (
                f"unknown wire shape ({self.shape}). Cannot calculate section_area_mm2."
            )
            self.log.error(err_msg)
            raise NotImplementedError(err_msg)
        return self._section_area_mm2

    def get_temp_coef_resistivity_perdegC(self) -> float:
        """
        Get temperature resistivity variation coefficient vs reference temperature 20degC from material type.
        Stores it in wire attribute "temp_coef_resistivity_perdegC" and returns it (no unit)
        """
        self._temp_coef_resistivity_perdegC = DICT_TEMP_COEF_RESISTIVITY_PERDEGC_VS_MATERIAL[self._material]  # fmt:skip
        return self._temp_coef_resistivity_perdegC

    def calc_rho_resistivity_meterohm(self) -> float:
        """
        Calc electrical resisivity in m.ohm from material and temperature.
        Stores it in wire attribute "rho_resistivity_meterohm" and returns it in m.ohm
        """
        rho_resistivity_meterohm_at_20degC = DICT_RHO_RESISTIVITY_METEROHM_VS_MATERIAL[self._material]  # fmt:skip
        self._rho_resistivity_meterohm = rho_resistivity_meterohm_at_20degC * (
            1 + self._temp_coef_resistivity_perdegC * (self._temp_degC - 20)
        )
        return self._rho_resistivity_meterohm

    def calc_eta_linres_ohmperm(self) -> float:
        """
        Calc lineic resistance in ohm/m from resisivity and section area.
        Stores it in wire attribute "eta_linres_ohmperm" and returns it in ohm/m
        """
        self._eta_linres_ohmperm = self._rho_resistivity_meterohm / (
            self._section_area_mm2 * 1e-6
        )
        return self._eta_linres_ohmperm

    def calc_mass_lindensity_gperm(self) -> float:
        """
        Calc lineic mass density in g/m from material and section area.
        Stores it in wire attribute "mass_lindensity_gperm" and returns it in g/m
        """
        self._mass_lindensity_gperm = (
            DICT_MASS_DENSITY_GPERCM3_VS_MATERIAL[self._material]
            * self._section_area_mm2
        )
        return self._mass_lindensity_gperm

    def get_recommended_insulation_thickness(self) -> float:
        """
        Get recommended insulation thickness from IEC 60317 and AWG NEMA MW1000C norms for the maximum grade 3 insulation.
        Took the max values to get maximum safety margins.
        Reverse engineered relationship from data tables available here : https://www.elektrisola.com/en/Products/Enamelled-Wire/Technical-Data

        Returns
        -------
        t_insulation_mm : float
            Recommended insulation thickness for current wire in mm

        Examples
        --------
        ## Get recommended ins. thickness for AWG 24 (which should corresponds to ~0.05mm)

        >>> mywire = Wire(awg=24, shape="round")
        >>> mywire.get_recommended_insulation_thickness()
        0.04007228622443135
        """
        if self._shape in (WireShape.ROUND, WireShape.SQUARE):
            return get_recommended_insulation_thickness(self._d_in_mm)
        elif self._shape in (WireShape.FOIL):
            return get_recommended_insulation_thickness(self._L_foil_mm / 10)  # from XP

    # Define methods to be overriden for "communication" with coils
    def trigger_all_coil_param_recalc_func(self) -> None:
        pass

    def trigger_elec_coil_param_recalc_func(self) -> None:
        pass
