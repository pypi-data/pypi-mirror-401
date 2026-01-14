"""
Abstract base classes for parameter constraints.

Constraints allow linking parameters across different line shapes, enabling
physical relationships (e.g., "peak 1 and peak 2 have the same FWHM") or
chemical knowledge (e.g., "doublet splitting is 0.5 eV").
"""

from abc import ABC, abstractmethod
from lmfit import Parameters


class Constraint(ABC):
    """
    Abstract base class for parameter constraints.
    
    A Constraint modifies an lmfit Parameters object to establish relationships
    between parameters. These relationships are enforced during fitting.
    
    Attributes
    ----------
    description : str
        Human-readable description of what this constraint does
    """
    
    @abstractmethod
    def apply(self, params: Parameters) -> None:
        """
        Apply the constraint to the parameters object.
        
        This method modifies the Parameters in-place, typically by setting
        the 'expr' attribute to create algebraic relationships.
        
        Parameters
        ----------
        params : Parameters
            The lmfit Parameters object to modify in-place
            
        Raises
        ------
        ValueError
            If referenced parameter names don't exist in params
        KeyError
            If parameter setup is invalid
        """
        pass
    
    def __repr__(self) -> str:
        """Return string representation of this constraint."""
        return f"{self.__class__.__name__}()"