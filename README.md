# Hadassim 5 – Final Assignment

This repository contains solutions for the final assignment from the Hadassim course.
Each part of the assignment is organized into its own directory.

## ✅ Part A: Log Analysis
**Files:**
- `logs.txt` — the raw input data.
- `split_logs.py` — separates logs into files by hour.
- `count_errors.py` — counts error types across the split logs.

### What We Did:
- Wrote a Python program that reads a large log file and splits it by hour into smaller files.
- Implemented efficient log parsing and writing using dictionaries and file streams.
- Counted the most common error messages (by error type) using a heap structure.

### Time Complexity:
To find the top N most frequent error types:
- We used a min-heap of size N to track the top errors.
- The total time complexity is: **O(U log N)**, where U is the number of unique error types.
- This is better than sorting all errors (which would be O(U log U)).

---

## ✅ Part B: Time Series Cleaning and Aggregation
**Files:**
- `base_processor.py` — base class for CSV and Parquet processors.
- `csv_processor.py` — processor for `.csv` time series files.
- `parquet_processor.py` — processor for `.parquet` time series files.
- `main.py` — chooses processor based on user input.
- `requirements.txt` — dependencies.

### What We Did:
- Built a clean object-oriented architecture with inheritance.
- Automatically detects file format (CSV or Parquet).
- Based on the file size, chooses whether to split the time series by day or not.
- For each part (daily or whole), computes hourly average.
- Removes duplicates, missing values, negative values, and out-of-range values.

### Design Note:
We used inheritance to handle CSV and Parquet differently while sharing common logic.
This separation makes the code easier to test and extend.

### Why Not Use a Stream?
While streaming is memory-efficient, we needed access to full-day data in order to:
- Detect duplicates
- Clean based on global criteria (e.g. value range)
- Group by hour accurately

Therefore, we opted to read the entire file (or day-chunk) into memory before processing.
