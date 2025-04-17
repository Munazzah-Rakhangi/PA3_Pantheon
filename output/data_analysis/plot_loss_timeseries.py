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
                timestamps.append(timestamp / 1000.0)
            except:
                continue
    return timestamps

def count_per_interval(timestamps, interval=1.0):
    counter = defaultdict(int)
    for t in timestamps:
        bucket = int(t // interval)
        counter[bucket] += 1
    return counter

def main():
    print("Generating loss time-series plots...\n")
    try:
        for scenario in SCENARIOS:
            print("--- Scenario: {} ---".format(scenario))
            plt.figure()

            for proto in PROTOCOLS:
                data_log = '../test_results/{}/{}/{}_mm_datalink_run1.log'.format(proto, scenario, proto)
                ack_log = '../test_results/{}/{}/{}_mm_acklink_run1.log'.format(proto, scenario, proto)

                if not os.path.exists(data_log) or not os.path.exists(ack_log):
                    print("[Missing files] Skipping", proto.upper())
                    continue

                sent_times = parse_log(data_log)
                ack_times = parse_log(ack_log)

                sent_count = count_per_interval(sent_times)
                ack_count = count_per_interval(ack_times)

                all_buckets = sorted(set(sent_count.keys()) | set(ack_count.keys()))
                losses = [(t, sent_count[t] - ack_count.get(t, 0)) for t in all_buckets]

                x = [t for t, _ in losses]
                y = [max(0, loss) for _, loss in losses]

                plt.plot(x, y, label=proto.upper())

            plt.title("Time-Series Packet Loss ({})".format(scenario))
            plt.xlabel("Time (s)")
            plt.ylabel("Lost Packets")
            plt.grid(True)
            plt.legend()
            out_name = "loss_timeseries_{}.png".format(scenario)
            plt.savefig(out_name)
            print("Saved:", out_name)

    except KeyboardInterrupt:
        print("\n[Interrupted] Gracefully exiting...")

if __name__ == "__main__":
    main()
