# main.py

import sys
from csv_processor import CSVProcessor
from parquet_processor import ParquetProcessor

def main():
    # Ask the user for the input file path
    file_path = input("Enter the path to the time series file (CSV or Parquet): ").strip()

    # Detect file type and select the appropriate processor
    if file_path.endswith(".csv"):
        processor = CSVProcessor(file_path, split_threshold_mb=1)
    elif file_path.endswith(".parquet"):
        processor = ParquetProcessor(file_path)
    else:
        print("Unsupported file type. Please provide a .csv or .parquet file.")
        sys.exit(1)

    # Run the processing pipeline
    processor.process()

if __name__ == "__main__":
    main()
