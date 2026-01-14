"""
High-level fitting orchestrator.

The XPSElementFitter manages the complete workflow for fitting all regions
within an ElementRegion with support for interactive fitting updates.
"""

from typing import Dict, Tuple, Optional, List
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from ..regions.elementregion import ElementRegion
from ..io.constants import ENERGY_COL, INTENSITY_COL
from ..analysis.residual_analysis import ResidualAnalysis

class XPSElementFitter:
    """
    Orchestrator for fitting all regions within an ElementRegion.
    
    Manages the complete fitting workflow with support for incremental fitting:
    regions can be fitted independently, and plots/results update to reflect
    current state (whether partial or complete).
    
    Attributes
    ----------
    element_region : ElementRegion
        The element region being fitted
    fitting_results : Dict[str, Any]
        Cached fit results by region name (empty dict if not yet fitted)
    background_subtractions : Dict[str, np.ndarray]
        Cached background arrays by region name
    """
    
    def __init__(self, element_region: ElementRegion):
        """Initialize the element fitter."""
        self.element_region = element_region
        self.fitting_results: Dict[str, Any] = {}
        self.background_subtractions: Dict[str, np.ndarray] = {}
        self.residual_analysis = ResidualAnalysis(self)  # Add residual tools
    
    def prepare_fitting_region(self, fitting_region: 'FittingRegion'
                              ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Extract and prepare data for a fitting region.
        
        Parameters
        ----------
        fitting_region : FittingRegion
            The region to prepare
            
        Returns
        -------
        Tuple[np.ndarray, np.ndarray, np.ndarray]
            (energy, raw_intensity, background_array)
        """
        
        e_min, e_max = fitting_region.energy_range
        mask = (self.element_region.dataset.df[ENERGY_COL] >= e_min) & \
               (self.element_region.dataset.df[ENERGY_COL] <= e_max)
        
        df_region = self.element_region.dataset.df[mask].copy()
        energy = df_region[ENERGY_COL].values
        intensity = df_region[INTENSITY_COL].values
        
        # Calculate background if not already done
        if fitting_region.background_array is None:
            fitting_region.set_background(self.element_region.dataset)
        
        background = fitting_region.background_array
        return energy, intensity, background
    
    def fit_region(self, fitting_region: 'FittingRegion',
                   print_info: bool = False) -> None:
        """
        Fit all peak stacks in a single fitting region.
        
        Parameters
        ----------
        fitting_region : FittingRegion
            Region to fit
        print_info : bool
            Whether to print detailed fit report
        """
        from scipy.optimize import minimize
        
        energy, intensity, background = self.prepare_fitting_region(fitting_region)
        bg_corrected = intensity - background
        
        # Fit each peak stack
        for peak_stack in fitting_region.peak_stacks:
            peak_stack.background_corrected_data = (energy, bg_corrected)
            model, params = peak_stack.build_composite_model()
            
            # Perform fit
            #result = model.fit(bg_corrected, params, x=energy)

            # --- Casa-style Poisson noise ---
            # Background-corrected signal is used for noise estimate
            #signal = np.maximum(bg_corrected, 1.0)
            #sigma = np.sqrt(signal)
            #weights = 1.0 / sigma
            raw_counts = np.maximum(intensity, 1.0)
            sigma = np.sqrt(raw_counts)
            weights = 1.0 / sigma

            # Perform weighted fit (THIS IS CRITICAL)
            result = model.fit(
                bg_corrected,
                params,
                x=energy,
                weights=weights
            )
            
            # Store results
            self.fitting_results[fitting_region.name] = {
                'region': fitting_region,
                'stack': peak_stack,
                'result': result,
                'energy': energy,
                'intensity': intensity,
                'background': background,
                'sigma': sigma
            }
            
            if print_info:
                print(f"\nFit results for {fitting_region.name}:")
                #print(f"Chi-squared: {result.chisqr:.4e}")
                #print(f"Reduced chi-squared: {result.redchi:.4e}")

                # Also print residual info
                residual_rms = self.residual_analysis.get_residual_rms(
                    fitting_region.name
                )
                if residual_rms is not None:
                    rms_counts = self.residual_analysis.get_residual_rms(fitting_region.name)
                    rms_rel = self.residual_analysis.get_normalized_rms(fitting_region.name)
                    rms_casa = self.residual_analysis.get_casa_rms(fitting_region.name)
                    
                    #print(f"RMS (counts):        {rms_counts:.2f}")
                    #print(f"RMS (relative):      {rms_rel:.2f} %")
                    print(f"RMS (Casa-style):    {rms_casa:.2f}")
                    #print(f"Reduced chi-squared: {result.redchi:.2f}")

                # Print GL mix info (if applicable)
                for line_shape in peak_stack.line_shapes:
                    if hasattr(line_shape, "describe_mix"):
                        mix_desc = line_shape.describe_mix(result.params)
                        if mix_desc:
                            print(f"  • {line_shape.name}: {mix_desc}")



    
    def fit_element(self, print_info: bool = True) -> None:
        """
        Fit all fitting regions in the element sequentially.
        
        Parameters
        ----------
        print_info : bool
            Whether to print fit reports for each region
        """
        for fitting_region in self.element_region.fitting_regions:
            self.fit_region(fitting_region, print_info)
    
    def has_results(self) -> bool:
        """
        Check if any fitting results exist.
        
        Returns
        -------
        bool
            True if at least one region has been fitted
        """
        return len(self.fitting_results) > 0
    
    def get_fitted_regions(self) -> List[str]:
        """
        Get names of regions that have been fitted.
        
        Returns
        -------
        List[str]
            Names of fitted regions
        """
        return list(self.fitting_results.keys())

    def _get_component_colors(self, n_components: int) -> List[str]:
        """
        Generate distinct colors for peak components.
        
        Parameters
        ----------
        n_components : int
            Number of components
            
        Returns
        -------
        List[str]
            Color hex codes
        """
        colors = [
            '#FF6B6B',  # Red
            '#4ECDC4',  # Teal
            '#45B7D1',  # Blue
            '#FFA07A',  # Light salmon
            '#98D8C8',  # Mint
            '#F7DC6F',  # Yellow
            '#BB8FCE',  # Purple
            '#85C1E2',  # Light blue
        ]
        return (colors * ((n_components // len(colors)) + 1))[:n_components]

    def _hex_to_rgba(self, hex_color: str, alpha: float = 0.15) -> str:
        """
        Convert hex color to rgba string with transparency.
        
        Parameters
        ----------
        hex_color : str
            Hex color code (e.g., '#FF6B6B')
        alpha : float
            Alpha transparency (0-1)
            
        Returns
        -------
        str
            RGBA color string (e.g., 'rgba(255, 107, 107, 0.15)')
        """
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f'rgba({r}, {g}, {b}, {alpha})'
    
        """
        Generate distinct colors for peak components.
        
        Parameters
        ----------
        n_components : int
            Number of components
            
        Returns
        -------
        List[str]
            Color hex codes
        """
        colors = [
            '#FF6B6B',  # Red
            '#4ECDC4',  # Teal
            '#45B7D1',  # Blue
            '#FFA07A',  # Light salmon
            '#98D8C8',  # Mint
            '#F7DC6F',  # Yellow
            '#BB8FCE',  # Purple
            '#85C1E2',  # Light blue
        ]
        return (colors * ((n_components // len(colors)) + 1))[:n_components]


    
    def plot_region(self, fitting_region_name: str,
                   title: Optional[str] = None,
                   show_components: bool = True) -> go.Figure:
        """
        Generate interactive plot of a region (fitted or not).
        
        If region has not been fitted, shows raw data and background only.
        If fitted, shows data, fit curve, and components.
        
        Parameters
        ----------
        fitting_region_name : str
            Name of fitting region to plot
        title : str, optional
            Custom plot title
        show_components : bool
            Whether to show individual peak components (only if fitted)
            
        Returns
        -------
        go.Figure
            Plotly figure object
        """
        import plotly.graph_objects as go
        
        if fitting_region_name not in self.fitting_results:
            # Return unfitted plot
            for fr in self.element_region.fitting_regions:
                if fr.name == fitting_region_name:
                    energy, intensity, background = self.prepare_fitting_region(fr)
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=energy, y=intensity, mode='lines',
                                            name='Raw Data', line=dict(color='black')))
                    fig.add_trace(go.Scatter(x=energy, y=background, mode='lines',
                                            name='Background', line=dict(color='red')))
                    fig.update_layout(title=title or f"{fitting_region_name} (Not Fitted)",
                                     xaxis_title="Binding Energy (eV)",
                                     yaxis_title="Intensity")
                    return fig
        
        result_data = self.fitting_results[fitting_region_name]
        result = result_data['result']
        energy = result_data['energy']
        intensity = result_data['intensity']
        background = result_data['background']
        
        fig = go.Figure()
        
        # Raw data
        fig.add_trace(go.Scatter(x=energy, y=intensity, mode='lines',
                                name='Raw Data', line=dict(color='black', width=2)))
        
        # Background
        fig.add_trace(go.Scatter(x=energy, y=background, mode='lines',
                                name='Background', line=dict(color='red')))
        
        # Fit curve
        fig.add_trace(go.Scatter(x=energy, y=result.best_fit + background,
                                mode='lines', name='Fit',
                                line=dict(color='blue', width=2)))
        
        # Components
        if show_components:
            for comp_name, comp in result.eval_components().items():
                fig.add_trace(go.Scatter(x=energy, y=comp + background,
                                        mode='lines', name=comp_name,
                                        line=dict(dash='dash')))
        
        fig.update_layout(title=title or f"{fitting_region_name}",
                         xaxis_title="Binding Energy (eV)",
                         yaxis_title="Intensity",
                         hovermode='x unified')
        
        return fig

    def plot_region_casa(self, fitting_region_name: str,
                   title: Optional[str] = None,
                   show_components: bool = True,
                   fill_components: bool = False) -> go.Figure:
        """
        Generate interactive Casa-style plot of a region (fitted or not).
        
        If region has not been fitted, shows raw data and background only.
        If fitted, shows data points, background line, fit curve, and components.
        
        Features:
        - Data as scatter points
        - Background and fit as lines
        - Full frame with inward-pointing ticks
        - Optional color fill for components
        - Extra padding left/right for visibility
        
        Parameters
        ----------
        fitting_region_name : str
            Name of fitting region to plot
        title : str, optional
            Custom plot title
        show_components : bool
            Whether to show individual peak components
        fill_components : bool
            Whether to fill component areas with color (Casa-style)
            
        Returns
        -------
        go.Figure
            Plotly figure object
        """
        import plotly.graph_objects as go
        
        if fitting_region_name not in self.fitting_results:
            # Return unfitted plot
            for fr in self.element_region.fitting_regions:
                if fr.name == fitting_region_name:
                    energy, intensity, background = self.prepare_fitting_region(fr)
                    
                    # Add padding
                    e_range = energy.max() - energy.min()
                    e_min = energy.min() - 0.1 * e_range
                    e_max = energy.max() + 0.1 * e_range
                    
                    fig = go.Figure()
                    
                    # Data as points
                    fig.add_trace(go.Scatter(
                        x=energy, y=intensity,
                        mode='markers',
                        name='Data',
                        marker=dict(size=4, color='black', opacity=0.6),
                        hovertemplate='<b>Energy:</b> %{x:.2f} eV<br><b>Intensity:</b> %{y:.1f}<extra></extra>'
                    ))
                    
                    # Background as line
                    fig.add_trace(go.Scatter(
                        x=energy, y=background,
                        mode='lines',
                        name='Background',
                        line=dict(color='red', width=2, dash='solid'),
                        hovertemplate='<b>Background:</b> %{y:.1f}<extra></extra>'
                    ))
                    
                    fig.update_layout(
                        title=title or f"{fitting_region_name} (Not Fitted)",
                        xaxis_title="Binding Energy (eV)",
                        yaxis_title="Intensity (counts)",
                        template="plotly_white",
                        hovermode='x unified',
                        height=600,
                        width=1200,
                        xaxis=dict(
                            autorange="reversed",
                            range=[e_max, e_min],
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='lightgray',
                            showline=True,
                            linewidth=2,
                            linecolor='black',
                            mirror=True,
                            ticks='inside'
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridwidth=1,
                            gridcolor='lightgray',
                            showline=True,
                            linewidth=2,
                            linecolor='black',
                            mirror=True,
                            ticks='inside'
                        ),
                        plot_bgcolor='white',
                        margin=dict(l=80, r=50, t=100, b=80)
                    )
                    
                    return fig
        
        result_data = self.fitting_results[fitting_region_name]
        result = result_data['result']
        energy = result_data['energy']
        intensity = result_data['intensity']
        background = result_data['background']
        
        # Add padding
        e_range = energy.max() - energy.min()
        e_min = energy.min() - 0.1 * e_range
        e_max = energy.max() + 0.1 * e_range
        
        fig = go.Figure()
        
        # Data as points (scatter)
        fig.add_trace(go.Scatter(
            x=energy, y=intensity,
            mode='markers',
            name='Data',
            marker=dict(size=4, color='black', opacity=0.7),
            hovertemplate='<b>Energy:</b> %{x:.2f} eV<br><b>Intensity:</b> %{y:.1f}<extra></extra>'
        ))
        
        # Background as line
        fig.add_trace(go.Scatter(
            x=energy, y=background,
            mode='lines',
            name='Background',
            line=dict(color='red', width=2),
            hovertemplate='<b>Background:</b> %{y:.1f}<extra></extra>'
        ))
        
        # Fit curve as line
        fit_values = result.best_fit + background
        fig.add_trace(go.Scatter(
            x=energy, y=fit_values,
            mode='lines',
            name='Fit Envelope',
            line=dict(color='blue', width=3),
            hovertemplate='<b>Fit:</b> %{y:.1f}<extra></extra>'
        ))
        
        # Components with optional fill
        if show_components:
            components = result.eval_components()
            colors = self._get_component_colors(len(components))
            
            for i, (comp_name, comp) in enumerate(components.items()):
                comp_values = comp + background
                
                if fill_components:
                    # Filled area under component (light and transparent)
                    # Use rgba with alpha channel for real transparency
                    rgba_color = self._hex_to_rgba(colors[i], alpha=0.15)
                    fig.add_trace(go.Scatter(
                        x=energy, y=comp_values,
                        mode='lines',
                        name=comp_name,
                        line=dict(color=colors[i], width=1.5),
                        fill='tozeroy',
                        fillcolor=rgba_color,
                        hovertemplate=f'<b>{comp_name}:</b> %{{y:.1f}}<extra></extra>'
                    ))
                else:
                    # Line only
                    fig.add_trace(go.Scatter(
                        x=energy, y=comp_values,
                        mode='lines',
                        name=comp_name,
                        line=dict(color=colors[i], width=2, dash='dash'),
                        hovertemplate=f'<b>{comp_name}:</b> %{{y:.1f}}<extra></extra>'
                    ))
        
        fig.update_layout(
            title=title or f"{fitting_region_name} - Fit",
            xaxis_title="Binding Energy (eV)",
            yaxis_title="Intensity (counts)",
            template="plotly_white",
            hovermode='x unified',
            height=600,
            width=1200,
            xaxis=dict(
                autorange="reversed",
                range=[e_max, e_min],
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True,
                ticks='inside',
                ticklen=6
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True,
                ticks='inside',
                ticklen=6
            ),
            plot_bgcolor='white',
            margin=dict(l=80, r=50, t=100, b=80)
        )
        
        return fig

    def plot_region_with_residuals(self, fitting_region_name: str,
                                    show_components: bool = True) -> Dict[str, go.Figure]:
        """
        Generate multiple plots for a region: fit + residuals.
        
        Returns
        -------
        dict
            {'fit': Figure, 'residuals': Figure, 'normalized_residuals': Figure}
        """
        plots = {}
        
        # Main fit plot
        if fitting_region_name not in self.fitting_results:
            raise ValueError(f"No results for region '{fitting_region_name}'")
        
        result_data = self.fitting_results[fitting_region_name]
        result = result_data['result']
        energy = result_data['energy']
        intensity = result_data['intensity']
        background = result_data['background']
        
        fig_fit = go.Figure()
        fig_fit.add_trace(go.Scatter(x=energy, y=intensity, mode='lines',
                                    name='Raw Data', line=dict(color='black', width=2)))
        fig_fit.add_trace(go.Scatter(x=energy, y=background, mode='lines',
                                    name='Background', line=dict(color='red')))
        fig_fit.add_trace(go.Scatter(x=energy, y=result.best_fit + background,
                                    mode='lines', name='Fit',
                                    line=dict(color='blue', width=2)))
        
        if show_components:
            for comp_name, comp in result.eval_components().items():
                fig_fit.add_trace(go.Scatter(x=energy, y=comp + background,
                                            mode='lines', name=comp_name,
                                            line=dict(dash='dash')))
        
        fig_fit.update_layout(
            title=f"{fitting_region_name} - Fit",
            xaxis_title="Binding Energy (eV)",
            yaxis_title="Intensity",
            template="plotly_white",
            hovermode='x unified',
            height=500,
            width=1000,
            xaxis=dict(autorange="reversed")
        )
        plots['fit'] = fig_fit
        
        # Residuals plot
        plots['residuals'] = self.residual_analysis.plot_residuals(
            fitting_region_name
        )
        
        # Normalized residuals plot
        plots['normalized_residuals'] = \
            self.residual_analysis.plot_normalized_residuals(
                fitting_region_name
            )
        
        return plots

    def plot_region_with_residuals_casa(self, fitting_region_name: str,
                                    show_components: bool = True,
                                    fill_components: bool = False) -> Dict[str, go.Figure]:
        """
        Generate multiple plots for a region: fit + residuals + background.
        
        Parameters
        ----------
        fitting_region_name : str
            Region name
        show_components : bool
            Show individual peaks
        fill_components : bool
            Fill component areas with color
        
        Returns
        -------
        dict
            {'fit': Figure, 'residuals': Figure, 'background': Figure}
        """
        plots = {}
        
        # Main fit plot
        if fitting_region_name not in self.fitting_results:
            raise ValueError(f"No results for region '{fitting_region_name}'")
        
        result_data = self.fitting_results[fitting_region_name]
        result = result_data['result']
        energy = result_data['energy']
        intensity = result_data['intensity']
        background = result_data['background']
        
        # Add padding
        e_range = energy.max() - energy.min()
        e_min = energy.min() - 0.1 * e_range
        e_max = energy.max() + 0.1 * e_range
        
        # ===== FIT PLOT =====
        fig_fit = go.Figure()
        
        # Data as points
        fig_fit.add_trace(go.Scatter(
            x=energy, y=intensity,
            mode='markers',
            name='Data',
            marker=dict(size=4, color='black', opacity=0.7),
            hovertemplate='<b>Energy:</b> %{x:.2f} eV<br><b>Intensity:</b> %{y:.1f}<extra></extra>'
        ))
        
        # Background
        fig_fit.add_trace(go.Scatter(
            x=energy, y=background,
            mode='lines',
            name='Background',
            line=dict(color='red', width=2),
            hovertemplate='<b>Background:</b> %{y:.1f}<extra></extra>'
        ))
        
        # Fit envelope
        fit_values = result.best_fit + background
        fig_fit.add_trace(go.Scatter(
            x=energy, y=fit_values,
            mode='lines',
            name='Fit Envelope',
            line=dict(color='blue', width=3),
            hovertemplate='<b>Fit:</b> %{y:.1f}<extra></extra>'
        ))
        
        # Components
        if show_components:
            components = result.eval_components()
            colors = self._get_component_colors(len(components))
            
            for i, (comp_name, comp) in enumerate(components.items()):
                comp_values = comp + background
                
                if fill_components:
                    rgba_color = self._hex_to_rgba(colors[i], alpha=0.15)
                    fig_fit.add_trace(go.Scatter(
                        x=energy, y=comp_values,
                        mode='lines',
                        name=comp_name,
                        line=dict(color=colors[i], width=1.5),
                        fill='tozeroy',
                        fillcolor=rgba_color,
                        hovertemplate=f'<b>{comp_name}:</b> %{{y:.1f}}<extra></extra>'
                    ))
                else:
                    fig_fit.add_trace(go.Scatter(
                        x=energy, y=comp_values,
                        mode='lines',
                        name=comp_name,
                        line=dict(color=colors[i], width=2, dash='dash'),
                        hovertemplate=f'<b>{comp_name}:</b> %{{y:.1f}}<extra></extra>'
                    ))
        
        fig_fit.update_layout(
            title=f"{fitting_region_name} - Fit",
            xaxis_title="Binding Energy (eV)",
            yaxis_title="Intensity (counts)",
            template="plotly_white",
            hovermode='x unified',
            height=600,
            width=1200,
            xaxis=dict(
                autorange="reversed",
                range=[e_max, e_min],
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True,
                ticks='inside',
                ticklen=6
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True,
                ticks='inside',
                ticklen=6
            ),
            plot_bgcolor='white',
            margin=dict(l=80, r=50, t=100, b=80)
        )
        plots['fit'] = fig_fit
          
        # ===== RESIDUALS PLOT =====
        plots['residuals'] = self.residual_analysis.plot_residuals(
            fitting_region_name
        )
        
        return plots
    
    def plot_element(self) -> Dict[str, go.Figure]:
        """
        Generate plots for all regions in the element.
        
        Returns plots even for regions not yet fitted (showing raw data/background).
        
        Returns
        -------
        Dict[str, go.Figure]
            Mapping of region names to plot figures
        """
        plots = {}
        for fitting_region in self.element_region.fitting_regions:
            plots[fitting_region.name] = self.plot_region(fitting_region.name)
        return plots

    def plot_element_casa(self) -> Dict[str, go.Figure]:
        """
        Generate plots for all regions in the element.
        
        Returns plots even for regions not yet fitted (showing raw data/background).
        
        Returns
        -------
        Dict[str, go.Figure]
            Mapping of region names to plot figures
        """
        plots = {}
        for fitting_region in self.element_region.fitting_regions:
            plots[fitting_region.name] = self.plot_region_casa(fitting_region.name)
        return plots
    
    def get_results_table(self, fitting_region_name: str,
                         include_errors: bool = True) -> pd.DataFrame:
        """
        Extract peak parameters as a formatted table.
        
        If region not yet fitted, returns empty DataFrame.
        
        Parameters
        ----------
        fitting_region_name : str
            Name of fitting region
        include_errors : bool
            Include error estimates
            
        Returns
        -------
        pd.DataFrame
            Table with: peak_name, center, center_err, amplitude, amplitude_err,
            fwhm, fwhm_err, area, area_err, reduced_chi_sq (if fitted)
        """
        if fitting_region_name not in self.fitting_results:
            return pd.DataFrame()
        
        result_data = self.fitting_results[fitting_region_name]
        result = result_data['result']
        
        rows = []
        for param_name, param in result.params.items():
            if 'center' in param_name:
                rows.append({
                    'parameter': param_name,
                    'value': param.value,
                    'stderr': param.stderr if include_errors else None
                })
        
        return pd.DataFrame(rows)
    
    def export_results(self, output_path: str, format: str = "csv") -> None:
        """
        Export all results to file(s).
        
        Parameters
        ----------
        output_path : str
            Output file or directory path
        format : str
            Export format ('csv', 'excel', 'json')
        """
        import os
        os.makedirs(output_path, exist_ok=True)
        
        for region_name, result_data in self.fitting_results.items():
            table = self.get_results_table(region_name)
            
            if format == "csv":
                table.to_csv(f"{output_path}/{region_name}.csv")
            elif format == "excel":
                table.to_excel(f"{output_path}/{region_name}.xlsx")
            elif format == "json":
                table.to_json(f"{output_path}/{region_name}.json")
    
    def get_fit_statistics(self, fitting_region_name: str) -> Optional[dict]:
        """
        Get goodness-of-fit metrics for a region.
        
        Returns None if region not yet fitted.
        
        Parameters
        ----------
        fitting_region_name : str
            Region name
            
        Returns
        -------
        dict or None
            Contains: chi_squared, reduced_chi_squared, AIC, BIC, R_squared,
            or None if not fitted
        """
        if fitting_region_name not in self.fitting_results:
            return None
        
        result = self.fitting_results[fitting_region_name]['result']
        
        return {
            'chi_squared': result.chisqr,
            'reduced_chi_squared': result.redchi,
            'aic': result.aic,
            'bic': result.bic,
            'nvarys': result.nvarys
        }

    def export_fit_report(self, fitting_region_name: str,
                         output_file: str = "fit_report.txt") -> None:
        """Export detailed fit report including residuals."""
        if fitting_region_name not in self.fitting_results:
            raise ValueError(f"No results for region '{fitting_region_name}'")
        
        result_data = self.fitting_results[fitting_region_name]
        result = result_data['result']
        
        with open(output_file, 'w') as f:
            f.write(f"{'='*70}\n")
            f.write(f"XPS FIT REPORT - {fitting_region_name}\n")
            f.write(f"{'='*70}\n\n")
            
            # Fit statistics
            f.write("FIT STATISTICS:\n")
            f.write(f"Chi-squared:          {result.chisqr:.6e}\n")
            f.write(f"Reduced chi-squared:  {result.redchi:.6f}\n")
            f.write(f"AIC:                  {result.aic:.2f}\n")
            f.write(f"BIC:                  {result.bic:.2f}\n")
            f.write(f"Number of variables:  {result.nvarys}\n")
            f.write(f"Number of data points: {result.ndata}\n\n")
            
            # Residual statistics
            stats = self.residual_analysis.get_residual_statistics(
                fitting_region_name
            )
            f.write("RESIDUAL STATISTICS:\n")
            f.write(f"RMS:                  {stats['rms_casa']:.6f}\n")
            #f.write(f"RMS (normalized):     {stats['rms_normalized']:.2f} %\n")
            f.write(f"Mean:                 {stats['mean_counts']:.6f}\n")
            f.write(f"Std dev:              {stats['std_counts']:.6f}\n")
            f.write(f"Min:                  {stats['min_counts']:.6f}\n")
            f.write(f"Max:                  {stats['max_counts']:.6f}\n\n")
            
            # Parameters
            f.write("FITTED PARAMETERS:\n")
            f.write(result.fit_report())
