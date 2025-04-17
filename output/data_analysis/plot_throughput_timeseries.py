import os
import matplotlib.pyplot as plt
from collections import defaultdict

PROTOCOLS = ['bbr', 'cubic', 'vegas']
SCENARIOS = ['low_bw_high_rtt', 'high_bw_low_rtt']

def parse_log(filepath):
    timestamps = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.strip()
            try:
                if '+' in line:
                    parts = line.split('+')
                    timestamp = float(parts[0].strip()) + float(parts[1].strip())
                else:
                    timestamp = float(line)
                timestamps.append(timestamp / 1000.0)  # convert to seconds
            except:
                continue
    return timestamps

def compute_throughput(timestamps, interval=1.0):
    throughput = []
    if not timestamps:
        return throughput
    start_time = min(timestamps)
    end_time = max(timestamps)
    time = start_time
    while time < end_time:
        count = sum(1 for t in timestamps if time <= t < time + interval)
        mbps = (count * 1500 * 8) / (interval * 1e6)  # Convert to Mbps
        throughput.append((time, mbps))
        time += interval
    return throughput

def main():
    print("Generating throughput plots...\n")
    try:
        for scenario in SCENARIOS:
            print("--- Scenario: {} ---".format(scenario))
            plt.figure()
            for proto in PROTOCOLS:
                log_file = '../test_results/{}/{}/{}_mm_datalink_run1.log'.format(proto, scenario, proto)
                print("Parsing:", log_file)
                if not os.path.exists(log_file):
                    print("[Missing]", log_file)
                    continue
                timestamps = parse_log(log_file)
                if not timestamps:
                    print("No valid data in", log_file)
                    continue
                data = compute_throughput(timestamps)
                x = [t for t, _ in data]
                y = [v for _, v in data]
                plt.plot(x, y, label=proto.upper())

            plt.title("Time-Series Throughput ({})".format(scenario))
            plt.xlabel("Time (s)")
            plt.ylabel("Throughput (Mbps)")
            plt.grid(True)
            plt.legend()
            filename = "throughput_timeseries_{}.png".format(scenario)
            plt.savefig(filename)
            print("Saved:", filename)
            plt.close()
    except KeyboardInterrupt:
        print("\n[Interrupted] Plotting cancelled by user. Exiting cleanly.")

if __name__ == "__main__":
    main()

