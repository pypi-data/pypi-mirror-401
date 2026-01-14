"""
Core dataset representation and manipulation.

Defines the XPSDataset class for managing raw XPS spectra with calibration,
plotting, and interactive analysis tools.
"""

from typing import Optional, Tuple
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from xps_lib.io.constants import ENERGY_COL, INTENSITY_COL


class XPSDataset:
    """
    Represents a complete XPS spectrum or measurement.
    
    Encapsulates raw data with methods for preprocessing, calibration,
    visualization, and region selection.
    
    Attributes
    ----------
    df : pd.DataFrame
        Data frame with columns for energy and intensity
    name : str
        Descriptive name for this spectrum
    metadata : dict
        Additional information (acquisition parameters, etc.)
    calibration_offset : float
        Current energy calibration offset (eV) applied to data
    """
    
    def __init__(self, df: pd.DataFrame, name: Optional[str] = None,
                 metadata: Optional[dict] = None):
        """
        Initialize dataset.
        
        Parameters
        ----------
        df : pd.DataFrame
            Raw data with energy and intensity columns
        name : str, optional
            Dataset name
        metadata : dict, optional
            Acquisition metadata
        """
        self.df = df.copy()
        self.name = name or "Unnamed Dataset"
        self.metadata = metadata or {}
        self.calibration_offset = 0.0
    
    def plot_spectrum(self, title: Optional[str] = None,
                     energy_range: Optional[Tuple[float, float]] = None) -> go.Figure:
        """
        Generate interactive plot of the complete spectrum.
        
        Useful for initial data inspection and determining energy ranges.
        
        Parameters
        ----------
        title : str, optional
            Plot title
        energy_range : Tuple[float, float], optional
            Restrict plot to (min, max) eV. If None, shows full range.
            
        Returns
        -------
        go.Figure
            Plotly figure with full spectrum
        """
        df_plot = self.df.copy()
        
        # Filter by energy range if provided
        if energy_range:
            e_min, e_max = energy_range
            df_plot = df_plot[
                (df_plot[ENERGY_COL] >= min(e_min, e_max)) &
                (df_plot[ENERGY_COL] <= max(e_min, e_max))
            ]
        
        # Create plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_plot[ENERGY_COL],
            y=df_plot[INTENSITY_COL],
            mode='lines',
            name='Raw Data',
            line=dict(color='black', width=2)
        ))
        
        fig.update_layout(
            title=title or f"XPS Spectrum - {self.name}",
            xaxis_title="Binding Energy (eV)",
            yaxis_title="Intensity",
            template="plotly_white",
            hovermode='x unified',
            height=600,
            width=1200,
            xaxis=dict(autorange="reversed")
        )
        
        return fig
    
    def calibrate(self, shift_eV: float) -> None:
        """
        Apply energy calibration (binding energy shift).
        
        Shifts all energy values by the given offset. Useful when reference
        peaks (like C1s at 284.8 eV) need to be adjusted.
        
        Parameters
        ----------
        shift_eV : float
            Energy shift to apply (eV). Can be positive or negative.
            
        Note
        ----
        This modifies the dataset in-place. The shift is cumulative if called
        multiple times.
        """
        self.df[ENERGY_COL] = self.df[ENERGY_COL] + shift_eV
        self.calibration_offset += shift_eV
    
    def get_calibration_offset(self) -> float:
        """
        Get the current calibration offset applied.
        
        Returns
        -------
        float
            Current calibration offset in eV
        """
        return self.calibration_offset
    
    def normalize(self, method: str = "max") -> None:
        """
        Normalize intensity.
        
        Parameters
        ----------
        method : str
            Normalization method ('max', 'area', 'minmax')
            
        Raises
        ------
        ValueError
            If method is not supported
        """
        pass
    
    def select_region(self, energy_range: Tuple[float, float]) -> 'XPSDataset':
        """
        Extract a subset of the data.
        
        Parameters
        ----------
        energy_range : Tuple[float, float]
            (min, max) binding energy (eV)
            
        Returns
        -------
        XPSDataset
            New dataset containing only the specified range
        """
        e_min, e_max = energy_range
        
        mask = (self.df[ENERGY_COL] >= min(e_min, e_max)) & \
               (self.df[ENERGY_COL] <= max(e_min, e_max))
        
        df_subset = self.df[mask].copy()
        return XPSDataset(df_subset, name=f"{self.name}_region", metadata=self.metadata)
    
    def copy(self) -> 'XPSDataset':
        """
        Create a deep copy of this dataset.
        
        Returns
        -------
        XPSDataset
            Independent copy
        """
        new_dataset = XPSDataset(self.df.copy(), name=self.name,
                                metadata=self.metadata.copy())
        new_dataset.calibration_offset = self.calibration_offset
        return new_dataset
    
    def get_info(self) -> dict:
        """
        Get dataset information summary.
        
        Returns
        -------
        dict
            Contains: name, n_points, energy_range, intensity_range, metadata,
            calibration_offset
        """
        return {
            'name': self.name,
            'n_points': len(self.df),
            'energy_range': (self.df[ENERGY_COL].min(), self.df[ENERGY_COL].max()),
            'intensity_range': (self.df[INTENSITY_COL].min(), self.df[INTENSITY_COL].max()),
            'metadata': self.metadata,
            'calibration_offset': self.calibration_offset
        }
