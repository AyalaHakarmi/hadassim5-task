# Hadassim 5 – Final Assignment

This repository contains solutions for the final assignment from the Hadassim course. Each part of the assignment is organized into its own directory:

```
HADASIM/
├── part_A/
│   ├── part_a_logs_analysis/      # Code for Part A – Log splitting and error counting
│   └── part_b_time_series/        # Code for Part B – Time series cleaning and aggregation
├── part_B/                        # (Not yet implemented)
├── part_C/                        # Theoretical answers
└── README.md                      # This file
```

---

## ✅ Part A – Log Analysis (`part_A/part_a_logs_analysis`)
**Files:**
- `logs.txt` — the raw input data
- `split_logs.py` — separates logs into files by hour
- `count_errors.py` — counts error types across the split logs

### What We Did:
- Wrote a Python program that reads a large log file and splits it by hour into smaller files.
- Implemented efficient log parsing and writing using dictionaries and file streams.
- Counted the most common error messages (by error type) using a heap structure.

### Time Complexity:
To find the top N most frequent error types:
- We used a min-heap of size N to track the top errors.
- The total time complexity is: **O(U log N)**, where U is the number of unique error types.
- This is better than sorting all errors (which would be O(U log U)).

### Space Complexity:
- We maintain a counter (dictionary) with U keys (unique error types): **O(U)**.
- We use a heap of size N to store the top N frequent errors: **O(N)**.
- Therefore, the total space complexity is: **O(U + N)**.

---

## ✅ Part B – Time Series Processing (`part_A/part_b_time_series`)
**Files:**
- `base_processor.py` — base class for CSV and Parquet processors
- `csv_processor.py` — processor for `.csv` time series files
- `parquet_processor.py` — processor for `.parquet` time series files
- `main.py` — chooses processor based on user input
- `requirements.txt` — dependencies

### What We Did:
- Built a clean object-oriented architecture with inheritance.
- Automatically detects file format (CSV or Parquet).
- Based on the file size, chooses whether to split the time series by day or not.
- For each part (daily or whole), computes hourly average.
- Removes duplicates, missing values, negative values, and out-of-range values.

### Design Note:
We used inheritance to handle CSV and Parquet differently while sharing common logic. This separation makes the code easier to test and extend.

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

---

## 🕒 Part C – Theoretical Questions (`part_C/`)
Answers to the theoretical questions are written in `answers.md`, organized by chapter and question number.

---
