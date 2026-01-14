"""
Element suggester for automatic region configuration.

Uses peaks detected in a spectrum and the reference table to suggest
which elements are likely present.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
from .reference_table import ElementReferenceTable, XPSElementInfo
from ..core.dataset import XPSDataset
import numpy as np


@dataclass
class ElementSuggestion:
    """
    A suggestion for an element based on detected peaks.
    
    Attributes
    ----------
    element_info : XPSElementInfo
        Reference information for this element
    detected_position : float
        Position of detected peak (eV)
    distance_from_reference : float
        Distance from expected position (eV)
    confidence : float
        Confidence score 0-1 (1 = exact match)
    """
    
    element_info: XPSElementInfo
    detected_position: float
    distance_from_reference: float
    confidence: float
    energy_window: Tuple[float, float] = None


class ElementSuggester:
    """
    Suggests elements based on detected peaks and reference data.
    
    Analyzes peaks in a spectrum and compares them to a reference table.
    User can then manually create ElementRegion with the suggested parameters.
    """
    
    def __init__(self, reference_table: Optional[ElementReferenceTable] = None):
        """
        Initialize the suggester.
        
        Parameters
        ----------
        reference_table : ElementReferenceTable, optional
            Reference database. If None, creates a new one with defaults.
        """
        self.ref_table = reference_table or ElementReferenceTable()
        self.last_suggestions: List[ElementSuggestion] = []
    
    def find_element_region(self, dataset: XPSDataset) -> None:
        """
        Find and suggest element regions based on peaks in the dataset.
        
        Automatically detects peaks in the spectrum, compares them to the
        reference table, and prints a list of suggestions.
        
        Parameters
        ----------
        dataset : XPSDataset
            The XPS dataset to analyze
            
        Example
        -------
        >>> suggester = ElementSuggester()
        >>> suggester.find_element_region(dataset)
        # Prints suggestions like:
        # [1] Fe2p3/2    at 707.5 eV (confidence: 0.95)
        # [2] O1s        at 532.0 eV (confidence: 0.88)
        """
        from ..io.constants import ENERGY_COL, INTENSITY_COL
        from scipy.signal import find_peaks
        
        # Extract data
        x = dataset.df[ENERGY_COL].values
        y = dataset.df[INTENSITY_COL].values
        
        # Find peaks using scipy
        peaks, properties = find_peaks(
            y,
            prominence=np.max(y) * 0.05,
            width=0.5
        )
        
        detected_peaks = [(x[p], y[p]) for p in peaks]
        
        if not detected_peaks:
            print("No peaks detected in spectrum.")
            self.last_suggestions = []
            return
        
        # Generate suggestions
        suggestions = []
        for peak_pos, peak_height in detected_peaks:
            nearby = self.ref_table.find_by_binding_energy(peak_pos, tolerance=10.0)
            
            for elem_info in nearby:
                distance = abs(elem_info.binding_energy - peak_pos)
                confidence = max(0, 1.0 - (distance / 10.0))

                # Get energy window (custom if set, otherwise ±3 FWHM)
                energy_window = elem_info.get_energy_window()
                
                suggestion = ElementSuggestion(
                    element_info=elem_info,
                    detected_position=peak_pos,
                    distance_from_reference=distance,
                    confidence=confidence,
                    energy_window=energy_window
                )
                suggestions.append(suggestion)
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x.confidence, reverse=True)
        self.last_suggestions = suggestions
        
        # Print suggestions
        self._print_suggestions(suggestions)
    
    def _print_suggestions(self, suggestions: List[ElementSuggestion]) -> None:
        """
        Print suggestions in a formatted table.
        
        Parameters
        ----------
        suggestions : List[ElementSuggestion]
            Element suggestions to display
        """
        print("\n" + "="*130)
        print("XPS ELEMENT SUGGESTIONS")
        print("="*130)
        #print(f"{'#':<4} {'Element':<12} {'Detected':<12} {'Expected':<12} {'Distance':<10} "
        #      f"{'Confidence':<12} {'Energy Window':<20} {'Description':<35}")
        print(f"{'#':<4} {'Element':<12} {'Detected':<12} {'Expected':<12} {'Distance':<10} "
              f"{'Energy Window':<20}")
        print("-"*130)
        
        for i, sugg in enumerate(suggestions, 1):
            elem = sugg.element_info
            window_str = f"{sugg.energy_window[0]:.1f}-{sugg.energy_window[1]:.1f} eV"
            
            print(f"{i:<4} {elem.full_name:<12} {sugg.detected_position:<12.2f} "
                  f"{elem.binding_energy:<12.2f} {sugg.distance_from_reference:<10.3f} "
                  #f"{sugg.confidence:<12.1%} {window_str:<20} {elem.description:<35}")
                  f"{window_str:<20}")
        
        print("="*130)
        print("\nCreate ElementRegion and FittingRegion:")
        if suggestions:
            top = suggestions[0].element_info
            window = top.get_energy_window()
            
            print(f"\n# Element: {top.full_name}")
            print(f"element = ElementRegion(element='{top.element}', orbital='{top.orbital}', dataset=dataset)")
            print(f"\nregion = FittingRegion(")
            print(f"    name='{top.full_name}',")
            print(f"    energy_range=({window[0]:.1f}, {window[1]:.1f}),")
            print(f"    background_method='shirley',")
            #print(f"    description='{top.description}'")
            print(f")")
            print(f"element.add_fitting_region(region)")
        print()

    def get_element_window(self, element: str, orbital: str) -> Optional[Tuple[float, float]]:
        """
        Get the energy window for a specific element.
        
        Parameters
        ----------
        element : str
            Element symbol (e.g., 'C')
        orbital : str
            Orbital notation (e.g., '1s')
            
        Returns
        -------
        Tuple[float, float] or None
            (min_eV, max_eV) energy window, or None if not found
        """
        elem_info = self.get_element(element, orbital)
        if elem_info:
            return elem_info.get_energy_window()
        return None

