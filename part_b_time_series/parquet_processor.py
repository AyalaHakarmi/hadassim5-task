# parquet_processor.py

import os
import pandas as pd
from base_processor import TimeSeriesProcessor

class ParquetProcessor(TimeSeriesProcessor):
    """
    Processes a Parquet file containing time series data.
    Assumes it includes 'timestamp' and 'value' columns.
    """

    def __init__(self, file_path, output_dir="parquet_output", **kwargs):
        super().__init__(file_path, **kwargs)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def load_data(self):
        """Reads the Parquet file and parses timestamps."""
        df = pd.read_parquet(self.file_path)

        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')

        self.df = df

    def compute_hourly_average(self, df):
        df['hour'] = df['timestamp'].dt.floor('h')
        hourly = df.groupby('hour')['value'].mean().reset_index()
        hourly.rename(columns={'hour': 'timestamp'}, inplace=True)
        return hourly

    def process(self):
        print(f"Processing Parquet file: {self.file_path}")
        self.load_data()
        self.df = self.clean_data(self.df)

        if self.should_split():
            print("Note: Parquet file is large, but no splitting will be performed.")

        final_df = self.compute_hourly_average(self.df)

        output_path = os.path.join(self.output_dir, "time_series_clean.csv")
        final_df.to_csv(output_path, index=False)
        print(f"Final result saved to {output_path}")
