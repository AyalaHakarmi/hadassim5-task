# main.py

import os
from collections import Counter
import heapq
from split_logs import split_log_file
from count_errors import count_errors_in_file
from tqdm import tqdm

# Configuration
INPUT_FILE = "logs.txt"
SPLIT_DIR = "splits"

def main():
    # Ask the user for N
    try:
        top_n = int(input("Enter the number of most frequent error codes to display (N): "))
        if top_n <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input. N must be a positive integer.")
        return

    print("Splitting the large log file...")
    split_log_file(INPUT_FILE, SPLIT_DIR, lines_per_file=100_000)

    print("Counting error codes in each part...")
    total_counter = Counter()
    for filename in tqdm(os.listdir(SPLIT_DIR)):
        path = os.path.join(SPLIT_DIR, filename)
        part_counter = count_errors_in_file(path)
        total_counter.update(part_counter)

    print(f"\nTop {top_n} most frequent error codes:")
    most_common = heapq.nlargest(top_n, total_counter.items(), key=lambda x: x[1])
    for code, count in most_common:
        print(f"{code}: {count}")

if __name__ == "__main__":
    main()
