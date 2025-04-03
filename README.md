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

### Why Not Use Stream Processing?
While stream processing is often more memory-efficient (as it processes the file line-by-line), it is **not suitable in this case** for the following reasons:

1. **Duplicate detection** requires having access to all timestamps seen so far.
   This would require either:
   - Keeping all seen values in memory (which is similar to loading the file), or
   - Writing intermediate data structures, which adds complexity and I/O cost.

2. **Hourly aggregation** requires grouping by hour, which cannot be reliably done if we only hold one line at a time — since we may need to merge or average data across multiple lines within the same hour.

3. **Data validation** (checking for missing or out-of-range values) may require comparing data across rows or detecting trends, which stream processing doesn’t allow efficiently.

**Conclusion:**
Stream processing sacrifices structure and flexibility for memory efficiency. In this case, we prioritize correctness and simplicity over memory optimization, especially since the daily chunks are manageable in memory.

### Real-Time Stream Processing (Question 3, Part B)
If the data arrives in a live stream rather than from a file, we must update the hourly averages incrementally, without having all the data in advance.

To handle this, we can maintain a running aggregation structure for each hour:

- Use a dictionary `hour → (sum, count)` to store the total value and number of values for each hour seen so far.
- For each incoming data point:
  1. Convert the timestamp to the relevant hour (e.g., floor to the hour).
  2. Update the `sum` and `count` for that hour.
  3. The average is computed as `sum / count`.

This approach allows constant-time updates and supports real-time streaming without needing to load historical data into memory.

**Note:** At the end of the stream (or periodically), we can output the computed averages per hour.
