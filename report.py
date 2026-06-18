import csv
import os


def save_report(elapsed, throughput, memory_mb):
    os.makedirs("reports", exist_ok=True)

    print("save_report called")

    file_path = "reports/results.csv"

    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "elapsed_time",
                "throughput",
                "memory_mb"
            ])

        writer.writerow([
            elapsed,
            throughput,
            memory_mb
        ])
    print("save_report called")
    print(f"Saved report to {file_path}")