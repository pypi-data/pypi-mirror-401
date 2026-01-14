"""
Fitting region definitions.

A fitting region represents a distinct energy range within an element orbital,
containing one or more peak stacks.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import numpy as np

from .peakstack import XPSPeakStack
from ..constraints.base import Constraint


@dataclass
class FittingRegion:
    """
    Represents a single energy range with background and peak stacks.
    
    Typically corresponds to a single XPS line (e.g., Fe 2p3/2 component),
    but may contain multiple overlapping features requiring multiple peak stacks.
    
    Attributes
    ----------
    name : str
        Descriptive name (e.g., 'Fe2p3/2', 'O_main', 'C_carbide')
    energy_range : Tuple[float, float]
        (min, max) binding energy in eV
    peak_stacks : List[XPSPeakStack]
        Peak stacks in this region
    background_method : str
        Background subtraction method ('linear', 'shirley', 'tougaard')
    background_region : Optional[Tuple[float, float]]
        Custom region for background determination (if applicable)
    description : str
        Details about this fitting region
    """

    def __init__(self, name: str, energy_range: Tuple[float, float],
                 background_method: str = "shirley", description: str = ""):
        """Initialize fitting region."""
        e_min, e_max = energy_range
        if e_min >= e_max:
            raise ValueError(f"Invalid energy range: {e_min} >= {e_max}")
        
        valid_methods = ['linear', 'shirley', 'tougaard']
        if background_method not in valid_methods:
            raise ValueError(f"Invalid background_method '{background_method}'")
        
        self.name = name
        self.energy_range = energy_range
        self.peak_stacks: List[XPSPeakStack] = []
        self.cross_stack_constraints: List[Constraint] = []
        self.background_method = background_method
        self.background_region: Optional[Tuple[float, float]] = None
        self.description = description
        self.background_array: Optional[np.ndarray] = None
    
    def add_peak_stack(self, peak_stack: XPSPeakStack) -> None:
        """Add a peak stack to this region."""
        if peak_stack is None:
            raise ValueError("peak_stack cannot be None")
        self.peak_stacks.append(peak_stack)
    
    def add_cross_stack_constraint(self, constraint: Constraint) -> None:
        """Add constraint linking parameters across peak stacks."""
        if constraint is None:
            raise ValueError("constraint cannot be None")
        self.cross_stack_constraints.append(constraint)
    
    def set_background(self, dataset: 'XPSDataset') -> None:
        """Calculate and set background for this region."""
        from ..io.constants import ENERGY_COL, INTENSITY_COL
        
        e_min, e_max = self.energy_range
        mask = (dataset.df[ENERGY_COL] >= e_min) & (dataset.df[ENERGY_COL] <= e_max)
        
        if not mask.any():
            raise ValueError(f"No data in range {e_min}-{e_max} eV")
        
        df_region = dataset.df.loc[mask].copy()
        x_data = df_region[ENERGY_COL].values
        y_data = df_region[INTENSITY_COL].values
        
        # Calculate background
        if self.background_method == 'linear':
            self.background_array = np.linspace(y_data[0], y_data[-1], len(y_data))
        elif self.background_method == 'shirley':
            self.background_array = self._shirley_background(x_data, y_data)
        elif self.background_method == 'tougaard':
            self.background_array = self._tougaard_background(x_data, y_data)
    
    def _shirley_background(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Calculate Shirley background (iterative)."""
        bg = np.ones_like(y) * y[0]
        for _ in range(50):
            integral = np.cumsum(y - bg)
            bg_new = y[0] + (y[-1] - y[0]) * integral / integral[-1]
            if np.allclose(bg, bg_new):
                break
            bg = bg_new
        return bg
    
    def _tougaard_background(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Simple Tougaard-like background."""
        C = 1000
        D = 3
        bg = np.zeros_like(y, dtype=float)
        for i, xi in enumerate(x):
            bg[i] = np.sum((y - y[i]) / (C + D * (x - xi)**2))
        return bg
    
    def validate(self) -> bool:
        """Check that fitting region is properly configured."""
        if not self.peak_stacks:
            raise ValueError(f"Region '{self.name}' has no peak stacks")
        return True
