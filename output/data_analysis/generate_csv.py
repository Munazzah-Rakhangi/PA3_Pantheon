import os
import json
import csv

# Schemes and scenarios
schemes = ["bbr", "cubic", "vegas"]
scenarios = ["low_bw_high_rtt", "high_bw_low_rtt"]

# Output file path (relative to this script's location)
output_file = "log_data.csv"

with open(output_file, mode="w") as csv_file:
    fieldnames = ["Scheme", "Scenario", "Throughput (Mbps)", "Delay (ms)", "Loss Rate"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for scheme in schemes:
        for scenario in scenarios:
            # Construct path using format (Python 2 compatible)
            perf_path = "../test_results/{}/{}/pantheon_perf.json".format(scheme, scenario)

            try:
                with open(perf_path, "r") as f:
                    data = json.load(f)
                    metrics = data[scheme]["1"]["all"]

                    writer.writerow({
                        "Scheme": scheme,
                        "Scenario": scenario,
                        "Throughput (Mbps)": round(metrics.get("tput", 0), 3),
                        "Delay (ms)": round(metrics.get("delay", 0), 3),
                        "Loss Rate": round(metrics.get("loss", 0), 5)
                    })

            except IOError:
                print("[Warning] Missing file: {}".format(perf_path))
            except Exception as e:
                print("[Error] Failed to read {}: {}".format(perf_path, str(e)))

print("\nlog_data.csv has been created.")

