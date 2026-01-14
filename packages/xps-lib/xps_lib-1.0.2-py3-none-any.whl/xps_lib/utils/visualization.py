"""
Visualization utilities for fit results.

Creates publication-quality plots and interactive visualizations.
"""

from typing import Optional, Dict
import plotly.graph_objects as go
import matplotlib.figure as mfig


class PlotGenerator:
    """
    Generates plots of XPS fitting results.
    """
    
    @staticmethod
    def create_fit_plot(x: 'np.ndarray', y: 'np.ndarray', 
                       result: 'lmfit.ModelResult',
                       title: Optional[str] = None,
                       show_components: bool = True) -> go.Figure:
        """
        Create interactive Plotly figure of fit.
        
        Parameters
        ----------
        x : np.ndarray
            Energy axis
        y : np.ndarray
            Intensity data
        result : lmfit.ModelResult
            Fitting result with best_fit and eval_components
        title : str, optional
            Plot title
        show_components : bool
            Whether to show individual peak components
            
        Returns
        -------
        go.Figure
            Plotly figure object
        """
        pass
    
    @staticmethod
    def create_residuals_plot(x: 'np.ndarray', y: 'np.ndarray',
                             result: 'lmfit.ModelResult') -> go.Figure:
        """
        Create plot of fit residuals.
        
        Parameters
        ----------
        x : np.ndarray
            Energy axis
        y : np.ndarray
            Intensity data
        result : lmfit.ModelResult
            Fitting result
            
        Returns
        -------
        go.Figure
            Plotly figure showing residuals and statistics
        """
        pass
    
    @staticmethod
    def create_correlation_plot(result: 'lmfit.ModelResult', 
                               min_correl: float = 0.3) -> mfig.Figure:
        """
        Create correlation matrix heatmap.
        
        Parameters
        ----------
        result : lmfit.ModelResult
            Fitting result
        min_correl : float
            Minimum correlation magnitude to display
            
        Returns
        -------
        matplotlib.figure.Figure
            Correlation heatmap
        """
        pass
    
    @staticmethod
    def create_comparison_plot(regions: Dict[str, 'FittingRegion'],
                              results: Dict[str, 'lmfit.ModelResult']) -> go.Figure:
        """
        Create comparison plot of multiple fitted regions.
        
        Parameters
        ----------
        regions : Dict[str, FittingRegion]
            Regions by name
        results : Dict[str, lmfit.ModelResult]
            Results by region name
            
        Returns
        -------
        go.Figure
            Multi-panel or overlay plot
        """
        pass