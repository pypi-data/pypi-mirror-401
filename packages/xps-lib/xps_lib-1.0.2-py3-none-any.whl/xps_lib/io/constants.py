"""
Global constants and standard column names.

Defines naming conventions and standard parameters.
"""

# Standard column names
ENERGY_COL = "Energy (BE/eV)"
INTENSITY_COL = "Intensity"

# Background method column names
LINEAR_BACKGROUND_COL = "background_linear"
SHIRLEY_BACKGROUND_COL = "background_shirley"
TOUGAARD_BACKGROUND_COL = "background_tougaard"

# Fit result column names
FIT_MODEL_COL = "fit_model"
RESIDUALS_COL = "residuals"
ENVELOPE_COL = "envelope"

# Default parameter bounds (eV)
DEFAULT_SIGMA_MIN = 0.05
DEFAULT_SIGMA_MAX = 2.0
DEFAULT_FRACTION_MIN = 0.0
DEFAULT_FRACTION_MAX = 1.0

# Default fitting options
DEFAULT_FIT_METHOD = "leastsq"
DEFAULT_FIT_TOLERANCE = 1e-6

# Supported line shapes
SUPPORTED_LINE_SHAPES = [
    "voigt", "gaussian", "lorentzian",
    "gl_mix", "asymmetric"
]

# Supported constraint types
SUPPORTED_CONSTRAINTS = [
    "equality", "offset", "ratio"
]