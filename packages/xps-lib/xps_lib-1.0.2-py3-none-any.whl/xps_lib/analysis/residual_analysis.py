from typing import Optional
import numpy as np
import plotly.graph_objects as go

class ResidualAnalysis:
    """Analyze and visualize fitting residuals."""
    
    def __init__(self, fitter: 'XPSElementFitter'):
        """Initialize residual analysis tool."""
        self.fitter = fitter
    
    def get_residuals(self, fitting_region_name: str) -> Optional[np.ndarray]:
        """
        Get residual array for a fitted region.
        
        Parameters
        ----------
        fitting_region_name : str
            Name of the fitted region
            
        Returns
        -------
        np.ndarray or None
            Residuals (observed - fitted), or None if not fitted
        """
        if fitting_region_name not in self.fitter.fitting_results:
            return None
        
        result = self.fitter.fitting_results[fitting_region_name]['result']
        return result.residual
    
    def get_residual_rms(self, fitting_region_name: str) -> Optional[float]:
        """
        Get RMS (root mean square) of residuals.
        
        Parameters
        ----------
        fitting_region_name : str
            Name of fitted region
            
        Returns
        -------
        float or None
            RMS of residuals, or None if not fitted
        """
        residuals = self.get_residuals(fitting_region_name)
        if residuals is None or len(residuals) == 0:
            return None

        n_data = len(residuals)
        
        #return np.sqrt(np.mean(residuals**2))
        rms = np.sqrt(np.sum(residuals**2) / n_data)  # Correct: Casa XPS formula
        return rms
    
    def get_normalized_rms(self, fitting_region_name: str) -> Optional[float]:
        """
        Get normalized RMS (dividing by average intensity).
        
        This allows comparison between spectra with different intensity scales.
        Formula: RMS_norm = RMS / mean(intensity)
        
        Parameters
        ----------
        fitting_region_name : str
            Name of fitted region
            
        Returns
        -------
        float or None
            Normalized RMS (%), or None if not fitted
        """
        residuals = self.get_residuals(fitting_region_name)
        if residuals is None or len(residuals) == 0:
            return None
        
        result_data = self.fitter.fitting_results[fitting_region_name]
        intensity = result_data['intensity']
        background = result_data['background']
        bg_corrected = intensity - background
        
        mean_intensity = np.mean(np.abs(bg_corrected))
        if mean_intensity == 0:
            return None
        
        rms = self.get_residual_rms(fitting_region_name)
        return 100.0 * rms / mean_intensity

    def get_casa_rms(self, fitting_region_name: str) -> Optional[float]:
        if fitting_region_name not in self.fitter.fitting_results:
            return None
    
        result = self.fitter.fitting_results[fitting_region_name]['result']
    
        # Casa RMS is sqrt(reduced chi-squared)
        return float(np.sqrt(result.redchi))
    
    def get_residual_statistics(self, fitting_region_name: str) -> Optional[dict]:
        """
        Get comprehensive residual statistics.
        
        Parameters
        ----------
        fitting_region_name : str
            Name of fitted region
            
        Returns
        -------
        dict or None
            Dictionary with: mean, std, min, max, rms, rms_normalized, chi2, reduced_chi2
        """
        residuals = self.get_residuals(fitting_region_name)
        if residuals is None or len(residuals) == 0:
            return None
        
        result = self.fitter.fitting_results[fitting_region_name]['result']
        
        stats = {
            'n_points': len(residuals),

            # Raw residual statistics (counts)
            'mean_counts': float(np.mean(residuals)),
            'std_counts': float(np.std(residuals)),
            'min_counts': float(np.min(residuals)),
            'max_counts': float(np.max(residuals)),
            'rms_counts': self.get_residual_rms(fitting_region_name),
        
            # Scale-independent metrics
            'rms_relative_percent': self.get_normalized_rms(fitting_region_name),
        
            # Casa-compatible metric
            'rms_casa': self.get_casa_rms(fitting_region_name),
        
            # Only meaningful because fit is weighted
            'chi_squared': result.chisqr,
            'reduced_chi_squared': result.redchi,
        }
        
        return stats
    
    def plot_residuals(self, fitting_region_name: str, 
                       title: Optional[str] = None) -> go.Figure:
        """
        Generate residual plot (data - fit).
        
        Shows how well the model fits the data at each energy point.
        A good fit should have residuals randomly distributed around zero.
        
        Parameters
        ----------
        fitting_region_name : str
            Name of fitted region
        title : str, optional
            Custom plot title
            
        Returns
        -------
        go.Figure
            Plotly figure showing residuals
        """
        residuals = self.get_residuals(fitting_region_name)
        if residuals is None:
            raise ValueError(f"No results for region '{fitting_region_name}'")
        
        result_data = self.fitter.fitting_results[fitting_region_name]
        energy = result_data['energy']
        
        fig = go.Figure()
        
        # Residuals
        fig.add_trace(go.Scatter(
            x=energy, y=residuals,
            mode='markers+lines',
            name='Residuals',
            line=dict(color='red', width=1),
            marker=dict(size=4, color='red')
        ))
        
        # Zero line
        fig.add_hline(y=0, line_dash="dash", line_color="black", 
                     annotation_text="Zero")
        
        # ±1σ bands
        rms = self.get_residual_rms(fitting_region_name)
        if rms is not None:
            fig.add_hline(y=rms, line_dash="dot", line_color="gray", 
                         opacity=0.5)
            fig.add_hline(y=-rms, line_dash="dot", line_color="gray", 
                         opacity=0.5)
        
        fig.update_layout(
            title=title or f"Residuals - {fitting_region_name}",
            xaxis_title="Binding Energy (eV)",
            yaxis_title="Residuals (Intensity)",
            template="plotly_white",
            hovermode='x unified',
            height=400,
            width=1000,
            xaxis=dict(autorange="reversed")
        )
        
        return fig
    
    def plot_normalized_residuals(self, fitting_region_name: str,
                                  title: Optional[str] = None) -> go.Figure:
        """
        Generate normalized residual plot (residuals / fit values).
        
        Useful for seeing relative quality of fit across different intensity regions.
        
        Parameters
        ----------
        fitting_region_name : str
            Name of fitted region
        title : str, optional
            Custom plot title
            
        Returns
        -------
        go.Figure
            Plotly figure showing normalized residuals
        """
        residuals = self.get_residuals(fitting_region_name)
        if residuals is None:
            raise ValueError(f"No results for region '{fitting_region_name}'")
        
        result_data = self.fitter.fitting_results[fitting_region_name]
        energy = result_data['energy']
        result = result_data['result']
        
        # Normalize by fitted values
        fitted_values = result.best_fit
        # Avoid division by zero
        fitted_values = np.where(np.abs(fitted_values) < 1e-6, 1e-6, fitted_values)
        normalized_residuals = 100.0 * residuals / fitted_values
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=energy, y=normalized_residuals,
            mode='markers+lines',
            name='Normalized Residuals',
            line=dict(color='orange', width=1),
            marker=dict(size=4, color='orange')
        ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="black")
        fig.add_hline(y=5, line_dash="dot", line_color="gray", opacity=0.5)
        fig.add_hline(y=-5, line_dash="dot", line_color="gray", opacity=0.5)
        
        fig.update_layout(
            title=title or f"Normalized Residuals - {fitting_region_name}",
            xaxis_title="Binding Energy (eV)",
            yaxis_title="Normalized Residuals (%)",
            template="plotly_white",
            hovermode='x unified',
            height=400,
            width=1000,
            xaxis=dict(autorange="reversed")
        )
        
        return fig
    
    def print_residual_report(self, fitting_region_name: str) -> None:
        """Print formatted residual statistics."""
        stats = self.get_residual_statistics(fitting_region_name)
        if stats is None:
            print(f"No results for region '{fitting_region_name}'")
            return
        
        print(f"\n{'='*70}")
        print(f"RESIDUAL ANALYSIS - {fitting_region_name}")
        print(f"{'='*70}")
        print(f"Data points:          {stats['n_points']}")
        print(f"Mean residual (counts): {stats['mean_counts']:>12.4f}")
        print(f"Std deviation (counts): {stats['std_counts']:>12.4f}")
        print(f"Min residual (counts):  {stats['min_counts']:>12.4f}")
        print(f"Max residual (counts):  {stats['max_counts']:>12.4f}")
        print(f"RMS (counts):           {stats['rms_counts']:>12.4f}")
        print(f"RMS (Casa-style):       {stats['rms_casa']:>12.4f}")
        #print(f"RMS (normalized):     {stats['rms_normalized']:>12.2f} %")
        print(f"Chi-squared:          {stats['chi_squared']:>12.4e}")
        print(f"Reduced chi-squared:  {stats['reduced_chi_squared']:>12.4f}")
        print(f"{'='*70}\n")
