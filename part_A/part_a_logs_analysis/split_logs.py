# split_logs.py

import os

def split_log_file(input_path, output_dir, lines_per_file=100_000):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, 'r') as infile:
        file_count = 0
        current_lines = []

        for i, line in enumerate(infile):
            current_lines.append(line)
            if (i + 1) % lines_per_file == 0:
                output_file = os.path.join(output_dir, f'part_{file_count}.log')
                with open(output_file, 'w') as f:
                    f.writelines(current_lines)
                current_lines = []
                file_count += 1

        if current_lines:
            output_file = os.path.join(output_dir, f'part_{file_count}.log')
            with open(output_file, 'w') as f:
                f.writelines(current_lines)
