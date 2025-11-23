"""Load data from CSV to pandas DataFrame."""
import pandas as pd
from typing import Optional

def load_csv_to_dataframe(csv_file_path: str) -> pd.DataFrame:
    """
    Load data from CSV file into pandas DataFrame.
    
    Args:
        csv_file_path: Path to the CSV file
        
    Returns:
        DataFrame with CSV data
    """
    df = pd.read_csv(csv_file_path)
    # Ensure all columns are string type for consistency
    df = df.astype('string')
    return df