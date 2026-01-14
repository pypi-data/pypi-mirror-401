"""
Input validation and error checking.

Validates element regions, fitting regions, and configurations before fitting.
"""

from typing import List, Tuple


class ConfigurationValidator:
    """
    Validates XPS analysis configurations for completeness and consistency.
    """
    
    @staticmethod
    def validate_element_region(element_region: 'ElementRegion') -> Tuple[bool, List[str]]:
        """
        Validate element region configuration.
        
        Parameters
        ----------
        element_region : ElementRegion
            Region to validate
            
        Returns
        -------
        Tuple[bool, List[str]]
            (is_valid, list_of_error_messages)
        """
        pass
    
    @staticmethod
    def validate_fitting_region(fitting_region: 'FittingRegion') -> Tuple[bool, List[str]]:
        """Validate fitting region configuration."""
        pass
    
    @staticmethod
    def validate_peak_stack(peak_stack: 'XPSPeakStack') -> Tuple[bool, List[str]]:
        """Validate peak stack configuration."""
        pass
    
    @staticmethod
    def check_parameter_names(params: 'Parameters') -> bool:
        """
        Check that parameter names are unique and valid.
        
        Parameters
        ----------
        params : lmfit.Parameters
            Parameters to check
            
        Returns
        -------
        bool
            True if all parameters are valid
        """
        pass
    
    @staticmethod
    def check_constraint_consistency(constraints: List['Constraint'], 
                                    params: 'Parameters') -> Tuple[bool, List[str]]:
        """
        Check that constraints reference valid parameters.
        
        Parameters
        ----------
        constraints : List[Constraint]
            Constraints to validate
        params : lmfit.Parameters
            Parameters that must exist
            
        Returns
        -------
        Tuple[bool, List[str]]
            (is_valid, error_messages)
        """
        pass