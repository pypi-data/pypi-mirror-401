"""
XPS Analysis Framework

A modular, production-ready framework for X-ray Photoelectron Spectroscopy (XPS)
data fitting and analysis with interactive Jupyter workflow support.

Main Workflow:
1. Load data: dataset = XPSDataset(...)
2. Plot: dataset.plot_spectrum()
3. Calibrate: EnergyCalibrator.calibrate_by_offset(dataset, shift)
4. Find peaks: element = find_element_region(dataset)
5. Configure: Add fitting regions and constraints
6. Fit: fitter.fit_element()
7. Plot results: fitter.plot_element()
8. Analyze: results = all_results_func({'Fe': fitter_fe, ...})
9. Quantify: composition = quantification_func({'Fe': fitter_fe, ...})
10. Export: fitter.export_results(...)
"""

# Import main user-facing classes
from .core.dataset import XPSDataset
from .regions.elementregion import ElementRegion
from .regions.fittingregion import FittingRegion
from .regions.peakstack import XPSPeakStack

from .lineshapes.standard import VoigtLineShape, GaussianLineShape, LorentzianLineShape
from .lineshapes.custom import GaussianLorentzianMixLineShape, AsymmetricLineShape

from .constraints.standard import EqualityConstraint, OffsetConstraint, RatioConstraint

from .fitting.fitter import XPSElementFitter
from .core.workflow import XPSAnalysisWorkflow

from .calibration.calibrator import EnergyCalibrator
from .regions.reference import XPSReferenceDatabase, FittingRegionSuggestion
from .peakfinding.finder import find_element_region, PeakFinder

from .quantification.quantifier import QuantificationEngine
from .analysis.reporting import all_results_func, quantification_func, AnalysisReporter

from .io.constants import ENERGY_COL, INTENSITY_COL
from .io.loader import DataLoader

__version__ = "1.0.0"
__author__ = "XPS Analysis Team"

__all__ = [
    # Core classes
    "XPSDataset",
    "ElementRegion",
    "FittingRegion",
    "XPSPeakStack",
    
    # Line shapes
    "VoigtLineShape",
    "GaussianLineShape",
    "LorentzianLineShape",
    "GaussianLorentzianMixLineShape",
    "AsymmetricLineShape",
    
    # Constraints
    "EqualityConstraint",
    "OffsetConstraint",
    "RatioConstraint",
    
    # Fitting
    "XPSElementFitter",
    "XPSAnalysisWorkflow",
    
    # Calibration and peak finding
    "EnergyCalibrator",
    "XPSReferenceDatabase",
    "find_element_region",
    "PeakFinder",
    
    # Quantification and reporting
    "QuantificationEngine",
    "AnalysisReporter",
    "all_results_func",
    "quantification_func",
    
    # IO
    "DataLoader",
    "ENERGY_COL",
    "INTENSITY_COL",
]
