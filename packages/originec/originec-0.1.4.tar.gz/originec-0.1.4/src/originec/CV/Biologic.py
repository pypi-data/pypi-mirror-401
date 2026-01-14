# %%
import pandas as pd
import numpy as np
from pathlib import Path


class CVParser:
    def __init__(self):
        """
        Initialize CVParser by reading CV data from clipboard.
        Data should be copied from EC-Lab using Alt+D.
        Expected format: First line contains file path, second line contains headers (Ewe/V vs. SCE, <I>/mA)
        """
        # Read first line to get the file name
        first_line = pd.read_clipboard(nrows=1, header=None, sep="\t")
        self.filename = Path(first_line.at[0, 0]).stem if not first_line.empty else "BiologicCV"
        
        # Read header line to get current unit
        header_line = pd.read_clipboard(nrows=1, header=None, sep="\t", skiprows=1)
        current_header = header_line.at[0, 1] if len(header_line.columns) > 1 else "<I>/mA"
        
        # Extract unit from header (e.g., "<I>/mA" -> "mA", "<I>/A" -> "A")
        current_unit = self._extract_unit(current_header)
        
        # Read the actual data (skip first line which is the file path, and header line)
        self.data = pd.read_clipboard(sep="\t", skiprows=2, header=None)
        
        # Rename columns to standardized names
        self.data.columns = ["x", "y"]
        
        # Convert to numeric, handling scientific notation
        self.data["x"] = pd.to_numeric(self.data["x"], errors='coerce')
        self.data["y"] = pd.to_numeric(self.data["y"], errors='coerce')
        
        # Convert current to mA based on detected unit
        conversion_factor = self._get_conversion_factor(current_unit)
        self.data["y"] = self.data["y"] * conversion_factor
        
        # Remove any NaN values
        self.data = self.data.dropna().reset_index(drop=True)
    
    def _extract_unit(self, header: str) -> str:
        """
        Extract current unit from header string.
        
        Parameters:
        -----------
        header : str
            Header string (e.g., "<I>/mA", "<I>/A", "I/μA")
        
        Returns:
        --------
        str
            Unit string ("mA", "A", "μA", etc.)
        """
        # Split by '/' and take the last part
        if '/' in header:
            unit = header.split('/')[-1].strip()
        else:
            unit = "mA"  # Default to mA
        return unit
    
    def _get_conversion_factor(self, unit: str) -> float:
        """
        Get conversion factor to convert from given unit to mA.
        
        Parameters:
        -----------
        unit : str
            Current unit ("mA", "A", "μA", etc.)
        
        Returns:
        --------
        float
            Conversion factor to multiply with the data
        """
        unit_lower = unit.lower()
        
        if unit_lower == "ma":
            return 1.0  # Already in mA
        elif unit_lower == "a":
            return 1000.0  # A to mA
        elif unit_lower in ["μa", "ua", "µa"]:
            return 0.001  # μA to mA
        elif unit_lower in ["na"]:
            return 0.000001  # nA to mA
        else:
            # Default: assume mA
            return 1.0

    def clean_data(self, split_val=None):
        """
        Clean and split CV data into cycles.
        Detects the sweep direction changes and splits the data accordingly.
        
        Parameters:
        -----------
        split_val : float, optional
            Voltage value to use for splitting cycles. If None, uses the first voltage value.
        
        Returns:
        --------
        pd.DataFrame
            DataFrame with columns named as '1x', '1y', '2x', '2y', etc. for each cycle segment
        """
        xy_df = self.data.copy()
        
        if split_val is None:
            # Use first value as the split point
            first_val = xy_df.iloc[0, 0]
        else:
            first_val = split_val
        
        # Find indices where voltage crosses the first_val
        crosses_first_val = np.where(np.diff(np.sign(xy_df["x"] - first_val)))[0]
        
        # Filter crosses to only include significant ones (minimum distance between crossings)
        # This helps avoid detecting noise as cycle boundaries
        min_distance = 50  # Minimum number of points between cycle boundaries
        if len(crosses_first_val) > 1:
            valid_crosses = [crosses_first_val[0]]
            for cross in crosses_first_val[1:]:
                if cross - valid_crosses[-1] > min_distance:
                    valid_crosses.append(cross)
            crosses_first_val = np.array(valid_crosses)
        
        # If less than 2 crossing points found, return the whole dataset as one cycle
        if len(crosses_first_val) < 2:
            clean_df = pd.DataFrame()
            clean_df["1x"] = xy_df["x"].reset_index(drop=True)
            clean_df["1y"] = xy_df["y"].reset_index(drop=True)
            return clean_df
        
        # Split dataframe at crossing points
        clean_df = pd.DataFrame()
        prev_index = 0
        cycle_num = 1
        
        for i, index in enumerate(crosses_first_val, start=1):
            if i % 2 == 0:  # Every even crossing marks the end of a full cycle
                df_temp = xy_df.iloc[prev_index:index + 1]
                clean_df[f"{cycle_num}x"] = df_temp["x"].reset_index(drop=True)
                clean_df[f"{cycle_num}y"] = df_temp["y"].reset_index(drop=True)
                cycle_num += 1
                prev_index = index + 1
            elif i == len(crosses_first_val):
                # Last odd crossing, include remaining data
                df_temp = xy_df.iloc[prev_index:]
                clean_df[f"{cycle_num}x"] = df_temp["x"].reset_index(drop=True)
                clean_df[f"{cycle_num}y"] = df_temp["y"].reset_index(drop=True)
        
        return clean_df


def main():
    # Initialize the parser (reads from clipboard)
    parser = CVParser()
    
    # Clean the data
    clean_data = parser.clean_data()
    
    # Print the cleaned data
    print(clean_data)
    print(f"\nNumber of cycles: {len(clean_data.columns) // 2}")


if __name__ == "__main__":
    main()
