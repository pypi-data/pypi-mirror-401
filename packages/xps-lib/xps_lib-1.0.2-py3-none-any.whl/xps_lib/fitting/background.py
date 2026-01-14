"""
Background subtraction strategies.

Contains abstraction for different background calculation methods.
"""

from abc import ABC, abstractmethod
import numpy as np


class BackgroundStrategy(ABC):
    """
    Abstract base class for background calculation strategies.
    
    Attributes
    ----------
    method_name : str
        Name of this strategy (e.g., 'shirley', 'linear')
    region : Optional[Tuple[float, float]]
        Optional custom region for background determination
    """
    
    @abstractmethod
    def calculate(self, energy: np.ndarray, intensity: np.ndarray) -> np.ndarray:
        """
        Calculate background array.
        
        Parameters
        ----------
        energy : np.ndarray
            Energy axis
        intensity : np.ndarray
            Intensity data
            
        Returns
        -------
        np.ndarray
            Background array (same shape as intensity)
        """
        pass


class LinearBackgroundStrategy(BackgroundStrategy):
    """Linear background subtraction."""
    
    def calculate(self, energy: np.ndarray, intensity: np.ndarray) -> np.ndarray:
        """Calculate linear background."""
        pass


class ShirleyBackgroundStrategy(BackgroundStrategy):
    """Shirley background (self-consistent iterative method)."""
    
    def calculate(self, energy: np.ndarray, intensity: np.ndarray) -> np.ndarray:
        """Calculate Shirley background."""
        pass


class TougaardBackgroundStrategy(BackgroundStrategy):
    """Tougaard background (universal inelastic scattering cross-section)."""
    
    def calculate(self, energy: np.ndarray, intensity: np.ndarray) -> np.ndarray:
        """Calculate Tougaard background."""
        pass