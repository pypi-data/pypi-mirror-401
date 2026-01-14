"""
Reference database and element region suggestions.

Maintains a database of known XPS lines with expected binding energies
and typical fitting parameters. Used to auto-suggest regions and constraints.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class XPSLineReference:
    """
    Reference data for a single XPS spectral line.
    
    Attributes
    ----------
    element : str
        Element symbol (e.g., 'Fe', 'O', 'C')
    orbital : str
        Orbital notation (e.g., '2p', '3s', '1s')
    binding_energy : float
        Typical binding energy (eV)
    fwhm_typical : float
        Typical full-width at half-maximum (eV)
    description : str
        Descriptive name (e.g., 'Fe 2p3/2', 'O 1s')
    common_satellites : List[float]
        Known satellite/shake-up energies relative to main peak (eV)
    """
    
    element: str
    orbital: str
    binding_energy: float
    fwhm_typical: float
    description: str
    common_satellites: List[float] = None


@dataclass
class FittingRegionSuggestion:
    """
    Suggested fitting region for an identified peak.
    
    Attributes
    ----------
    element : str
        Element symbol
    orbital : str
        Orbital notation
    energy_range : Tuple[float, float]
        Suggested (min, max) energy range (eV)
    suggested_n_peaks : int
        How many peaks to fit (1 for simple, 2+ for multiplets/oxidation states)
    description : str
        Human-readable description
    typical_constraints : List[str]
        Suggested constraint types ('equality_sigma', 'offset_center', etc.)
    """
    
    element: str
    orbital: str
    energy_range: Tuple[float, float]
    suggested_n_peaks: int
    description: str
    typical_constraints: List[str]


class XPSReferenceDatabase:
    """
    Database of known XPS lines and fitting parameters.
    
    Maintains comprehensive reference data for common XPS lines and provides
    methods to find and suggest appropriate fitting strategies.
    """
    
    def __init__(self):
        """Initialize the reference database with standard XPS lines."""
        pass
    
    def find_nearby_peaks(self, energy: float, window: float = 5.0,
                         element: Optional[str] = None) -> List[XPSLineReference]:
        """
        Find reference peaks near a given energy.
        
        Useful for identifying which elements might be responsible for observed
        peaks in the spectrum.
        
        Parameters
        ----------
        energy : float
            Energy to search around (eV)
        window : float
            Search window width (eV)
        element : str, optional
            If provided, only search for this element
            
        Returns
        -------
        List[XPSLineReference]
            List of reference peaks sorted by proximity to energy
        """
        pass
    
    def get_line_reference(self, element: str, orbital: str) -> Optional[XPSLineReference]:
        """
        Get reference data for a specific XPS line.
        
        Parameters
        ----------
        element : str
            Element symbol (e.g., 'Fe')
        orbital : str
            Orbital notation (e.g., '2p')
            
        Returns
        -------
        XPSLineReference or None
            Reference data if found, None otherwise
        """
        pass
    
    def suggest_fitting_region(self, element: str, orbital: str,
                              binding_energy: Optional[float] = None
                              ) -> Optional[FittingRegionSuggestion]:
        """
        Get suggested fitting region for an element.
        
        Parameters
        ----------
        element : str
            Element symbol
        orbital : str
            Orbital notation
        binding_energy : float, optional
            Observed binding energy (if provided, will tailor suggestions)
            
        Returns
        -------
        FittingRegionSuggestion or None
            Fitting suggestions if available
        """
        pass

