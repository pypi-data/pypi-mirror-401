from typing import Optional, Dict
import pandas as pd
from ..elements.reference_table import XPSElementInfo, ElementReferenceTable

class XPSQuantification:
    """Quantitative XPS analysis using relative sensitivity factors."""
    
    def __init__(self, reference_table: Optional[ElementReferenceTable] = None):
        """Initialize quantification tools."""
        self.ref_table = reference_table or ElementReferenceTable()
    
    def calculate_composition(self, fitted_peaks: Dict[str, Dict]) -> pd.DataFrame:
        """
        Calculate atomic composition from fitted peak areas.
        
        Parameters
        ----------
        fitted_peaks : Dict[str, Dict]
            Dictionary mapping element orbital (e.g., 'O1s', 'C1s') to fitted data:
            {
                'O1s': {'area': 1500.0, 'uncertainty': 50.0},
                'C1s': {'area': 3200.0, 'uncertainty': 100.0}
            }
            
        Returns
        -------
        pd.DataFrame
            Composition table with: Element, Area, Sensitivity Factor, 
            Relative Sensitivity, At. %, At. % ±
        """
        results = []
        
        # Calculate I/λ (peak intensity / sensitivity factor)
        total_i_lambda = 0
        data_for_calc = []
        
        for peak_id, peak_data in fitted_peaks.items():
            # Parse element and orbital
            for key, elem_info in self.ref_table.elements.items():
                if key == peak_id:
                    area = peak_data['area']
                    sf = elem_info.sensitivity_factor
                    i_lambda = area / sf
                    
                    data_for_calc.append({
                        'element': elem_info.element,
                        'orbital': elem_info.orbital,
                        'peak_id': peak_id,
                        'area': area,
                        'sensitivity_factor': sf,
                        'i_lambda': i_lambda,
                        'uncertainty': peak_data.get('uncertainty', 0.05 * area)
                    })
                    total_i_lambda += i_lambda
                    break
        
        # Calculate atomic percentages
        for data in data_for_calc:
            at_percent = 100.0 * data['i_lambda'] / total_i_lambda
            rel_sf = data['i_lambda']
            
            # Propagate uncertainty (simplified)
            uncertainty_fraction = data['uncertainty'] / data['area']
            at_percent_err = at_percent * uncertainty_fraction
            
            results.append({
                'Element': data['element'],
                'Peak': data['peak_id'],
                'Area': f"{data['area']:.1f}",
                'Sensitivity Factor': f"{data['sensitivity_factor']:.3f}",
                'I/λ': f"{rel_sf:.2f}",
                'At. %': f"{at_percent:.2f}",
                'At. % ±': f"{at_percent_err:.2f}"
            })
        
        return pd.DataFrame(results)
    
    @staticmethod
    def estimate_sampling_depth(binding_energy: float) -> float:
        """
        Estimate electron inelastic mean free path (IMFP) and sampling depth.
        
        Uses Seah-Dench equation for solids (simplified).
        
        Parameters
        ----------
        binding_energy : float
            Binding energy in eV (kinetic energy of photoelectron)
            
        Returns
        -------
        float
            Sampling depth in nanometers (approximately 3x IMFP)
        """
        # Simplified IMFP calculation
        ke = max(50, binding_energy)  # Kinetic energy, minimum 50 eV
        
        # Seah-Dench IMFP equation (simplified)
        if ke < 150:
            imfp = 0.41 * ke**0.5
        elif ke < 500:
            imfp = 0.11 * ke - 7.1
        else:
            imfp = 0.025 * ke + 89
        
        sampling_depth = 3 * imfp / 1000  # Convert to nm, ×3 for effective depth
        return sampling_depth