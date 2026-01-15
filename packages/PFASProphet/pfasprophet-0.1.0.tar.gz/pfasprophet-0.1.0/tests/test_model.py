# -*- coding: utf-8 -*-
import pytest
import pandas as pd
from PFASProphet import PFASProphet 
import os
import shutil
import tempfile
from PFASProphet import commons as C

def test_model_loading():
    """Test that the model resource loads without error."""
    prophet = PFASProphet()
    model = prophet.load_model() 
    assert model is not None, "Model failed to load."

@pytest.mark.parametrize("mass, fragments, expected_length", [
    ([248.9461], [[63.9624]], 1),  # Single compound
    ([248.9461, 298.9427, 348.9396, 397.9525, 398.9357, 412.9667, 448.9334, 462.9632, 498.9302, 512.9601, 548.9270, 562.9565, 514.9001, 247.9622, 297.9590], [[],[63.9624, 77.9654, 118.9921, 218.9820, 297.9606],[79.9566, 98.9557, 348.9388],[77.9653, 397.9525],[79.9570, 98.9556, 118.9925, 168.9888, 229.9479, 398.9356],[79.9582, 98.9560, 168.9904],[79.9569, 98.9555, 118.9921, 168.9884, 229.9454],[118.9919, 168.9893, 218.9853, 268.9810, 418.9727],[79.9578, 98.9561, 118.9939, 168.9939, 218.9855, 418.9730, 462.9654],[118.9924, 168.9898, 218.9857, 268.9826, 318.9799, 468.9681],[79.9574, 98.9565, 129.9532, 179.9506, 229.9474, 279.9445, 329.9411, 429.9436],[118.9922, 168.9891, 218.9856, 268.9825, 318.9825, 418.9783, 518.9665],[79.9571, 98.9554, 134.9867, 184.9829, 168.9827, 279.9459],[63.9623, 77.9654, 247.9612],[79.9563, 97.9592, 115.0744, 221.1902, 265.1596, 283.1917]], 15),  # Multiple Compounds (fixed expected_length)
])
def test_valid_input_full(mass,fragments, expected_length):
    """Test prediction with valid mass and fragment inputs, checking output length."""
    prophet = PFASProphet()
    result = prophet.predict(mass=mass, fragments=fragments)
    assert isinstance(result, list), f"Expected DataFrame, got {type(result)}"
    assert len(result) == len(mass), f"Output rows must match input mass count"
    assert len(result) == expected_length, f"Expected {expected_length} results, got {len(result)}"

@pytest.fixture
def backup_csv():
    """Fixture to back up and restore the test CSV file."""
    csv_path = C.EXAMPLE_CSV
    # Create a temporary backup
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copy(csv_path, tmp_file.name)
        backup_path = tmp_file.name
    yield 
    
    shutil.copy(backup_path, csv_path)
    os.unlink(backup_path)  # Clean up the backup

@pytest.mark.parametrize("mass_col, fragments_col", [
    ("mass", "fragments"),  # Original columns
    ("UK_COW_MASS", "UK_COW_FRAGS"),  # New columns to test
])
def test_predict_with_csv_modification(backup_csv, mass_col, fragments_col):
    """Test CSV prediction with different column names, ensuring file modification and restoration."""
    prophet = PFASProphet()
    # This will overwrite the original CSV (since in_file=True)
    result = prophet.predict(file_path=C.EXAMPLE_CSV, mass_col=mass_col, fragments_col=fragments_col, in_file=True)
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) > 0, "No predictions returned"

def test_predict_invalid_columns():
    """Test that predict raises ValueError for missing columns in CSV."""
    prophet = PFASProphet()
    # Create a temp CSV with wrong column names
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        tmp.write("wrong_mass,wrong_fragments\n100.0,[1.0]\n")
        tmp_path = tmp.name
    
    try:
        with pytest.raises(ValueError, match="Columns 'mass' or 'fragments' not found"):
            prophet.predict(file_path=tmp_path)
    finally:
        os.unlink(tmp_path)

def test_predict_no_valid_mass():
    """Test that predict raises ValueError when mass column has no valid data."""
    prophet = PFASProphet()
    # Create a temp CSV with empty mass column
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        tmp.write("mass,fragments\n,\n,\n")
        tmp_path = tmp.name
    
    try:
        with pytest.raises(ValueError, match="No valid mass values found in column 'mass'"):
            prophet.predict(file_path=tmp_path)
    finally:
        os.unlink(tmp_path)

def test_predict_no_input_provided():
    """Test that predict raises ValueError when neither file_path nor mass/fragments are provided."""
    prophet = PFASProphet()
    with pytest.raises(ValueError, match="Provide either direct lists or a file_path"):
        prophet.predict()

def test_predict_length_mismatch():
    """Test that predict raises ValueError for mismatched mass/fragments lengths."""
    prophet = PFASProphet()
    with pytest.raises(ValueError, match="Length mismatch"):
        prophet.predict(mass=[100.0, 200.0], fragments=[[1.0]]) 
