"""
Standard constraint implementations.

Contains common constraint types needed in XPS analysis.
"""

from .base import Constraint
from lmfit import Parameters

class PositionConstraint(Constraint):
    """
    Enforce that one parameter equals another plus a fixed offset.
    
    Example: center2 = center1 + 0.5 eV (for doublet)
    Example: sigma2 = sigma1 + 0.1 eV (different widths)
    
    Attributes
    ----------
    param_name_base : str
        Reference parameter name
    param_name_offset : str
        Parameter to constrain
    offset : float
        Fixed offset value (same units as parameter)
    description : str
        Automatically generated description
    """
    
    def __init__(self, param_name_base: str, param_name_offset: str, 
                 offset: float):
        """
        Create an offset constraint.
        
        Parameters
        ----------
        param_name_base : str
            Reference parameter name
        param_name_offset : str
            Parameter to constrain
        offset : float
            Fixed offset (can be positive or negative)
        """
        self.param_name_base = param_name_base
        self.param_name_offset = param_name_offset
        self.offset = offset
        self.description = f"{param_name_offset} = {param_name_base} + {offset}"
    
    def apply(self, params: Parameters) -> None:
        """Set param_name_offset.expr = param_name_base + offset."""
        if self.param_name_base not in params:
            raise ValueError(f"Parameter {self.param_name_base} not found in params")
        if self.param_name_offset not in params:
            raise ValueError(f"Parameter {self.param_name_offset} not found in params")
        
        params[self.param_name_offset].expr = f"{self.param_name_base} + {self.offset}"


class AreaConstraint(Constraint):
    
    def __init__(self, param_name_base: str, param_name_scaled: str, 
                 area_ratio: float):
        """
        Create an area constraint.
        
        Parameters
        ----------
        param_name_base : str
            Reference parameter name
        param_name_scaled : str
            Parameter to constrain
        ratio : float
            Multiplication factor
        """
        self.param_name_base = param_name_base
        self.param_name_scaled = param_name_scaled
        self.area_ratio = area_ratio
        self.description = f"Area({param_name_scaled}) = {area_ratio} * Area({param_name_base})"

    
    def apply(self, params: Parameters) -> None:
        if self.param_name_base not in params:
            raise ValueError(f"Parameter {self.param_name_base} not found")
        if self.param_name_scaled not in params:
            raise ValueError(f"Parameter {self.param_name_scaled} not found")
        
        params[self.param_name_scaled].expr = f"{self.area_ratio} * {self.param_name_base}"

