"""
PFASProphet predictor module.

Contains the main PFASProphet class for PFAS score predictions.
"""
import numpy as np
import pandas as pd
from joblib import dump, load
import json
from importlib import resources
from . import commons as C
from pydantic import validate_call, Field, ConfigDict
from typing import List, Union, Optional
import ast

class PFASProphet:
    """
    Main class for PFAS prediction using machine learning.

    This class loads a pre-trained model and provides methods to predict PFAS scores
    from mass spectrometry data (masses and fragments). It supports both direct lists
    and CSV files, with options for ionisation adjustments.
    """
    def __init__(self):
        """Initialize the PFASProphet instance. No parameters required."""
        pass

    def load_model(self):
        """
        Load the pre-trained machine learning model.

        Uses importlib.resources to access the model file bundled with the package.
        Sets model verbosity to -1 for silent operation.

        Returns:
            The loaded model object.
        """
        model_path = resources.files("PFASProphet").joinpath(C.MODEL_NAME)
    
        with resources.as_file(model_path) as path:
            self.model = load(path)

        self.model.set_params(verbosity=-1)

        return self.model

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def predict(
        self, 
        mass: Optional[List[float]] = Field(None, description="List of precursor masses"),
        fragments: Optional[List[List[float]]] = Field(None, description="List of fragment lists"),
        file_path: Optional[str] = Field(None, description="Path to CSV file with mass and fragments columns"),
        mass_col: str = Field("mass", description="Column name for precursor mass"),
        fragments_col: str = Field("fragments", description="Column name for MS2 fragments"),
        in_file: bool = Field(False, description="If True, appened the input file with results else new file is created"),
        is_ionised: bool = Field(True, description="If True, mass is ionised (default); if False, mass is neutral and proton mass is sustracted to obtain ionised mass")
    ) -> list:
        """
        Predict PFAS scores from masses and fragments or a CSV file.

        Args:
            mass (list[float], optional): List of precursor masses.
            fragments (list[list[float]], optional): List of fragment lists.
            file_path (str, optional): Path to CSV file.
            mass_col (str): Mass column name (default: 'mass').
            fragments_col (str): Fragments column name (default: 'fragments').
            in_file (bool): Append to input file if True.
            is_ionised (bool): If True, mass is ionised; if False, subtract proton mass.

        Returns:
            list: List of prediction scores.

        Raises:
            ValueError: If inputs are invalid.
        """

        self.load_model()

        def parse_fragments(value):
            """
            Parse fragment strings from CSV into lists.

            Supports both '[1.1,2.2]' (list literal) and '1.1,2.2' (comma-separated).
            Returns empty list for NaN/invalid values.

            Args:
                value: The value from the CSV column.

            Returns:
                list[float]: Parsed fragment masses.

            Raises:
                ValueError: For invalid data types.
            """
            if isinstance(value, str):
                if value.strip().startswith('['):
                    return ast.literal_eval(value)
                else:
                    return [float(x.strip()) for x in value.split(',') if x.strip()]
            elif pd.isna(value):  # Handle NaN or None
                return []
            else:
                raise ValueError("Invalid fragment data type")  # Fallback for other invalid types

        # ... (rest of predict method)

        # If a CSV is provided, we ignore the 'mass' and 'fragments' list arguments
        if file_path:
            df = pd.read_csv(file_path)
            
            # 1. Extract columns using the provided names
            if mass_col not in df.columns or fragments_col not in df.columns:
                available = ", ".join(df.columns)
                raise ValueError(f"Columns '{mass_col}' or '{fragments_col}' not found. Available: {available}")

            # Filter out rows with NaN/empty in mass_col only (allow fragments to be empty)
            df = df.dropna(subset=[mass_col])
            
            # Raise error if no valid mass values remain
            if df.empty:
                raise ValueError(f"No valid mass values found in column '{mass_col}'. Ensure the column contains numeric data.")

            mass_list = df[mass_col].tolist()
            
            # Adjust for ionisation if needed (negative ESI: subtract proton for neutral -> ionised)
            if not is_ionised:
                mass_list = [m - C.PROTON_MASS for m in mass_list]
            # Parse fragments (NaN/empty becomes [])
            fragments_list = [parse_fragments(f) for f in df[fragments_col]]
            
            # return predictions
            predictions = self._predict_compound_list(mass_list, fragments_list)

            # Add prediction to the dataframe
            df["PP_Score"] = predictions
            # Generate new filename: e.g., "data.csv" -> "data_PP.csv"

            save_path =  file_path if in_file else file_path.replace(".csv", "_PP.csv")
            df.to_csv(save_path, index=False)
            print(f"Results saved to: {save_path}")
                

            return predictions
        elif mass is not None and fragments is not None:
            if not is_ionised:
                mass = [m - C.PROTON_MASS for m in mass] if isinstance(mass, list) else mass - C.PROTON_MASS
            return self._predict_compound_list(mass, fragments)

        raise ValueError("Provide either direct lists or a file_path.")
    

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def _predict_compound_list(
        
         self, 
        mass: List[float] = Field(..., min_length=1, description="List of precursor masses"),
        fragments: List[List[float]] = Field(..., min_length=1, description="List of fragment lists")
    ) -> list:
        """
        Internal method to predict scores for a list of compounds.

        Handles input validation, type conversion, and calls processing methods.

        Args:
            mass (list[float]): List of masses.
            fragments (list[list[float]]): List of fragment lists.

        Returns:
            list: Prediction scores.

        Raises:
            ValueError: For invalid inputs.
        """
        
        # Additional logic check: Ensure lengths match
        if len(mass) != len(fragments):
            raise ValueError(f"Length mismatch: {len(mass)} masses vs {len(fragments)} fragment lists.")
        
        self.df_entries = False
        
        if isinstance(mass,str):
            print("mass is of type string, converting entries :")
            try:
                mass = json.loads(mass)
            except Exception as error:
                print("An exception occurred:", error)
                print("Process failed as fragments is a string and cannot be converted to list")
                return None
        # checking fragment input is a list of floats
        if isinstance(fragments,str):
            print("Fragments is of type string, converting to list")
            try:
                fragments = json.loads(fragments)
            except Exception as error:
                print("An exception occurred:", error)
                print("Process failed as fragments is a string and cannot be converted to list")
                return None
        try:
            fragments = [list(map(float, fragments_row)) for fragments_row in fragments]
        except Exception as error:
            print("An exception occurred:", error)
            print("process failed as fragments is a list containing strings not convertable to floats")
            return None
        
        if isinstance(mass,list):
            if len(mass) != len(fragments):
                print("mass list and fragment list not of the same length")
                return None
        
        if isinstance(mass,float):
            mass = [mass]
            fragments = [fragments]
            
        self.mass = mass
        self.fragments = fragments
        
        self._handle_mass()
        
        self._create_entry_frags()

        return self._get_prediction()
    
    def _handle_mass(self):
        """
        Compute Kendrick Mass Defects (KMDs) for various compound formulas.

        KMDs are used as features for the ML model. Calculates KMD for CF2, CN, CO, etc.
        """
        def kmd(meas_mass, compound):
            """
            Calculate Kendrick Mass Defect.

            Args:
                meas_mass (float): Measured mass.
                compound (float): Compound mass.

            Returns:
                float: KMD value.
            """
            t = meas_mass * (round(compound) / compound)
            kmd = round(t) - t
            return kmd
        self._get_table()["KMD_CF2"]   = [kmd(ms,C.CF2_MASS) for ms in self.mass]
        self._get_table()["KMD_CN"]    = [kmd(ms,C.CN_MASS) for ms in self.mass]
        self._get_table()["KMD_CO"]    = [kmd(ms,C.CO_MASS) for ms in self.mass]
        self._get_table()["KMD_CH2"]   = [kmd(ms,C.CH2_MASS) for ms in self.mass]
        self._get_table()["KMD_CF2O"]  = [kmd(ms,C.CF2O_MASS) for ms in self.mass]
        self._get_table()["KMD_C2F4O"] = [kmd(ms,C.C2F4O_MASS) for ms in self.mass]
   
    def _get_feature_names(self):
        """
        Retrieve feature names from the loaded model.

        Returns:
            list: Feature names.
        """
        self.features = self.model.feature_names_in_
        return self.features
    
    def _get_losses(self):
        """
        Compute neutral losses for each compound.

        For each fragment, calculate precursor mass - fragment mass, plus the fragment itself.

        Returns:
            list: List of loss/fragment lists.
        """
        self.losses = self.fragments.copy()
        for i in range(len(self.fragments)):
            MM = self.mass[i]
            self.losses[i] = [MM - x for x in self.fragments[i]]+self.fragments[i]
            self.losses
        
        return self.losses
        
    def _set_fragments_bins(self):
        """
        Bin fragment masses into discrete values for feature encoding.

        Uses BIN_WIDTH and DECIMAL_PLACES_FOR_FRAGMENTS for rounding.

        Returns:
            list: Binned fragment lists.
        """
        self.fragments_binned = [list(np.around(np.around(np.array(fragments_row)/C.BIN_WIDTH)*C.BIN_WIDTH,decimals=C.DECIMAL_PLACES_FOR_FRAGMENTS)) for fragments_row in self._get_losses()]
        return self.fragments_binned
                
    def _get_table(self):
        """
        Get or create the feature table DataFrame.

        Initializes a DataFrame with feature columns and rows for each compound.

        Returns:
            pd.DataFrame: Feature table.
        """
        if self.df_entries is False:
            self.df_entries = pd.DataFrame(0, index=np.arange(len(self.mass)), columns=self._get_feature_names())
        return self.df_entries

    def _create_entry_frags(self):
        """
        Encode binned fragments into the feature table.

        Sets 1 in the table for each matching fragment bin.
        """
        for i in list(self._get_table().index):
            for (frg) in self._set_fragments_bins()[i]:
                if str(frg) in self.features:
                    self._get_table().loc[i,str(frg)] = 1
                    
    def _get_prediction(self):
        """
        Run the model prediction.

        Returns:
            list[float]: Prediction probabilities (first class scores).
        """
        res = self.model.predict_proba(self._get_table())
        return [float(item[0]) for item in res]

                    
