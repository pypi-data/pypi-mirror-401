"""
Data loading and import utilities.

Handles loading XPS data from ZIP archives, CSV files, and other formats.
"""
from typing import Optional, List
import pandas as pd
import zipfile


class DataLoader:
    """
    Loads XPS data from various sources.
    """
    
    @staticmethod
    def zip_to_df(zip_path: str, 
                  target_file: Optional[str] = None,
                  sep: str = "\t",
                  encoding: str = "utf-8",
                  energy_col: str = "Energy (BE/eV)",
                  intensity_col: str = "Intensity") -> Optional[pd.DataFrame]:
        """
        Load XPS data from ZIP archive (original implementation).
        
        Extracts a CSV file from a ZIP archive and converts it to a DataFrame
        with standardized column names.
        
        Parameters
        ----------
        zip_path : str
            Path to .zip file
        target_file : str, optional
            Specific file within archive (e.g., 'spectra/Fe2p.csv').
            If None, lists all files and returns None.
        sep : str
            CSV delimiter (default: tab)
        encoding : str
            Text encoding (default: utf-8)
        energy_col : str
            Name for energy column in output
        intensity_col : str
            Name for intensity column in output
            
        Returns
        -------
        pd.DataFrame or None
            Loaded data with standardized column names (Energy, Intensity),
            or None if just listing files
            
        Raises
        ------
        ValueError
            If target_file is specified but not found in archive
            
        Example
        -------
        >>> # List files in archive
        >>> df = DataLoader.zip_to_df('data.zip')
        
        >>> # Load specific file
        >>> df = DataLoader.zip_to_df('data.zip', 'spectra/Fe2p.csv')
        """
        with zipfile.ZipFile(zip_path, "r") as z:
            file_list = z.namelist()
            if not target_file:
                print("Files in the zip archive:")
                for file in file_list:
                    print(file)
                return None
            if target_file not in file_list:
                raise ValueError(f"File '{target_file}' not found in the zip archive.")
            with z.open(target_file) as csv_file:
                df = pd.read_csv(csv_file, sep=sep, encoding=encoding)
                df.columns = [energy_col, intensity_col]
                return df
    
    @staticmethod
    def load_from_zip(zip_path: str,
                     target_file: Optional[str] = None,
                     sep: str = "\t",
                     encoding: str = "utf-8") -> Optional[pd.DataFrame]:
        """
        Load XPS data from ZIP archive (convenience wrapper).
        
        Wrapper around zip_to_df with sensible defaults.
        
        Parameters
        ----------
        zip_path : str
            Path to .zip file
        target_file : str, optional
            Specific file within archive
        sep : str
            CSV delimiter
        encoding : str
            Text encoding
            
        Returns
        -------
        pd.DataFrame or None
            Loaded data, or None if just listing files
        """
        return DataLoader.zip_to_df(zip_path, target_file, sep, encoding)
    
    @staticmethod
    def load_from_csv(csv_path: str,
                     energy_col: str = "Energy (BE/eV)",
                     intensity_col: str = "Intensity",
                     sep: str = "\t",
                     **kwargs) -> pd.DataFrame:
        """
        Load XPS data from CSV file.
        
        Parameters
        ----------
        csv_path : str
            Path to CSV file
        energy_col : str
            Expected name of energy column in file
        intensity_col : str
            Expected name of intensity column in file
        sep : str
            CSV delimiter
        **kwargs
            Additional arguments for pd.read_csv
            
        Returns
        -------
        pd.DataFrame
            Loaded data with standardized column names
            
        Raises
        ------
        FileNotFoundError
            If CSV file doesn't exist
        ValueError
            If required columns are missing
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        df = pd.read_csv(csv_path, sep=sep, **kwargs)
        
        # Check if columns exist
        if energy_col not in df.columns or intensity_col not in df.columns:
            raise ValueError(f"Required columns '{energy_col}' and/or '{intensity_col}' not found in CSV")
        
        return df
    
    @staticmethod
    def list_files_in_zip(zip_path: str) -> List[str]:
        """
        List all files in a ZIP archive.
        
        Parameters
        ----------
        zip_path : str
            Path to .zip file
            
        Returns
        -------
        List[str]
            File names in archive (with paths)
            
        Example
        -------
        >>> files = DataLoader.list_files_in_zip('data.zip')
        >>> print(files)
        ['metadata.xml', 'spectra/Fe2p.csv', 'spectra/O1s.csv']
        """
        with zipfile.ZipFile(zip_path, "r") as z:
            return z.namelist()
    
    @staticmethod
    def find_survey_spectrum(zip_path: str) -> Optional[str]:
        """
        Find survey spectrum file in ZIP archive.
        
        Searches for files with common survey naming patterns
        ('survey', 'Survey', 'SURVEY', 'full_scan', etc.).
        
        Parameters
        ----------
        zip_path : str
            Path to .zip file
            
        Returns
        -------
        str or None
            File path of survey spectrum in archive, or None if not found
        """
        files = DataLoader.list_files_in_zip(zip_path)
        survey_keywords = ['survey', 'Survey', 'SURVEY', 'full_scan', 'Full_Scan', 'fullscan']
        
        for keyword in survey_keywords:
            for file in files:
                if keyword in file and file.endswith('.csv'):
                    return file
        
        return None