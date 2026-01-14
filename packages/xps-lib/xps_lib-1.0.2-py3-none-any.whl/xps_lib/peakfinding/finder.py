"""
Peak finding and element identification.

Automatically detects peaks in XPS spectra and suggests which elements
they might correspond to based on the reference database.
"""

from dataclasses import dataclass
from typing import Optional
from ..regions.reference import XPSReferenceDatabase, FittingRegionSuggestion

from typing import List, Tuple
import numpy as np


@dataclass
class DetectedPeak:
    """
    A peak detected in the spectrum.
    
    Attributes
    ----------
    center : float
        Peak center energy (eV)
    height : float
        Peak height (intensity)
    width : float
        Peak width estimate (eV)
    area : float
        Integrated peak area
    element_suggestions : List[Tuple[str, str, float]]
        List of (element, orbital, likelihood) suggestions
    """
    center: float
    height: float
    width: float
    area: float
    element_suggestions: List[Tuple[str, str, float]] = None


class PeakFinder:
    """
    Automatically detects peaks in XPS spectra.
    
    Uses scipy peak detection algorithms to find maxima and estimates their
    properties. Integrates with reference database to suggest element identities.
    """
    
    @staticmethod
    def find_peaks(dataset: 'XPSDataset',
                   prominence_threshold: float = 0.05,
                   min_width: float = 0.1) -> List[DetectedPeak]:
        """
        Find peaks in the spectrum.
        
        Parameters
        ----------
        dataset : XPSDataset
            Spectrum to analyze
        prominence_threshold : float
            Minimum peak prominence (relative to baseline)
        min_width : float
            Minimum peak width (eV)
            
        Returns
        -------
        List[DetectedPeak]
            Detected peaks with properties and element suggestions
        """
        pass
    
    @staticmethod
    def suggest_element_regions(detected_peaks: List[DetectedPeak],
                               reference_db: XPSReferenceDatabase
                               ) -> List[FittingRegionSuggestion]:
        """
        Suggest element regions based on detected peaks.
        
        For each detected peak, queries the reference database to suggest
        which elements and orbitals might be responsible.
        
        Parameters
        ----------
        detected_peaks : List[DetectedPeak]
            Peaks detected in the spectrum
        reference_db : XPSReferenceDatabase
            Reference database for lookup
            
        Returns
        -------
        List[FittingRegionSuggestion]
            Ranked suggestions for which elements/orbitals to analyze
        """
        pass


def find_element_region(dataset: 'XPSDataset',
                       reference_db: Optional[XPSReferenceDatabase] = None
                       ) -> Optional['ElementRegion']:
    """
    Interactive function to identify and suggest an element region.
    
    This is the main user-facing function for peak detection. It:
    1. Detects peaks in the dataset
    2. Queries the reference database
    3. Presents suggestions to the user
    4. Optionally returns a partially configured ElementRegion
    
    Parameters
    ----------
    dataset : XPSDataset
        Spectrum to analyze
    reference_db : XPSReferenceDatabase, optional
        Reference database. If None, uses default.
        
    Returns
    -------
    ElementRegion or None
        Suggested element region based on user selection, or None if user cancels
        
    Example
    -------
    >>> element = find_element_region(dataset)
    >>> if element:
    ...     print(f"Found {element.full_name} at {element.fitting_regions[0].energy_range}")
    """
    pass