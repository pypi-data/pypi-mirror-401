"""
Single-peak constraints for XPS fitting.

These constraints limit a single peak's parameters to fixed ranges,
useful for enforcing physical bounds like FWHM ranges and position ranges.
"""

from .base import Constraint
from lmfit import Parameters


class FWHMConstraint(Constraint):
    """
    Constrain FWHM (Full Width at Half Maximum) of a single peak to a range.
    
    Parameters
    ----------
    prefix : str
        Parameter prefix for the peak (e.g., 'p0_', 'p1_')
    min_fwhm : float
        Minimum allowed FWHM (eV)
    max_fwhm : float
        Maximum allowed FWHM (eV)
        
    Example
    -------
    >>> # Limit Si 2p 3/2 FWHM to 0.7-1.3 eV
    >>> constraint = FWHMConstraint("p0_", min_fwhm=0.7, max_fwhm=1.3)
    """
    
    def __init__(self, prefix: str, min_fwhm: float, max_fwhm: float):
        """Initialize FWHM constraint."""
        self.prefix = prefix if prefix.endswith("_") else prefix + "_"
        self.min_fwhm = min_fwhm
        self.max_fwhm = max_fwhm
        self.description = f"{self.prefix}sigma: FWHM {min_fwhm:.2f}-{max_fwhm:.2f} eV"
    
    def apply(self, params: Parameters) -> None:
        """
        Apply FWHM bounds by constraining sigma.
        
        For Gaussian: FWHM = 2.3548 * sigma
        For Lorentzian: FWHM = 2 * sigma
        
        We use the geometric mean as a compromise.
        """
        sigma_name = f'{self.prefix}sigma'
        
        if sigma_name not in params:
            raise KeyError(f"Parameter '{sigma_name}' not found")
        
        # Convert FWHM bounds to sigma bounds (using geometric mean)
        # For most lineshapes: FWHM ≈ 2.355 * sigma
        conversion_factor = 2.355
        min_sigma = self.min_fwhm / conversion_factor
        max_sigma = self.max_fwhm / conversion_factor
        
        params[sigma_name].min = min_sigma
        params[sigma_name].max = max_sigma


class PositionConstraint(Constraint):
    """
    Constrain position (center) of a single peak to a range.
    
    Parameters
    ----------
    prefix : str
        Parameter prefix for the peak (e.g., 'p0_', 'p1_')
    min_pos : float
        Minimum allowed position (eV)
    max_pos : float
        Maximum allowed position (eV)
        
    Example
    -------
    >>> # Limit C 1s position to 284-286 eV
    >>> constraint = PositionConstraint("p0_", min_pos=284, max_pos=286)
    """
    
    def __init__(self, prefix: str, min_pos: float, max_pos: float):
        """Initialize position constraint."""
        self.prefix = prefix if prefix.endswith("_") else prefix + "_"
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.description = f"{self.prefix}center: Position {min_pos:.2f}-{max_pos:.2f} eV"
    
    def apply(self, params: Parameters) -> None:
        """Apply position bounds to center parameter."""
        center_name = f'{self.prefix}center'
        
        if center_name not in params:
            raise KeyError(f"Parameter '{center_name}' not found")
        
        params[center_name].min = self.min_pos
        params[center_name].max = self.max_pos


class AmplitudeConstraint(Constraint):
    """
    Constrain amplitude (intensity) of a single peak to a range.
    
    Parameters
    ----------
    prefix : str
        Parameter prefix for the peak (e.g., 'p0_', 'p1_')
    min_amp : float
        Minimum allowed amplitude
    max_amp : float
        Maximum allowed amplitude
        
    Example
    -------
    >>> # Limit peak amplitude to 100-10000 counts
    >>> constraint = AmplitudeConstraint("p0_", min_amp=100, max_amp=10000)
    """
    
    def __init__(self, prefix: str, min_amp: float, max_amp: float):
        """Initialize amplitude constraint."""
        self.prefix = prefix if prefix.endswith("_") else prefix + "_"
        self.min_amp = min_amp
        self.max_amp = max_amp
        self.description = f"{self.prefix}amplitude: {min_amp:.2f}-{max_amp:.2f}"
    
    def apply(self, params: Parameters) -> None:
        """Apply amplitude bounds."""
        amp_name = f'{self.prefix}amplitude'
        
        if amp_name not in params:
            raise KeyError(f"Parameter '{amp_name}' not found")
        
        params[amp_name].min = self.min_amp
        params[amp_name].max = self.max_amp