"""
Element region definitions and operations.

An element region is the top-level container for all analysis of a single
element (and orbital), typically processed in one Jupyter notebook cell.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any

from .fittingregion import FittingRegion

from .fittingregion import FittingRegion
from .peakstack import XPSPeakStack
from ..lineshapes.standard import VoigtLineShape
from ..constraints.standard import PositionConstraint, AreaConstraint
from ..elements.reference_table import ElementReferenceTable


@dataclass
class ElementRegion:
    """
    Top-level container for a single element orbital analysis.
    
    Each ElementRegion should be processed in its own Jupyter cell and
    represents the complete analysis workflow for one element.
    
    Attributes
    ----------
    element : str
        Element symbol (e.g., 'Fe', 'O', 'C')
    orbital : str
        Orbital notation (e.g., '2p', '3s', '1s')
    fitting_regions : List[FittingRegion]
        Energy ranges to fit (typically 1-2 for simple peaks, more for complex multiplets)
    dataset : Optional[Any]
        Reference to underlying XPSDataset
    notes : str
        Analysis notes and metadata
    """
    
    def __init__(self, element: str, orbital: str,
                 dataset: Optional['XPSDataset'] = None,
                 fitting_regions: Optional[List[FittingRegion]] = None):
        """Initialize element region."""
        self.element = element
        self.orbital = orbital
        self.dataset = dataset
        self.fitting_regions: List[FittingRegion] = fitting_regions or []
        self.notes = ""

    def __post_init__(self):
        """Auto-configure fitting regions if not provided."""
        if not self.fitting_regions:
            self._auto_configure_from_reference()
    
    def _auto_configure_from_reference(self) -> None:
        """
        Automatically configure fitting regions based on reference table.
        
        Creates fitting regions with appropriate energy ranges, peak stacks,
        and constraints based on the element's reference data.
        """
        ref_table = ElementReferenceTable()
        elem_info = ref_table.get_element(self.element, self.orbital)
        
        if not elem_info:
            # Element not in reference table - create minimal config
            print(f"Warning: {self.element}{self.orbital} not in reference table. "
                  f"Creating minimal configuration.")
            region = FittingRegion(
                name=f"{self.element}{self.orbital}",
                energy_range=(0, 100),  # User must adjust this
                background_method='shirley'
            )
            stack = XPSPeakStack(name=f"{self.element}{self.orbital}_peak")
            stack.add_line_shape(VoigtLineShape(f'{self.element}', prefix='p0_'))
            region.add_peak_stack(stack)
            self.fitting_regions.append(region)
            return
        
        # Create fitting region
        energy_window = elem_info.fwhm_typical * 3  # ±3 FWHM
        region = FittingRegion(
            name=f"{self.element}{self.orbital}",
            energy_range=(
                elem_info.binding_energy - energy_window,
                elem_info.binding_energy + energy_window
            ),
            background_method='shirley',
            description=elem_info.description
        )
        
        # Create peak stack with sub-peaks
        """if elem_info.sub_peaks:
            stack = XPSPeakStack(
                name=f"{self.element}{self.orbital}_multiplet",
                description=f"Multiple peaks for {elem_info.description}"
            )
            
            # Add line shapes for each sub-peak
            for i, sub_peak in enumerate(elem_info.sub_peaks):
                peak_name = sub_peak.get('name', f'peak_{i}')
                prefix = f"p{i}_"
                stack.add_line_shape(VoigtLineShape(peak_name, prefix=prefix))
            
            # Add constraints
            if len(elem_info.sub_peaks) > 1:
                # Position constraints
                for i in range(1, len(elem_info.sub_peaks)):
                    offset = elem_info.sub_peaks[i].get('offset', 0)
                    if offset != 0:
                        stack.add_constraint(
                            OffsetConstraint(
                                'p0_center',
                                f'p{i}_center',
                                offset=offset
                            )
                        )
                
                # Area constraints
                for i in range(1, len(elem_info.sub_peaks)):
                    area_ratio = elem_info.sub_peaks[i].get('area_ratio', 1.0)
                    if area_ratio != 1.0:
                        stack.add_constraint(
                            AreaConstraint(
                                'p0_amplitude',
                                f'p{i}_amplitude',
                                area_ratio=area_ratio
                            )
                        )
        else:
            # Single peak
            stack = XPSPeakStack(
                name=f"{self.element}{self.orbital}_single",
                description=f"Single peak for {elem_info.description}"
            )
            stack.add_line_shape(VoigtLineShape(f'{self.element}{self.orbital}', prefix='p0_'))
        
        region.add_peak_stack(stack)"""
        self.fitting_regions.append(region)
    
    @property
    def full_name(self) -> str:
        """
        Return full element orbital identifier.
        
        Returns
        -------
        str
            String like 'Fe2p', 'O1s', 'C_KVV'
        """
        return f"{self.element}{self.orbital}"
    
    def add_fitting_region(self, fitting_region: FittingRegion) -> None:
        """
        Add a fitting region to this element.
        
        Parameters
        ----------
        fitting_region : FittingRegion
            Energy range to add
        """
        if fitting_region is None:
            raise ValueError("fitting_region cannot be None")
        self.fitting_regions.append(fitting_region)
    
    def validate(self) -> bool:
        """
        Check that element region is complete and valid.
        
        Returns
        -------
        bool
            True if valid
            
        Raises
        ------
        ValueError
            If missing required information (dataset, fitting regions, etc.)
        """
        if not self.element or not self.orbital:
            raise ValueError("Element and orbital must be specified")
        
        if self.dataset is None:
            raise ValueError("Dataset must be assigned to ElementRegion")
        
        if not self.fitting_regions:
            raise ValueError("At least one fitting region must be defined")
        
        return True
