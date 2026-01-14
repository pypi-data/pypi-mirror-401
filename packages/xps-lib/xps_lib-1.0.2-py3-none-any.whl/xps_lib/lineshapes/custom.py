"""
Custom and advanced XPS line shape implementations.

Contains specialized peak models for specific XPS applications:
Gaussian-Lorentzian mixing, asymmetric shapes, etc.
"""

from .base import LineShape
from lmfit import Model, Parameters
import numpy as np
from scipy.signal import fftconvolve

class GaussianLorentzianMixLineShape(LineShape):
    """
    Variable Gaussian-Lorentzian mix line shape with GL(n) notation support.
    
    Allows smooth interpolation between pure Gaussian and pure Lorentzian
    through a mixing parameter. More flexible than fixed Voigt.
    
    Supports Casa-style GL(n) notation where n is the Lorentzian percentage.
    
    Parameters
    ----------
    name : str
        Peak name
    prefix : str
        lmfit parameter prefix
    lorentzian_percent : float or None
        Lorentzian percentage (0-100). If set, m is fixed to this value / 100.
        If None (default), m is optimized during fitting starting from 50%.
        
    Examples
    --------
    >>> # GL(30) - 30% Lorentzian, 70% Gaussian (fixed)
    >>> shape = GaussianLorentzianMixLineShape("Al 2p3/2", prefix="p0_", lorentzian_percent=30)
    
    >>> # GL(50) - 50/50 mix (fixed)
    >>> shape = GaussianLorentzianMixLineShape("N 1s", prefix="p0_", lorentzian_percent=50)
    
    >>> # Optimize the mix ratio automatically
    >>> shape = GaussianLorentzianMixLineShape("Fe 2p", prefix="p0_")
    """
    
    def __init__(self, name: str, prefix: str = "", lorentzian_percent: float = None):
        """
        Initialize GL mix line shape.
        
        Parameters
        ----------
        name : str
            Peak name
        prefix : str
            lmfit prefix
        lorentzian_percent : float, optional
            Lorentzian percentage (0-100). If provided, fixes m to this value.
        """
        super().__init__(name, prefix)
        self.lorentzian_percent = lorentzian_percent
        
        if lorentzian_percent is not None:
            if not (0 <= lorentzian_percent <= 100):
                raise ValueError("lorentzian_percent must be between 0 and 100")
    
    @staticmethod
    def gl_mix_func(x: np.ndarray, amplitude: float, center: float, 
                    sigma: float, m: float) -> np.ndarray:
        """
        Compute Gaussian-Lorentzian mix at given x values.
        
        Parameters
        ----------
        x : np.ndarray
            Energy values
        amplitude : float
            Peak height
        center : float
            Peak center
        sigma : float
            Width
        m : float
            Mixing parameter (0=pure Gaussian, 1=pure Lorentzian)
            
        Returns
        -------
        np.ndarray
            Peak values
        """
        from scipy.special import wofz
        
        z = ((x - center) + 1j * sigma) / (sigma * np.sqrt(2))
        voigt = np.real(wofz(z)) / (sigma * np.sqrt(2 * np.pi))
        
        gaussian = np.exp(-((x - center)**2) / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))
        lorentzian = sigma / ((x - center)**2 + sigma**2) / np.pi
        
        result = (1 - m) * gaussian + m * lorentzian
        return amplitude * result / np.max(result)
    
    def get_model(self) -> Model:
        """Return a custom Model using gl_mix_func."""
        return Model(self.gl_mix_func, prefix=self.prefix)
    
    def make_params(self, x: np.ndarray, y: np.ndarray) -> Parameters:
        """
        Initialize GL mix parameters.
        
        If lorentzian_percent was specified in __init__, m is fixed to that value.
        Otherwise, starts with m=0.5 (neutral) and lets optimization find the best blend.
        """
        center = np.sum(x * y) / np.sum(y) if np.sum(y) > 0 else np.mean(x)
        amplitude = np.max(y)
        sigma = np.std(x[y > amplitude/2]) if np.max(y) > 0 else 0.5
        
        params = Parameters()
        params.add(f'{self.prefix}amplitude', value=amplitude, min=0)
        params.add(f'{self.prefix}center', value=center, min=np.min(x), max=np.max(x))
        params.add(f'{self.prefix}sigma', value=max(0.1, sigma), min=0.05, max=2.0)
        
        # Set m based on whether lorentzian_percent was specified
        if self.lorentzian_percent is not None:
            m_value = self.lorentzian_percent / 100.0
            params.add(f'{self.prefix}m', value=m_value, vary=False)  # Fixed
        else:
            params.add(f'{self.prefix}m', value=0.5, min=0.0, max=1.0)  # Optimizable
        
        return params

    def describe_mix(self, params) -> str:
        """
        Return human-readable GL mix string if mix is not fixed.
        Uses Casa-style GL(n) where n = Lorentzian percentage.
        """
        mix_param_name = f"{self.prefix}m"
    
        if mix_param_name not in params:
            return ""
    
        param = params[mix_param_name]
    
        # Only report if optimized (not fixed)
        if not param.vary:
            return ""
    
        lorentz_pct = param.value * 100.0
        gauss_pct = 100.0 - lorentz_pct
    
        return f"GL({lorentz_pct:.0f}) → {gauss_pct:.0f}% G / {lorentz_pct:.0f}% L"



class LA(LineShape):
    """
    Casa-style LA line shape: smooth asymmetric Lorentzian convolved with Gaussian.
    Fully continuous, no split or jump.
    """

    def __init__(self, name, prefix="", alpha=None, beta=None,
                 lorentzian_percent=100, sigma_inst=0.02, smooth=0.02):
        super().__init__(name, prefix)
        self.alpha = alpha
        self.beta = beta
        self.lorentzian_percent = lorentzian_percent
        self.sigma_inst = sigma_inst
        self.smooth = smooth

    @staticmethod
    def _asymmetric_lorentz(x, amplitude, center, sigma, alpha, beta, smooth):
        """Smooth asymmetric Lorentzian (pre-convolution)."""
        dx = x - center
        S = 0.5 * (1 + np.tanh(dx / smooth))
        width = sigma * ((alpha - 1) * (1 - S) + (beta - 1) * S + 1)
        return amplitude * width / (np.pi * (dx**2 + width**2))

    def la_func(self, x, amplitude, center, sigma, alpha, beta):
        """Full LA peak: asymmetric Lorentzian convolved with Gaussian."""
        # Lorentzian
        lorentz = self._asymmetric_lorentz(x, 1.0, center, sigma, alpha, beta, self.smooth)

        # Gaussian kernel centered at zero
        dx = x[1] - x[0]
        N = len(x)
        t = np.linspace(-N//2, N//2, N) * dx
        gauss = np.exp(-0.5 * (t / self.sigma_inst) ** 2)
        gauss /= np.sum(gauss)  # normalize

        # Convolution
        conv = fftconvolve(lorentz, gauss, mode='same')

        # Scale amplitude
        conv *= amplitude / np.max(conv)
        return conv

    def get_model(self):
        return Model(lambda x, amplitude, center, sigma, alpha, beta:
                     self.la_func(x, amplitude, center, sigma, alpha, beta),
                     prefix=self.prefix)

    def make_params(self, x, y):
        center = np.sum(x * y) / np.sum(y) if np.sum(y) > 0 else np.mean(x)
        amplitude = np.max(y)
        sigma = np.std(x[y > amplitude / 2]) if np.max(y) > 0 else 0.5

        params = Parameters()
        params.add(f"{self.prefix}amplitude", value=amplitude, min=0)
        params.add(f"{self.prefix}center", value=center, min=np.min(x), max=np.max(x))
        params.add(f"{self.prefix}sigma", value=max(0.1, sigma), min=0.05, max=2.0)

        if self.alpha is not None:
            params.add(f"{self.prefix}alpha", value=self.alpha, vary=False)
        else:
            params.add(f"{self.prefix}alpha", value=1.0, min=0.5, max=3.0)

        if self.beta is not None:
            params.add(f"{self.prefix}beta", value=self.beta, vary=False)
        else:
            params.add(f"{self.prefix}beta", value=1.0, min=0.5, max=3.0)

        return params

    def describe(self, params):
        alpha_val = params[f"{self.prefix}alpha"].value
        beta_val = params[f"{self.prefix}beta"].value
        return f"LA({alpha_val:.2f}, {beta_val:.2f}, {self.lorentzian_percent:.0f})"


class LorentzAsymmetricLineShape(LineShape):
    """
    Lorentzian-based asymmetric line shape with independent left/right broadening.
    
    Models cases where asymmetry is physically meaningful (shake-up satellites,
    charge-transfer effects, etc.). Uses Lorentzian profile with asymmetric widths.
    
    Supports Casa-style LA(alpha, beta, n) notation where:
    - alpha: left-side width factor
    - beta: right-side width factor  
    - n: Lorentzian percentage (0-100)
    
    Parameters
    ----------
    name : str
        Peak name
    prefix : str
        lmfit parameter prefix
    alpha : float or None
        Left-side broadening factor. If None, optimized during fitting.
    beta : float or None
        Right-side broadening factor. If None, optimized during fitting.
    lorentzian_percent : float or None
        Lorentzian percentage (0-100). If None, uses Lorentzian by default.
        
    Examples
    --------
    >>> # LA(1.2, 2.5, 100) - Fixed asymmetry (fixed)
    >>> shape = LorentzAsymmetricLineShape("C 1s", prefix="p0_", 
    ...                                     alpha=1.2, beta=2.5, lorentzian_percent=100)
    
    >>> # Optimize asymmetry automatically
    >>> shape = LorentzAsymmetricLineShape("Fe 2p", prefix="p0_")
    """
    
    def __init__(self, name: str, prefix: str = "", 
                 alpha: float = None, beta: float = None,
                 lorentzian_percent: float = 100):
        """
        Initialize asymmetric Lorentzian line shape.
        
        Parameters
        ----------
        name : str
            Peak name
        prefix : str
            lmfit prefix
        alpha : float, optional
            Left-side broadening. If provided, fixes to this value.
        beta : float, optional
            Right-side broadening. If provided, fixes to this value.
        lorentzian_percent : float, optional
            Lorentzian character (default 100 = pure Lorentzian)
        """
        super().__init__(name, prefix)
        self.alpha = alpha
        self.beta = beta
        self.lorentzian_percent = lorentzian_percent
        
        if lorentzian_percent is not None:
            if not (0 <= lorentzian_percent <= 100):
                raise ValueError("lorentzian_percent must be between 0 and 100")
    
    @staticmethod
    def asymmetric_lorentz_func(x: np.ndarray, amplitude: float, center: float,
                               sigma: float, alpha: float, beta: float) -> np.ndarray:
        """
        Compute asymmetric Lorentzian peak at given x values.
        
        Parameters
        ----------
        x : np.ndarray
            Energy values
        amplitude : float
            Peak height
        center : float
            Peak center
        sigma : float
            Base width parameter
        alpha : float
            Left-side broadening factor
        beta : float
            Right-side broadening factor
            
        Returns
        -------
        np.ndarray
            Peak values
        """
        left = x < center
        right = x >= center
        
        result = np.zeros_like(x, dtype=float)
        
        # Left side
        if np.any(left):
            width_l = sigma * alpha
            result[left] = amplitude * width_l / ((x[left] - center)**2 + width_l**2) / np.pi
        
        # Right side
        if np.any(right):
            width_r = sigma * beta
            result[right] = amplitude * width_r / ((x[right] - center)**2 + width_r**2) / np.pi
        
        return result
    
    def get_model(self) -> Model:
        """Return a custom Model using asymmetric_lorentz_func."""
        return Model(self.asymmetric_lorentz_func, prefix=self.prefix)
    
    def make_params(self, x: np.ndarray, y: np.ndarray) -> Parameters:
        """
        Initialize asymmetric Lorentzian parameters.
        
        If alpha/beta were specified in __init__, they are fixed.
        Otherwise, they start at 1.0 (symmetric) and can be optimized.
        """
        center = np.sum(x * y) / np.sum(y) if np.sum(y) > 0 else np.mean(x)
        amplitude = np.max(y)
        sigma = np.std(x[y > amplitude/2]) if np.max(y) > 0 else 0.5
        
        params = Parameters()
        params.add(f'{self.prefix}amplitude', value=amplitude, min=0)
        params.add(f'{self.prefix}center', value=center, min=np.min(x), max=np.max(x))
        params.add(f'{self.prefix}sigma', value=max(0.1, sigma), min=0.05, max=2.0)
        
        # Alpha (left broadening)
        if self.alpha is not None:
            params.add(f'{self.prefix}alpha', value=self.alpha, vary=False)  # Fixed
        else:
            params.add(f'{self.prefix}alpha', value=1.0, min=0.5, max=3.0)  # Optimizable
        
        # Beta (right broadening)
        if self.beta is not None:
            params.add(f'{self.prefix}beta', value=self.beta, vary=False)  # Fixed
        else:
            params.add(f'{self.prefix}beta', value=1.0, min=0.5, max=3.0)  # Optimizable
        
        return params
    
    def describe_asymmetry(self, params) -> str:
        """
        Return human-readable LA notation if asymmetry is optimized.
        Uses Casa-style LA(alpha, beta, n) format.
        """
        alpha_name = f"{self.prefix}alpha"
        beta_name = f"{self.prefix}beta"
        
        if alpha_name not in params or beta_name not in params:
            return ""
        
        alpha_param = params[alpha_name]
        beta_param = params[beta_name]
        
        # Only report if optimized (not fixed)
        if not alpha_param.vary or not beta_param.vary:
            return ""
        
        return f"LA({alpha_param.value:.1f}, {beta_param.value:.1f}, {self.lorentzian_percent:.0f})"


class AsymmetricLineShape(LineShape):
    """
    Asymmetric Gaussian line shape with independent left/right broadening.
    
    Models cases where asymmetry is physically meaningful (shake-up satellites,
    charge-transfer effects, etc.).
    
    Supports Casa-style AS(alpha, beta) notation where:
    - alpha: left-side broadening factor
    - beta: right-side broadening factor
    
    Parameters
    ----------
    name : str
        Peak name
    prefix : str
        lmfit parameter prefix
    alpha : float or None
        Left-side broadening factor. If None, optimized during fitting.
    beta : float or None
        Right-side broadening factor. If None, optimized during fitting.
        
    Examples
    --------
    >>> # AS(1.2, 2.5) - Fixed asymmetry (fixed)
    >>> shape = AsymmetricLineShape("C 1s", prefix="p0_", alpha=1.2, beta=2.5)
    
    >>> # Optimize asymmetry automatically
    >>> shape = AsymmetricLineShape("Fe 2p", prefix="p0_")
    """
    
    def __init__(self, name: str, prefix: str = "", 
                 alpha: float = None, beta: float = None):
        """
        Initialize asymmetric Gaussian line shape.
        
        Parameters
        ----------
        name : str
            Peak name
        prefix : str
            lmfit prefix
        alpha : float, optional
            Left-side broadening. If provided, fixes to this value.
        beta : float, optional
            Right-side broadening. If provided, fixes to this value.
        """
        super().__init__(name, prefix)
        self.alpha = alpha
        self.beta = beta
    
    @staticmethod
    def asymmetric_func(x: np.ndarray, amplitude: float, center: float,
                       sigma: float, alpha: float, beta: float) -> np.ndarray:
        """
        Compute asymmetric Gaussian peak at given x values.
        
        Parameters
        ----------
        x : np.ndarray
            Energy values
        amplitude : float
            Peak height
        center : float
            Peak center
        sigma : float
            Base width parameter
        alpha : float
            Left broadening factor
        beta : float
            Right broadening factor
            
        Returns
        -------
        np.ndarray
            Peak values
        """
        left = x < center
        right = x >= center
        
        result = np.zeros_like(x, dtype=float)
        
        if np.any(left):
            result[left] = amplitude * np.exp(-((x[left] - center)**2) / (2 * (sigma * alpha)**2))
        if np.any(right):
            result[right] = amplitude * np.exp(-((x[right] - center)**2) / (2 * (sigma * beta)**2))
        
        return result
    
    def get_model(self) -> Model:
        """Return a custom Model using asymmetric_func."""
        return Model(self.asymmetric_func, prefix=self.prefix)
    
    def make_params(self, x: np.ndarray, y: np.ndarray) -> Parameters:
        """
        Initialize asymmetric Gaussian parameters.
        
        If alpha/beta were specified in __init__, they are fixed.
        Otherwise, they start at 1.0 (symmetric) and can be optimized.
        """
        center = np.sum(x * y) / np.sum(y) if np.sum(y) > 0 else np.mean(x)
        amplitude = np.max(y)
        sigma = np.std(x[y > amplitude/2]) if np.max(y) > 0 else 0.5
        
        params = Parameters()
        params.add(f'{self.prefix}amplitude', value=amplitude, min=0)
        params.add(f'{self.prefix}center', value=center, min=np.min(x), max=np.max(x))
        params.add(f'{self.prefix}sigma', value=max(0.1, sigma), min=0.05, max=2.0)
        
        # Alpha (left broadening)
        if self.alpha is not None:
            params.add(f'{self.prefix}alpha', value=self.alpha, vary=False)  # Fixed
        else:
            params.add(f'{self.prefix}alpha', value=1.0, min=0.5, max=3.0)  # Optimizable
        
        # Beta (right broadening)
        if self.beta is not None:
            params.add(f'{self.prefix}beta', value=self.beta, vary=False)  # Fixed
        else:
            params.add(f'{self.prefix}beta', value=1.0, min=0.5, max=3.0)  # Optimizable
        
        return params
    
    def describe_asymmetry(self, params) -> str:
        """
        Return human-readable AS notation if asymmetry is optimized.
        Uses Casa-style AS(alpha, beta) format.
        """
        alpha_name = f"{self.prefix}alpha"
        beta_name = f"{self.prefix}beta"
        
        if alpha_name not in params or beta_name not in params:
            return ""
        
        alpha_param = params[alpha_name]
        beta_param = params[beta_name]
        
        # Only report if optimized (not fixed)
        if not alpha_param.vary or not beta_param.vary:
            return ""
        
        return f"AS({alpha_param.value:.1f}, {beta_param.value:.1f})"
