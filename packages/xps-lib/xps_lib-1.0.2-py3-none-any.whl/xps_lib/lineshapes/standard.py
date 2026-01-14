"""
Standard XPS line shape implementations.

Contains concrete implementations of common peak models used in XPS:
Voigt, Gaussian, and Lorentzian profiles.
"""

from .base import LineShape
from lmfit import Model, Parameters
from lmfit.models import VoigtModel, GaussianModel, LorentzianModel
import numpy as np


class VoigtLineShape(LineShape):
    """
    Voigt profile: convolution of Gaussian and Lorentzian.
    
    This is the most physically realistic line shape for many XPS applications,
    combining natural line width (Lorentzian) with instrumental broadening (Gaussian).
    
    Parameters
    ----------
    amplitude : float
        Peak intensity (height)
    center : float
        Peak position (binding energy, eV)
    sigma : float
        Width parameter (standard deviation of Gaussian component, eV)
    fraction : float
        Lorentzian fraction (0=pure Gaussian, 1=pure Lorentzian)
    """
    
    def get_model(self) -> Model:
        """
        Return a VoigtModel.
        
        Returns
        -------
        Model
            lmfit VoigtModel with this shape's prefix
        """
        return VoigtModel(prefix=self.prefix)
    
    def make_params(self, x: np.ndarray, y: np.ndarray) -> Parameters:
        """
        Initialize Voigt parameters with intelligent guesses.
        
        Parameters
        ----------
        x : np.ndarray
            Energy data
        y : np.ndarray
            Background-corrected intensity
            
        Returns
        -------
        Parameters
            Initialized with: center (from weighted average), amplitude (from peak),
            sigma (reasonable guess), fraction (0.5 as neutral starting point)
        """
        
        # Find peak position (weighted average)
        if np.sum(y) > 0:
            center = np.sum(x * y) / np.sum(y)
        else:
            center = np.mean(x)
        
        # Find amplitude (peak height)
        amplitude = np.max(y)
        
        # Estimate sigma (FWHM/2.3548 for Gaussian)
        sigma = np.std(x[y > amplitude/2])
        if sigma == 0 or np.isnan(sigma):
            sigma = 0.5
        
        # Create parameters
        params = Parameters()
        params.add(f'{self.prefix}amplitude', value=amplitude, min=0)
        params.add(f'{self.prefix}center', value=center, min=np.min(x), max=np.max(x))
        params.add(f'{self.prefix}sigma', value=sigma, min=0.05, max=2.0)
        params.add(f'{self.prefix}fraction', value=0.5, min=0.0, max=1.0)
        
        return params
    
    def get_fwhm(self, params: Parameters) -> float:
        """
        Calculate FWHM for Voigt profile.
        
        Uses approximation formula combining Gaussian and Lorentzian contributions.
        
        Parameters
        ----------
        params : Parameters
            Must contain sigma and fraction parameters
            
        Returns
        -------
        float
            FWHM in eV
        """
        sigma = params[f'{self.prefix}sigma'].value
        fraction = params[f'{self.prefix}fraction'].value
        
        # Approximation for Voigt FWHM
        fg = 2.3548 * sigma  # Gaussian FWHM
        fl = 2.0 * sigma     # Lorentzian FWHM
        
        # Weighted average approximation
        fwhm = (1 - fraction) * fg + fraction * fl
        return fwhm


class GaussianLineShape(LineShape):
    """
    Pure Gaussian profile.
    
    Used when instrumental broadening dominates (low resolution spectra,
    or high-energy regions with large instrumental contributions).
    
    Parameters
    ----------
    amplitude : float
        Peak intensity
    center : float
        Peak position
    sigma : float
        Standard deviation of Gaussian (eV)
    """
    
    def get_model(self) -> Model:
        """Return a GaussianModel with this shape's prefix."""
        return GaussianModel(prefix=self.prefix)
    
    def make_params(self, x: np.ndarray, y: np.ndarray) -> Parameters:
        """Initialize Gaussian parameters."""
        center = np.sum(x * y) / np.sum(y) if np.sum(y) > 0 else np.mean(x)
        amplitude = np.max(y)
        sigma = np.std(x[y > amplitude/2]) if np.max(y) > 0 else 0.5
        
        params = Parameters()
        params.add(f'{self.prefix}amplitude', value=amplitude, min=0)
        params.add(f'{self.prefix}center', value=center, min=np.min(x), max=np.max(x))
        params.add(f'{self.prefix}sigma', value=max(0.1, sigma), min=0.05, max=2.0)
        
        return params
    
    def get_fwhm(self, params: Parameters) -> float:
        """Calculate FWHM for Gaussian profile (sigma * 2.3548)."""
        sigma = params[f'{self.prefix}sigma'].value
        return sigma * 2.3548


class LorentzianLineShape(LineShape):
    """
    Pure Lorentzian profile.
    
    Used when natural line width dominates (high-resolution spectra,
    or transitions with short lifetimes).
    
    Parameters
    ----------
    amplitude : float
        Peak intensity
    center : float
        Peak position
    sigma : float
        Half-width at half-maximum related parameter (eV)
    """
    
    def get_model(self) -> Model:
        """Return a LorentzianModel with this shape's prefix."""
        return LorentzianModel(prefix=self.prefix)
    
    def make_params(self, x: np.ndarray, y: np.ndarray) -> Parameters:
        """Initialize Lorentzian parameters."""
        center = np.sum(x * y) / np.sum(y) if np.sum(y) > 0 else np.mean(x)
        amplitude = np.max(y)
        sigma = np.std(x[y > amplitude/2]) if np.max(y) > 0 else 0.5
        
        params = Parameters()
        params.add(f'{self.prefix}amplitude', value=amplitude, min=0)
        params.add(f'{self.prefix}center', value=center, min=np.min(x), max=np.max(x))
        params.add(f'{self.prefix}sigma', value=max(0.1, sigma), min=0.05, max=2.0)
        
        return params
    
    def get_fwhm(self, params: Parameters) -> float:
        """Calculate FWHM for Lorentzian profile (sigma * 2)."""
        sigma = params[f'{self.prefix}sigma'].value
        return sigma * 2.0
