# count_errors.py

from collections import Counter
import re

def extract_error_code(line):
    """Extract error code from a log line."""
    match = re.search(r'Error:\s*(\S+)', line)
    return match.group(1) if match else None

def count_errors_in_file(file_path):
    """Count error codes in a single log file."""
    counter = Counter()
    with open(file_path, 'r') as f:
        for line in f:
            code = extract_error_code(line)
            if code:
                counter[code] += 1
    return counter
