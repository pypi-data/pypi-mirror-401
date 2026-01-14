import numpy as np
import pandas as pd
from typing import Optional, Tuple, List, Dict, Any
import plotly.graph_objects as go
from lmfit import Parameters

class Constraint:
    """Abstract base class for parameter constraints."""
    
    def __init__(self, description: str = ""):
        """Initialize constraint."""
        self.description = description
    
    def apply(self, params: Parameters) -> None:
        """Apply the constraint to parameters."""
        pass
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"{self.__class__.__name__}({self.description})"


class PositionConstraint(Constraint):
    """Constrain peak position: param2 = param1 + offset"""
    
    def __init__(self, param_name_base: str, param_name_constrained: str, 
                 offset: float, min_offset: Optional[float] = None,
                 max_offset: Optional[float] = None):
        """
        Create position constraint with optional bounds.
        
        Example: B_center = A_center + 13.2 eV for 2p1/2 vs 2p3/2
        With bounds: offset can vary between min_offset and max_offset
        
        Parameters
        ----------
        offset : float
            Target offset value
        min_offset : float, optional
            Minimum allowed offset
        max_offset : float, optional
            Maximum allowed offset
        """
        self.param_name_base = param_name_base
        self.param_name_constrained = param_name_constrained
        self.offset = offset
        self.min_offset = min_offset
        self.max_offset = max_offset
        
        if min_offset is not None and max_offset is not None:
            desc = f"{param_name_constrained} = {param_name_base} + {offset:.2f} " \
                   f"(range: {min_offset:.2f}-{max_offset:.2f})"
        else:
            desc = f"{param_name_constrained} = {param_name_base} + {offset:.2f}"
        super().__init__(desc)
    
    def apply(self, params: Parameters) -> None:
        """Apply: param_constrained = param_base + offset"""
        if self.param_name_base not in params:
            raise ValueError(f"Parameter {self.param_name_base} not found")
        if self.param_name_constrained not in params:
            raise ValueError(f"Parameter {self.param_name_constrained} not found")
        
        # Set expression
        params[self.param_name_constrained].expr = \
            f"{self.param_name_base} + {self.offset}"
        
        # Apply bounds if specified
        if self.min_offset is not None:
            params[self.param_name_constrained].min = \
                params[self.param_name_base].value + self.min_offset
        if self.max_offset is not None:
            params[self.param_name_constrained].max = \
                params[self.param_name_base].value + self.max_offset


class FWHMConstraint(Constraint):
    """Constrain peak width: param2 = param1 * ratio"""
    
    def __init__(self, param_name_base: str, param_name_constrained: str,
                 ratio: float = 1.0, min_ratio: Optional[float] = None,
                 max_ratio: Optional[float] = None):
        """
        Create FWHM constraint with optional bounds.
        
        Example: B_sigma = A_sigma * 1.0 for same width
        With bounds: ratio can vary between min_ratio and max_ratio
        
        Parameters
        ----------
        ratio : float
            Target ratio value
        min_ratio : float, optional
            Minimum allowed ratio
        max_ratio : float, optional
            Maximum allowed ratio
        """
        self.param_name_base = param_name_base
        self.param_name_constrained = param_name_constrained
        self.ratio = ratio
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio
        
        if min_ratio is not None and max_ratio is not None:
            desc = f"{param_name_constrained} = {param_name_base} * {ratio:.2f} " \
                   f"(range: {min_ratio:.2f}-{max_ratio:.2f})"
        else:
            desc = f"{param_name_constrained} = {param_name_base} * {ratio:.2f}"
        super().__init__(desc)
    
    def apply(self, params: Parameters) -> None:
        """Apply: param_constrained = param_base * ratio"""
        if self.param_name_base not in params:
            raise ValueError(f"Parameter {self.param_name_base} not found")
        if self.param_name_constrained not in params:
            raise ValueError(f"Parameter {self.param_name_constrained} not found")
        
        # Set expression
        params[self.param_name_constrained].expr = \
            f"{self.ratio} * {self.param_name_base}"
        
        # Apply bounds if specified
        if self.min_ratio is not None:
            params[self.param_name_constrained].min = \
                params[self.param_name_base].value * self.min_ratio
        if self.max_ratio is not None:
            params[self.param_name_constrained].max = \
                params[self.param_name_base].value * self.max_ratio


class AreaConstraint(Constraint):
    """
    Constrain peak area via amplitude ratio:
    p1_amplitude = p0_amplitude * ratio
    """

    def __init__(self, base_prefix: str, constrained_prefix: str,
                 area_ratio: float,
                 min_ratio: Optional[float] = None,
                 max_ratio: Optional[float] = None):

        self.base_prefix = base_prefix if base_prefix.endswith("_") else base_prefix + "_"
        self.constrained_prefix = (
            constrained_prefix if constrained_prefix.endswith("_")
            else constrained_prefix + "_"
        )

        self.area_ratio = area_ratio
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio

        desc = f"Area({self.constrained_prefix}) = Area({self.base_prefix}) * {area_ratio:.2f}"
        super().__init__(desc)

    def apply(self, params: Parameters) -> None:
        base_amp = f"{self.base_prefix}amplitude"
        constrained_amp = f"{self.constrained_prefix}amplitude"

        if base_amp not in params:
            raise ValueError(f"Parameter {base_amp} not found")
        if constrained_amp not in params:
            raise ValueError(f"Parameter {constrained_amp} not found")

        params[constrained_amp].expr = f"{base_amp} * {self.area_ratio}"

        if self.min_ratio is not None:
            params[constrained_amp].min = params[base_amp].value * self.min_ratio
        if self.max_ratio is not None:
            params[constrained_amp].max = params[base_amp].value * self.max_ratio



class RatioConstraint(Constraint):
    """Constrain any parameter with a fixed ratio: param2 = param1 * ratio"""
    
    def __init__(self, param_name_base: str, param_name_constrained: str,
                 ratio: float):
        """
        Create generic ratio constraint.
        
        This is more general than AreaConstraint and can be used for any parameter.
        """
        self.param_name_base = param_name_base
        self.param_name_constrained = param_name_constrained
        self.ratio = ratio
        
        desc = f"{param_name_constrained} = {param_name_base} * {ratio:.3f}"
        super().__init__(desc)
    
    def apply(self, params: Parameters) -> None:
        """Apply: param_constrained = param_base * ratio"""
        if self.param_name_base not in params:
            raise ValueError(f"Parameter {self.param_name_base} not found")
        if self.param_name_constrained not in params:
            raise ValueError(f"Parameter {self.param_name_constrained} not found")
        
        params[self.param_name_constrained].expr = \
            f"{self.ratio} * {self.param_name_base}"
