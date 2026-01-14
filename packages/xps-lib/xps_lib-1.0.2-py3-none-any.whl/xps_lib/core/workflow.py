"""
High-level workflow management.

Defines a complete XPS analysis workflow from data loading through
results export.
"""

import numpy as np
import pandas as pd

from typing import List, Dict, Optional, Tuple
from ..regions.elementregion import ElementRegion
from ..fitting.fitter import XPSElementFitter
from ..elements.reference_table import ElementReferenceTable
from ..analysis.residual_analysis import ResidualAnalysis
from ..quantification.quantifier import XPSQuantification

class XPSWorkflow:
    """
    Interactive XPS workflow for Jupyter-style usage.

    Supports:
      - incremental element fitting
      - immediate inspection
      - deferred quantification
    """

    def __init__(self, dataset, reference_table: ElementReferenceTable):
        self.dataset = dataset
        self.reference_table = reference_table

        self.elements: dict[str, ElementRegion] = {}
        self.fitters: dict[str, XPSElementFitter] = {}

        self.quant_lineshapes: Dict[Tuple[str, str], List[str]] = {}

        self.composition = None

    # ------------------------------------------------------------------
    # Element registration
    # ------------------------------------------------------------------

    def register_element(self, element: ElementRegion):
        self.elements[element.element] = element
        return element

    def set_quantification_lineshapes(self, element: str, region: str, 
                                      prefixes: List[str]):
        """
        Set which lineshapes to use for quantification for a given element/region.
        
        This allows you to use only specific peaks in quantification while still
        fitting all peaks. For example, fit both Al 2p3/2 (p0_) and Al 2p1/2 (p1_)
        together, but only use p0_ for quantification to avoid double-counting.
        
        Parameters
        ----------
        element : str
            Element symbol (e.g., 'Al', 'N', 'C')
        region : str
            Fitting region name (e.g., 'Al2p', 'N1s')
        prefixes : List[str]
            List of lmfit prefixes to include (e.g., ['p0_'] for first peak only,
            or ['p0_', 'p1_'] for both peaks). Standard lmfit prefixes are:
            'p0_' (first lineshape), 'p1_' (second), 'p2_' (third), etc.
            
        Example
        -------
        >>> workflow = XPSWorkflow(dataset, ref_table)
        
        >>> # Setup N 1s (single peak)
        >>> element_n = ElementRegion("N", "1s", dataset)
        >>> workflow.register_element(element_n)
        >>> # ... add fitting region with one lineshape (p0_) ...
        >>> workflow.fit_element("N")
        >>> workflow.set_quantification_lineshapes("N", "N1s", ["p0_"])
        
        >>> # Setup Al 2p (two peaks: 2p3/2 and 2p1/2)
        >>> element_al = ElementRegion("Al", "2p3/2", dataset)
        >>> workflow.register_element(element_al)
        >>> # ... add fitting region with TWO lineshapes (p0_ and p1_) ...
        >>> workflow.fit_element("Al")
        >>> # Only use Al 2p3/2 (p0_) for quantification, skip p1_ (2p1/2)
        >>> workflow.set_quantification_lineshapes("Al", "Al2p", ["p0_"])
        
        >>> # Calculate composition without double-counting Al
        >>> composition = workflow.quantify()
        """
        key = (element, region)
        self.quant_lineshapes[key] = prefixes
        print(f"Set quantification lineshapes for {element}/{region}: {prefixes}")

    def get_quantification_lineshapes(self) -> Dict[Tuple[str, str], List[str]]:
        """
        Get current quantification lineshape configuration.
        
        Returns
        -------
        Dict[Tuple[str, str], List[str]]
            Mapping of (element, region) -> list of prefixes
        """
        return self.quant_lineshapes.copy()


    # ------------------------------------------------------------------
    # Incremental fitting
    # ------------------------------------------------------------------

    def fit_element(self, element: str, print_info: bool = True):
        if element not in self.elements:
            raise KeyError(f"Element '{element}' is not registered")

        fitter = XPSElementFitter(self.elements[element])
        fitter.fit_element(print_info=print_info)

        self.fitters[element] = fitter
        return fitter

    # ------------------------------------------------------------------
    # Accessors (post-fit)
    # ------------------------------------------------------------------

    def fitter(self, element: str) -> XPSElementFitter:
        if element not in self.fitters:
            raise KeyError(f"Element '{element}' has not been fitted yet")
        return self.fitters[element]

    def results(self, element: str):
        return self.fitter(element).fitting_results

    def residuals(self, element: str):
        return self.fitter(element).residual_analysis

    # ------------------------------------------------------------------
    # Plotting
    # ------------------------------------------------------------------

    def plot(self, element: str, show_components: bool = True, 
             fill_components: bool = False):
        """
        Plot all fitting regions for an element.
        
        Shows fit, residuals, and background subtraction.
        Automatically displays all plots without requiring manual .show() calls.
        
        Parameters
        ----------
        element : str
            Element symbol (e.g., 'Al', 'N')
        show_components : bool
            Whether to show individual peak components
        fill_components : bool
            Whether to fill component areas with color (Casa-style)
        """
        if element not in self.fitters:
            raise KeyError(f"Element '{element}' has not been fitted yet")
        
        fitter = self.fitters[element]
        
        # Get all regions for this element
        if element not in self.elements:
            raise KeyError(f"Element '{element}' is not registered")
        
        element_region = self.elements[element]

        self.peak_summary(element)
        self.constraint_summary(element)
        
        # Plot each fitting region
        for fitting_region in element_region.fitting_regions:
            region_name = fitting_region.name
            plots = fitter.plot_region_with_residuals_casa(
                region_name, 
                show_components=show_components,
                fill_components=fill_components
            )
            
            print(f"\n{'='*80}")
            print(f"PLOTS FOR {element} - {region_name}")
            print(f"{'='*80}\n")
            
            # Display all plots
            if "fit" in plots:
                plots["fit"].show()
            if "residuals" in plots:
                plots["residuals"].show()
            #if "background" in plots:
                #plots["background"].show()

    def plot_region(self, element: str, region: str, show_components=True):
        fitter = self.fitter(element)
        plots = fitter.plot_region_with_residuals_casa(
            region, show_components=show_components
        )
        plots["fit"].show()
        plots["residuals"].show()
        return plots

    # ------------------------------------------------------------------
    # Quantification
    # ------------------------------------------------------------------

    def quantify(self, elements: List[str] | str | None = None) -> pd.DataFrame:
        """
        Calculate atomic composition from fitted elements.
        
        Uses only the lineshapes specified in set_quantification_lineshapes()
        to avoid double-counting peaks like Al 2p3/2 and 2p1/2.
        
        Parameters
        ----------
        elements : List[str] | str, optional
            Which elements to include. If None, uses all fitted elements.
            
        Returns
        -------
        pd.DataFrame
            Composition table with Element, Peak, Area, Sensitivity Factor, etc.
        """
        if not self.fitters:
            raise RuntimeError("No fitted elements available for quantification")
    
        # Normalize input
        if elements is None:
            elements = list(self.fitters.keys())
        elif isinstance(elements, str):
            elements = [elements]
    
        self._quantified_elements = elements
    
        from ..quantification.quantifier import XPSQuantification
        quantifier = XPSQuantification(self.reference_table)
    
        fitted_peaks = {}
    
        print("\n" + "="*80)
        print("EXTRACTING PEAKS FOR QUANTIFICATION")
        print("="*80)
    
        for element in elements:
            if element not in self.fitters:
                raise KeyError(f"Element '{element}' has not been fitted")
    
            fitter = self.fitters[element]
            print(f"\nElement: {element}")
    
            for region_name, data in fitter.fitting_results.items():
                result = data["result"]
                
                print(f"  Region: {region_name}")
    
                # Get allowed lineshapes for this element/region
                allowed_prefixes = self.quant_lineshapes.get(
                    (element, region_name), None
                )
    
                if allowed_prefixes is None:
                    print(f"     No lineshape selection set. Using ALL peaks.")
                    allowed_prefixes = None  # Use all
    
                # Extract all amplitude parameters
                for name, param in result.params.items():
                    if not name.endswith("_amplitude"):
                        continue
    
                    prefix = name.replace("_amplitude", "")
                    
                    # Skip if not in allowed list
                    if allowed_prefixes is not None and prefix not in allowed_prefixes:
                        print(f"    → Skipping {prefix} (not selected)")
                        continue
    
                    # Get sigma parameter
                    sigma = result.params.get(f"{prefix}_sigma")
                    if sigma is None:
                        print(f"    ✗ {prefix}: no sigma found")
                        continue
    
                    # Calculate area
                    amplitude = param.value
                    sigma_val = sigma.value
                    area = amplitude * sigma_val * np.sqrt(2 * np.pi)
    
                    # Build peak ID using element and region
                    # Key insight: Use the element as key, since reference table has element-based keys
                    peak_id = f"{element}{region_name.replace(element, '').replace(f'{element[0]}', '')}"
                    
                    # For simple cases where region name = element+orbital
                    # e.g., region_name = "N1s" for element "N" with orbital "1s"
                    # Just use the reference table key directly
                    
                    # Find matching element in reference table
                    ref_key = None
                    for key in self.reference_table.elements.keys():
                        if key.startswith(element):
                            ref_key = key
                            break
                    
                    if ref_key is None:
                        print(f"     {prefix}: Element {element} not found in reference table")
                        continue
    
                    print(f"     {prefix}: area={area:.2f}, using {ref_key}")
    
                    fitted_peaks[ref_key] = {
                        "area": area,
                        "uncertainty": area * 0.05,
                    }
    
        print("\n" + "="*80)
        print(f"QUANTIFICATION - {len(fitted_peaks)} peaks extracted")
        print("="*80)
    
        if len(fitted_peaks) == 0:
            raise RuntimeError(
                "No peaks were extracted for quantification. "
                "Check your reference table and quantification settings."
            )
    
        print(f"\nPeaks to quantify: {list(fitted_peaks.keys())}")
        
        self.composition = quantifier.calculate_composition(fitted_peaks)
        
        #print(f"\nComposition dataframe shape: {self.composition.shape}")
        #print(f"Columns: {self.composition.columns.tolist()}")
        
        return self.composition
    
    def composition_summary(self) -> pd.DataFrame:
        """
        Get clean summary of composition by element.
        
        Returns
        -------
        pd.DataFrame
            Simple table with Element, At. %, At. % ±
        """
        if self.composition is None:
            raise RuntimeError("No composition calculated yet. Run quantify() first.")
        
        df = self.composition.copy()
        
        #print(f"\nComposition dataframe info:")
        #print(f"  Shape: {df.shape}")
        #print(f"  Columns: {df.columns.tolist()}")
        #print(f"  Data:\n{df}")
        
        if df.empty:
            raise RuntimeError(
                "Composition dataframe is empty! "
                "Check that quantify() extracted peaks correctly."
            )
        
        # Find columns - look for variations of "At. %"
        at_percent_col = None
        at_percent_err_col = None
        
        for col in df.columns:
            col_lower = str(col).lower()
            if "at" in col_lower and "%" in col_lower:
                if "±" in col or "+/-" in col or "err" in col_lower:
                    at_percent_err_col = col
                else:
                    at_percent_col = col
        
        if at_percent_col is None:
            print(f"DEBUG: Available columns: {df.columns.tolist()}")
            raise KeyError(
                f"Could not find 'At. %' column in composition. "
                f"Available columns: {df.columns.tolist()}"
            )
        
        # Convert to numeric
        df[at_percent_col] = pd.to_numeric(df[at_percent_col], errors='coerce')
        if at_percent_err_col:
            df[at_percent_err_col] = pd.to_numeric(df[at_percent_err_col], errors='coerce')
        
        # Group by element and sum
        summary = df.groupby("Element", as_index=False).agg({
            at_percent_col: "sum"
            #at_percent_col: "sum",
            #at_percent_err_col: "mean" if at_percent_err_col else "first"
        })
        
        # Rename columns
        #summary.columns = ["Element", "At. %", "At. % ±"]
        summary.columns = ["Element", "At. %"]
        
        # Filter to quantified elements if specified
        if hasattr(self, "_quantified_elements"):
            summary = summary[
                summary["Element"].isin(self._quantified_elements)
            ]
        
        return summary
    
    
    def peak_summary(self, element: str) -> pd.DataFrame:
        """
        Returns a per-component summary table with all peak parameters.
        
        Shows: Element | Region | Component | Position (eV) | FWHM (eV) | Area
        
        Parameters
        ----------
        element : str
            Element symbol (e.g., 'Al', 'N')
            
        Returns
        -------
        pd.DataFrame
            Summary table with all peak parameters
        """
        fitter = self.fitter(element)
        rows = []
        
        for region_name, data in fitter.fitting_results.items():
            result = data["result"]
            
            # Extract all peak components
            for name, param in result.params.items():
                if not name.endswith("_center"):
                    continue
                
                prefix = name.replace("_center", "")
                sigma_name = f"{prefix}_sigma"
                amp_name = f"{prefix}_amplitude"
                
                sigma = result.params.get(sigma_name)
                amp = result.params.get(amp_name)
                
                if sigma is None or amp is None:
                    continue
                
                position = param.value
                position_err = param.stderr if param.stderr else 0
                
                # Calculate FWHM from sigma
                fwhm = 2.3548 * sigma.value
                fwhm_err = 2.3548 * sigma.stderr if sigma.stderr else 0
                
                # Calculate area
                area = amp.value * sigma.value * np.sqrt(2 * np.pi)
                
                rows.append({
                    "Element": element,
                    "Region": region_name,
                    "Component": prefix,
                    "Position (eV)": f"{position:.4f}",
                    #"Position ± (eV)": f"{position_err:.4f}" if position_err else "—",
                    "FWHM (eV)": f"{fwhm:.4f}",
                    #"FWHM ± (eV)": f"{fwhm_err:.4f}" if fwhm_err else "—",
                    "Area": f"{area:.2f}",
                    "Amplitude": f"{amp.value:.2f}",
                    #"Sigma": f"{sigma.value:.4f}",
                })
        
        summary_df = pd.DataFrame(rows)
        
        # Print nicely formatted
        print(f"\n{'='*130}")
        print(f"PEAK COMPONENT SUMMARY - {element}")
        print(f"{'='*130}")
        print(summary_df.to_string(index=False))
        print(f"{'='*130}\n")
        
        return summary_df

    def constraint_summary(self, element: str) -> pd.DataFrame:
        """
        Returns a summary table of all constraints applied to an element.
        
        Shows the constraint type and parameters involved.
        
        Parameters
        ----------
        element : str
            Element symbol (e.g., 'Al', 'N')
            
        Returns
        -------
        pd.DataFrame
            Summary table with constraint details
        """
        if element not in self.elements:
            raise KeyError(f"Element '{element}' is not registered")
        
        element_region = self.elements[element]
        rows = []
        
        for fitting_region in element_region.fitting_regions:
            # Constraints within peak stacks
            for peak_stack in fitting_region.peak_stacks:
                for constraint in peak_stack.get_all_constraints():
                    rows.append({
                        "Region": fitting_region.name,
                        "Stack": peak_stack.name,
                        "Type": constraint.__class__.__name__,
                        "Description": constraint.description
                        #"Status": "Applied"
                    })
            
            # Cross-stack constraints
            for constraint in fitting_region.cross_stack_constraints:
                rows.append({
                    "Region": fitting_region.name,
                    "Stack": "Cross-stack",
                    "Type": constraint.__class__.__name__,
                    "Description": constraint.description
                    #"Status": "Applied"
                })
        
        summary_df = pd.DataFrame(rows)
        
        if len(summary_df) == 0:
            print(f"\nNo constraints defined for {element}")
            return summary_df
        
        # Print nicely formatted
        print(f"\n{'='*130}")
        print(f"CONSTRAINT SUMMARY - {element}")
        print(f"{'='*130}")
        print(summary_df.to_string(index=False))
        print(f"{'='*130}\n")
        
        return summary_df


    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export(self, elements: List[str] | None = None, prefix: str = ""):
        """
        Export all fit reports and composition.
        
        Parameters
        ----------
        elements : List[str], optional
            Which elements to export. If None, exports all.
        prefix : str
            Prefix for output filenames
        """
        if elements is None:
            elements = list(self.fitters.keys())

        for element in elements:
            fitter = self.fitters[element]
            for region in fitter.fitting_results:
                fitter.export_fit_report(
                    region, f"{prefix}{region}_fit_report.txt"
                )

        if self.composition is not None:
            with open(f"{prefix}quantification_report.txt", "w") as f:
                f.write("="*70 + "\n")
                f.write("QUANTIFICATION REPORT\n")
                f.write("="*70 + "\n\n")
                f.write("DETAILED RESULTS:\n")
                f.write(self.composition.to_string())
                f.write("\n\n")
                f.write("SUMMARY (by element):\n")
                f.write(self.composition_summary().to_string())

