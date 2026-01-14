"""
Peak stack definitions and operations.

A peak stack groups multiple line shapes with their inter-peak constraints,
forming a logical unit within a fitting region (e.g., a doublet, a satellite
structure, etc.).
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import numpy as np
from lmfit import Model, Parameters

from ..lineshapes.base import LineShape
#from ..constraints.base import Constraint
from ..constraints.constraints_new import Constraint


#@dataclass
class XPSPeakStack:
    """
    Container for multiple line shapes with shared constraints.
    
    A peak stack represents a physically or chemically meaningful group of peaks
    that should be fitted together. For example:
    - A 2p doublet (2 Voigt peaks with linked FWHM and splitting)
    - A multiplet structure (3+ peaks with chemical shift relationships)
    - Spin-orbit coupled peaks
    
    Attributes
    ----------
    name : str
        Descriptive name (e.g., 'Fe2p3/2_doublet', 'O_shake_up')
    line_shapes : List[LineShape]
        Individual peak models in this stack
    constraints : List[Constraint]
        Relationships between peaks in this stack
    background_corrected_data : Optional[Tuple[np.ndarray, np.ndarray]]
        Cached (energy, intensity) data for this stack
    description : str
        Detailed description of what this stack represents
    """

    def __init__(self, name: str, description: str = ""):
        """Initialize peak stack."""
        self.name = name
        self.description = description
        self.line_shapes: List = []
        self.constraints: List[Constraint] = []
        self.child_stacks: List['XPSPeakStack'] = []  # For nested stacks
        self.background_corrected_data: Optional[Tuple[np.ndarray, np.ndarray]] = None
        self.component_index: Optional[int] = None  # For grouping peaks by tag


    
    def add_line_shape(self, line_shape: LineShape) -> None:
        """
        Add a line shape to this stack.
        
        Parameters
        ----------
        line_shape : LineShape
            Peak model to add
            
        Raises
        ------
        ValueError
            If line_shape is not a LineShape instance
        """
        if line_shape is None:
            raise ValueError("line_shape cannot be None")
        self.line_shapes.append(line_shape)
    
    def add_constraint(self, constraint: Constraint) -> None:
        """
        Add a constraint linking parameters in this stack.
        
        Parameters
        ----------
        constraint : Constraint
            Relationship to enforce during fitting
        """
        if constraint is None:
            raise ValueError("constraint cannot be None")
        self.constraints.append(constraint)

    def add_child_stack(self, child_stack: 'XPSPeakStack') -> None:
        """
        Add another peak stack as a child.
        
        This allows nesting stacks and creating constraints between them.
        Useful for grouping related peaks (e.g., spin-orbit pairs).
        
        Example:
            stack_2p3_2 = XPSPeakStack('Fe2p3/2')
            stack_2p1_2 = XPSPeakStack('Fe2p1/2')
            stack_2p3_2.add_child_stack(stack_2p1_2)
            # Now they're grouped together
        """
        if child_stack is None:
            raise ValueError("child_stack cannot be None")
        self.child_stacks.append(child_stack)

    def set_component_index(self, index: int) -> None:
        """
        Set component index (tag) for grouping peaks.
        
        Peaks with the same index should be summed together in the envelope.
        Used in Casa XPS to group peaks that belong together.
        """
        self.component_index = index

    def get_all_line_shapes(self) -> List:
        """Get all line shapes including from child stacks."""
        all_shapes = list(self.line_shapes)
        for child in self.child_stacks:
            all_shapes.extend(child.get_all_line_shapes())
        return all_shapes
    
    def get_all_constraints(self) -> List[Constraint]:
        """Get all constraints including from child stacks."""
        all_constraints = list(self.constraints)
        for child in self.child_stacks:
            all_constraints.extend(child.get_all_constraints())
        return all_constraints

    
    def build_composite_model(self) -> Tuple[Model, Parameters]:
        """
        Build the composite lmfit Model and initialize Parameters.
        
        Combines all line shapes into a single model, initializes all parameters
        with intelligent guesses, and applies all constraints.
        
        Returns
        -------
        Tuple[Model, Parameters]
            Composite model suitable for fitting, and initialized parameters
            with constraints applied
            
        Raises
        ------
        ValueError
            If no line shapes are defined
        ValueError
            If background_corrected_data is not set
        RuntimeError
            If model construction or constraint application fails
        """
        from lmfit import Model, Parameters
        
        # Get ALL line shapes (including nested)
        all_line_shapes = self.get_all_line_shapes()
        
        if not all_line_shapes:
            raise ValueError(
                f"XPSPeakStack '{self.name}' has no line shapes (including children)"
            )
        
        if self.background_corrected_data is None:
            raise ValueError(
                f"Background-corrected data not set for '{self.name}'"
            )
        
        x, y = self.background_corrected_data
        
        # Step 1: Build composite model
        model = None
        params = Parameters()
        
        for line_shape in all_line_shapes:
            ls_model = line_shape.get_model()
            model = ls_model if model is None else model + ls_model
            ls_params = line_shape.make_params(x, y)
            params.update(ls_params)
        
        # Step 2: Apply all constraints (including nested)
        all_constraints = self.get_all_constraints()
        for constraint in all_constraints:
            try:
                constraint.apply(params)
            except Exception as e:
                raise RuntimeError(
                    f"Failed to apply constraint {constraint.description} "
                    f"in peak stack '{self.name}': {e}"
                )
        
        return model, params
    
    def get_peak_summary(self, params: Parameters) -> dict:
        """
        Extract key peak properties (center, FWHM, amplitude) from parameters.
        
        Parameters
        ----------
        params : Parameters
            Fitted or trial parameters
            
        Returns
        -------
        dict
            Mapping of peak names to their properties (center, FWHM, amplitude, etc.)
        """
        summary = {}
        for line_shape in self.get_all_line_shapes():
            prefix = line_shape.prefix
            peak_info = {
                'center': params[f'{prefix}center'].value,
                'center_err': params[f'{prefix}center'].stderr,
                'amplitude': params[f'{prefix}amplitude'].value,
                'amplitude_err': params[f'{prefix}amplitude'].stderr,
            }
            fwhm = line_shape.get_fwhm(params)
            if fwhm is not None:
                peak_info['fwhm'] = fwhm
            summary[line_shape.name] = peak_info
        return summary