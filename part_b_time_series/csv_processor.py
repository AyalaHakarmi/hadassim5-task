# csv_processor.py

import os
import pandas as pd
from base_processor import TimeSeriesProcessor

class CSVProcessor(TimeSeriesProcessor):
    """
    Processes a CSV file containing time series data with 'timestamp' and 'value' columns.
    If the file is large, it splits the data by day and computes hourly averages per day.
    Otherwise, it processes the whole file directly.
    """

    def __init__(self, file_path, output_dir="csv_output", **kwargs):
        super().__init__(file_path, **kwargs)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def load_data(self):
        """
        Reads the CSV file into a DataFrame and ensures timestamp column is parsed as datetime.
        """
        df = pd.read_csv(self.file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        self.df = df

    def split_by_day(self):
        """
        Splits the full DataFrame into multiple CSV files by date.
        """
        self.df['date'] = self.df['timestamp'].dt.date
        for date, group in self.df.groupby('date'):
            path = os.path.join(self.output_dir, f"day_{date}.csv")
            group.drop(columns='date').to_csv(path, index=False)

    def compute_hourly_average(self, input_file):
        """
        Computes hourly averages from a time series CSV file.
        Ensures timestamps and values are valid and numeric.
        """
        df = pd.read_csv(input_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna(subset=['timestamp', 'value'])

        df['hour'] = df['timestamp'].dt.floor('h')
        hourly = df.groupby('hour')['value'].mean().reset_index()
        hourly.rename(columns={'hour': 'timestamp'}, inplace=True)

        return hourly

    def process(self):
        """
        Main processing logic based on file size.
        Decides whether to split or process directly.
        """
        print(f"Processing CSV file: {self.file_path}")
        self.load_data()

        self.df = self.clean_data(self.df)

        if self.should_split():
            print("File is large – splitting by day and processing each separately...")
            self.split_by_day()
            hourly_results = []

            for filename in sorted(os.listdir(self.output_dir)):
                if filename.endswith(".csv"):
                    path = os.path.join(self.output_dir, filename)
                    hourly = self.compute_hourly_average(path)
                    hourly_results.append(hourly)

            final_df = pd.concat(hourly_results).sort_values('timestamp')
        else:
            print("File is small – computing hourly average directly...")
            final_df = self.compute_hourly_average(self.file_path)

        output_path = os.path.join(self.output_dir, "time_series_clean.csv")
        final_df.to_csv(output_path, index=False)
        print(f"Final result saved to {output_path}")
