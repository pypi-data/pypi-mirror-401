"""
Reference table for XPS elements with typical parameters and suggestions.

Maintains a database of elements commonly analyzed in XPS with their
characteristic peaks, typical fitting parameters, and analysis tips.
"""

from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass, field
import numpy as np

@dataclass
class XPSElementInfo:
    """
    Reference information for a single XPS element/orbital.
    
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
        Descriptive name (e.g., 'Iron 2p3/2')
    sub_peaks : List[Dict]
        List of sub-peaks (e.g., spin-orbit splitting)
        Each dict contains: {'name': str, 'offset': float, 'area_ratio': float, ...}
    fitting_tips : List[str]
        Tips for fitting this element
    sensitivity_factor : float
        Relative sensitivity factor for quantification
    energy_window : Optional[Tuple[float, float]]
        Custom energy window (min, max) for fitting region.
        If None, uses ±3 FWHM from binding_energy.
    """
    
    element: str
    orbital: str
    binding_energy: float
    fwhm_typical: float
    description: str
    sub_peaks: List[Dict] = field(default_factory=list)
    fitting_tips: List[str] = field(default_factory=list)
    sensitivity_factor: float = 1.0
    energy_window: Optional[Tuple[float, float]] = None
    
    @property
    def full_name(self) -> str:
        """Return element+orbital identifier (e.g., 'Fe2p')."""
        return f"{self.element}{self.orbital}"

    def get_energy_window(self) -> Tuple[float, float]:
        """
        Get energy window for fitting region.
        
        Returns custom window if set, otherwise calculates ±3 FWHM.
        
        Returns
        -------
        Tuple[float, float]
            (min_eV, max_eV) energy range for fitting
        """
        if self.energy_window is not None:
            return self.energy_window
        
        # Fallback: ±3 FWHM
        window = self.fwhm_typical * 3
        return (self.binding_energy - window, self.binding_energy + window)




class ElementReferenceTable:
    """
    Reference database for XPS elements.
    
    Stores typical parameters for common XPS elements and provides
    methods to query and add to the database.
    """
    
    def __init__(self):
        """Initialize with standard XPS elements."""
        self.elements: Dict[str, XPSElementInfo] = {}
        self._populate_standard_elements()
    
    def _populate_standard_elements(self) -> None:
        """Populate with standard XPS elements and their parameters."""

        n_1s_info = XPSElementInfo(
            element='N',
            orbital='1s',
            binding_energy=397.9,
            fwhm_typical=0.9,
            description='Nitrogen 1s - AlN bonding',
            fitting_tips=['Single peak in AlN', 'GL(75) lineshape works well'],
            sensitivity_factor=1.8,  # Custom RSF for this sample
            energy_window=(391.0, 401.0)  # Exact window for fitting
        )
        self.add_element(n_1s_info)
    
        # Add Al 2p3/2 with custom window and RSF
        al_2p_3_2_info = XPSElementInfo(
            element='Al',
            orbital='2p3/2',
            binding_energy=73.5,
            fwhm_typical=0.8,
            description='Aluminum 2p3/2 - AlN bonding',
            sub_peaks=[
                {'name': 'Al 2p3/2', 'offset': 0, 'area_ratio': 1.0},
                {'name': 'Al 2p1/2', 'offset': 0.43, 'area_ratio': 0.5}
            ],
            fitting_tips=['GL(30) lineshape', 'Spin-orbit doublet with 2p1/2'],
            sensitivity_factor=0.55,  # Standard RSF for Al 2p
            energy_window=(69.9, 76.9)  # Exact window for fitting
        )
        self.add_element(al_2p_3_2_info)
    
        # Add Al 2p1/2 (for reference, but won't be used in quantification)
        al_2p_1_2_info = XPSElementInfo(
            element='Al',
            orbital='2p1/2',
            binding_energy=73.93,
            fwhm_typical=0.8,
            description='Aluminum 2p1/2 - Spin-orbit split',
            fitting_tips=['Constrained to Al 2p3/2'],
            sensitivity_factor=0.0,  # Set to 0 - don't use for quantification
            energy_window=(69.9, 76.9)
        )
        self.add_element(al_2p_1_2_info)
        
        # Iron (Fe) - very common in XPS
        self.add_element(XPSElementInfo(
            element='Fe',
            orbital='2p3/2',
            binding_energy=707.5,
            fwhm_typical=1.2,
            description='Iron 2p3/2 - Metallic and oxidized states',
            sub_peaks=[
                {'name': 'Fe metallic', 'offset': 0, 'area_ratio': 1.0},
                {'name': 'Fe oxide', 'offset': 0.7, 'area_ratio': 0.5}
            ],
            fitting_tips=[
                'Use Voigt profile for best results',
                'Common oxidation state offset: 0.7 eV',
                'Typical FWHM: 1.0-1.5 eV',
                'Use Shirley background for Fe 2p region',
            ],
            sensitivity_factor=295.763,
            energy_window=(700.0, 715.0)  # Custom window
        ))
        
        self.add_element(XPSElementInfo(
            element='Fe',
            orbital='2p1/2',
            binding_energy=720.7,
            fwhm_typical=1.2,
            description='Iron 2p1/2 - Spin-orbit split (13.2 eV)',
            fitting_tips=[
                'Spin-orbit splitting: ~13.2 eV from 2p3/2',
                'Similar width to 2p3/2',
                'Area ratio 2p1/2:2p3/2 ≈ 1:2',
            ],
            sensitivity_factor=295.763,
            energy_window=(715.0, 730.0)  # Custom window
        ))
        
        # Oxygen (O) - most common
        self.add_element(XPSElementInfo(
            element='O',
            orbital='1s',
            binding_energy=532.0,
            fwhm_typical=0.8,
            description='Oxygen 1s - Oxide and hydroxide',
            sub_peaks=[
                {'name': 'O oxide', 'offset': 0, 'area_ratio': 1.0},
                {'name': 'O-H hydroxide', 'offset': 1.2, 'area_ratio': 0.5}
            ],
            fitting_tips=[
                'Oxygen 1s is typically single peak or doublet',
                'Common offset for OH: 0.8-1.5 eV',
                'Use Shirley or linear background',
                'Typical FWHM: 0.7-1.0 eV',
            ],
            sensitivity_factor=2.88,
            energy_window=(528.0, 538.0)  # Custom window ±5 eV
        ))
        
        # Carbon (C) - reference peak and contamination
        self.add_element(XPSElementInfo(
            element='C',
            orbital='1s',
            binding_energy=284.8,
            fwhm_typical=0.7,
            description='Carbon 1s - Common reference peak',
            sub_peaks=[
                {'name': 'C-C hydrocarbon', 'offset': 0, 'area_ratio': 1.0},
                {'name': 'C-O ether', 'offset': 1.5, 'area_ratio': 0.3},
            ],
            fitting_tips=[
                'Typical reference peak at 284.8 eV for charging correction',
                'Multiple oxidation states common',
                'Typical FWHM: 0.6-0.9 eV',
            ],
            sensitivity_factor=1,
            energy_window=(280.0, 290.0)  # Custom window ±5 eV
        ))
        
        """# Nitrogen (N)
        self.add_element(XPSElementInfo(
            element='N',
            orbital='1s',
            binding_energy=397.9,
            fwhm_typical=0.9,
            description='Nitrogen 1s',
            fitting_tips=[
                'Different N bonding states: ~2 eV apart',
                'Typical FWHM: 0.8-1.2 eV',
            ],
            sensitivity_factor=68.671,
            energy_window=(395.0, 410.0)  # Custom window ±6 eV
        ))"""
        
        # Copper (Cu)
        self.add_element(XPSElementInfo(
            element='Cu',
            orbital='2p3/2',
            binding_energy=932.6,
            fwhm_typical=1.1,
            description='Copper 2p3/2 - Cu(I) and Cu(II)',
            sub_peaks=[
                {'name': 'Cu(I)', 'offset': 0, 'area_ratio': 1.0},
                {'name': 'Cu(II)', 'offset': 1.4, 'area_ratio': 1.0}
            ],
            fitting_tips=[
                'Cu(II) has characteristic shake-up satellite',
                'Typical FWHM: 1.0-1.5 eV',
            ],
            sensitivity_factor=396.777,
            energy_window=(925.0, 945.0)  # Custom window
        ))

        # Si
        self.add_element(XPSElementInfo(
            element='Si',
            orbital='2p',
            binding_energy=103.5,
            fwhm_typical=1.1,
            description='Copper 2p3/2 - Cu(I) and Cu(II)',
            sub_peaks=[
                {'name': 'Cu(I)', 'offset': 0, 'area_ratio': 1.0},
                {'name': 'Cu(II)', 'offset': 1.4, 'area_ratio': 1.0}
            ],
            fitting_tips=[
                'Cu(II) has characteristic shake-up satellite',
                'Typical FWHM: 1.0-1.5 eV',
            ],
            sensitivity_factor=1.06,
            energy_window=(95, 111)  # Custom window
        ))

        # Gallium 3d
        self.add_element(XPSElementInfo(
            element='Ga',
            orbital='3d',
            binding_energy=20.5,
            fwhm_typical=1.0,
            description='Gallium 3d - Metallic and oxide states',
            sub_peaks=[
                {'name': 'Ga metal', 'offset': 0, 'area_ratio': 1.0},
                {'name': 'Ga oxide', 'offset': 1.8, 'area_ratio': 1.5}
            ],
            fitting_tips=[
                'Ga3d typically shows metal and oxide components',
                'Oxide is ~1.5-2.0 eV higher',
                'FWHM: 0.9-1.3 eV',
            ],
            sensitivity_factor=150.0,
            energy_window=(15.0, 35.0)  # Custom window ±10 eV
        ))

    def add_element(self, element_info: XPSElementInfo) -> None:

        key = element_info.full_name
        self.elements[key] = element_info

    def get_element(self, element: str, orbital: str) -> Optional[XPSElementInfo]:

        key = f"{element}{orbital}"
        return self.elements.get(key)
    
    def find_by_binding_energy(self, binding_energy: float, 
                              tolerance: float = 5.0) -> List[XPSElementInfo]:
        """
        Find elements near a specific binding energy.
        
        Parameters
        ----------
        binding_energy : float
            Target binding energy (eV)
        tolerance : float
            Search window (eV)
            
        Returns
        -------
        List[XPSElementInfo]
            Elements found, sorted by distance from target
        """
        results = []
        for elem_info in self.elements.values():
            if abs(elem_info.binding_energy - binding_energy) <= tolerance:
                results.append(elem_info)
        
        # Sort by distance
        results.sort(key=lambda x: abs(x.binding_energy - binding_energy))
        return results
    
    def set_energy_window(self, element: str, orbital: str, 
                         min_eV: float, max_eV: float) -> None:
        """
        Set custom energy window for an element.
        
        Use this to override the default ±3 FWHM window with exact values
        provided by your boss or based on your data.
        
        Parameters
        ----------
        element : str
            Element symbol (e.g., 'C')
        orbital : str
            Orbital notation (e.g., '1s')
        min_eV : float
            Minimum energy (eV)
        max_eV : float
            Maximum energy (eV)
            
        Example
        -------
        >>> ref_table = ElementReferenceTable()
        >>> ref_table.set_energy_window('C', '1s', 280.0, 290.0)
        >>> ref_table.set_energy_window('O', '1s', 528.0, 538.0)
        """
        elem_info = self.get_element(element, orbital)
        if elem_info is None:
            print(f"Warning: {element}{orbital} not found in reference table")
            return
        
        elem_info.energy_window = (min_eV, max_eV)
        print(f"✓ Updated {element}{orbital} energy window: {min_eV:.1f} - {max_eV:.1f} eV")
