from abc import ABC, abstractmethod
import os
import pandas as pd

class TimeSeriesProcessor(ABC):
    """
    Abstract base class for time series processing.
    Handles file size check, data validation, and defines interface for concrete processors.
    """

    def __init__(self, file_path, max_value=1_000_000, split_threshold_mb=100):
        self.file_path = file_path
        self.max_value = max_value
        self.split_threshold_mb = split_threshold_mb
        self.df = None

    def should_split(self):
        size_mb = os.path.getsize(self.file_path) / (1024 * 1024)
        return size_mb > self.split_threshold_mb

    def clean_data(self, df):
        """
        Cleans the time series DataFrame by applying several data validation checks:

        Standard checks (as defined in the assignment):
        - Missing values in 'timestamp' or 'value'
        - Duplicate timestamps
        - Negative values

        Additional check (our own enhancement):
        - Out-of-range values: filters values above a configurable max_value

        Parameters:
            df (pd.DataFrame): Raw input DataFrame with 'timestamp' and 'value' columns

        Returns:
            pd.DataFrame: Cleaned DataFrame with invalid rows removed
        """

        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')

        # Validation checks
        issues = {
            'missing_values': df.isnull().any(axis=1).sum(),
            'duplicate_timestamps': df.duplicated(subset='timestamp').sum(),
            'negative_values': (df['value'] < 0).sum(),
            'out_of_range': (df['value'] > self.max_value).sum()  # Additional check
        }

        # Drop invalid rows
        df = df.dropna(subset=['timestamp', 'value'])
        df = df.drop_duplicates(subset='timestamp')
        df = df[df['value'] >= 0]
        df = df[df['value'] <= self.max_value]

        # Summary of issues
        print("Validation Summary:")
        for k, v in issues.items():
            print(f"- {k.replace('_', ' ').capitalize()}: {v}")
        print(f"Cleaned rows: {len(df)}")

        return df

    @abstractmethod
    def process(self):
        pass