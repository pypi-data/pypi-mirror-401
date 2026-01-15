# -*- coding: utf-8 -*-
# Example CSV file path for testing
EXAMPLE_CSV = "tests/example_compounds_to_process.csv"

# Name of the pre-trained model file
MODEL_NAME = "model.model"

# Bin width for fragment mass binning (in Da)
BIN_WIDTH=0.09

# Molecular masses for Kendrick Mass Defect calculations (in Da)
CF2_MASS = 49.996806    # CF2 group
CN_MASS = 26.003073     # CN group
CO_MASS = 27.994915     # CO group
CH2_MASS = 14.015650    # CH2 group
CF2O_MASS = 65.991721   # CF2O group
C2F4O_MASS = 115.988527 # C2F4O group

# Proton mass for ionisation adjustments in negative ESI-MS (in Da)
PROTON_MASS = 1.007276

# Decimal places for rounding fragment bins
DECIMAL_PLACES_FOR_FRAGMENTS = 4

