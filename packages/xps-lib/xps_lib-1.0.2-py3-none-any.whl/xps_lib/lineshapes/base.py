"""
Abstract base classes for XPS peak line shapes.

This module defines the LineShape interface that all concrete peak models must
implement. It establishes contracts for model creation, parameter initialization,
and FWHM calculations.
"""

from abc import ABC, abstractmethod
from lmfit import Model, Parameters
import numpy as np


class LineShape(ABC):
    """
    Abstract base class for all XPS peak line shapes.
    
    A LineShape encapsulates a single peak model that can be used in fitting.
    Each implementation must provide:
    - A model factory method
    - Parameter initialization with reasonable defaults and bounds
    - Optional FWHM calculation for result interpretation
    
    Attributes
    ----------
    name : str
        Descriptive identifier for this peak (e.g., 'Fe2p3/2_main', 'O_peak1')
    prefix : str
        lmfit parameter prefix to avoid name collisions (e.g., 'p0_', 'p1_')
    model : Model, optional
        Cached lmfit Model instance
    """
    
    def __init__(self, name: str, prefix: str = ""):
        """
        Initialize a line shape.
        
        Parameters
        ----------
        name : str
            Descriptive name for this peak model
        prefix : str
            lmfit prefix for parameters (must end with underscore if not empty)
        """
        self.name = name
        self.prefix = prefix if prefix.endswith("_") or prefix == "" else prefix + "_"
        self.model = None
    
    @abstractmethod
    def get_model(self) -> Model:
        """
        Return the lmfit Model for this line shape.
        
        This method should return a fresh or cached Model instance that can
        be combined with other models using the '+' operator.
        
        Returns
        -------
        Model
            An lmfit Model instance representing this peak shape
        """
        pass
    
    @abstractmethod
    def make_params(self, x: np.ndarray, y: np.ndarray) -> Parameters:
        """
        Create and initialize Parameters for this line shape.
        
        This method analyzes the provided data to generate intelligent initial
        guesses for all parameters (center, amplitude, width, etc.). It should
        also set reasonable bounds to guide the fit.
        
        Parameters
        ----------
        x : np.ndarray
            Energy axis data (binding energy in eV)
        y : np.ndarray
            Intensity data (should be background-corrected)
            
        Returns
        -------
        Parameters
            lmfit Parameters object with initial guesses and bounds set
        """
        pass
    
    def get_fwhm(self, params: Parameters) -> float:
        """
        Calculate Full-Width at Half-Maximum from fitted parameters.
        
        Default implementation returns None. Override in subclasses where
        FWHM is meaningful and calculable from the parameters.
        
        Parameters
        ----------
        params : Parameters
            Fitted or trial parameters from the model
            
        Returns
        -------
        float or None
            FWHM value in eV, or None if not applicable
        """
        pass