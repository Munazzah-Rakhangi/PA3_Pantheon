# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import numpy as np

PROTOCOLS = ['bbr', 'cubic', 'vegas']
SCENARIOS = ['low_bw_high_rtt', 'high_bw_low_rtt']

def parse_rtt_from_log(filepath):
    rtts = []
    try:
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
                    rtts.append(timestamp / 1000.0)  # Convert ms → seconds
                except:
                    continue
    except IOError:
        print("[Missing]", filepath)
    return rtts

def main():
    print("Generating RTT stats comparison plots...\n")
    width = 0.35
    x = np.arange(len(PROTOCOLS))  # For each protocol

    for scenario in SCENARIOS:
        avg_rtts = []
        p95_rtts = []

        for proto in PROTOCOLS:
            log_path = '../test_results/{}/{}/{}_mm_acklink_run1.log'.format(proto, scenario, proto)
            print("Reading:", log_path)
            rtts = parse_rtt_from_log(log_path)
            if not rtts:
                avg_rtts.append(0)
                p95_rtts.append(0)
            else:
                avg_rtts.append(np.mean(rtts) * 1000)   # Convert back to ms
                p95_rtts.append(np.percentile(rtts, 95) * 1000)

        fig, ax = plt.subplots()
        ax.bar(x - width/2, avg_rtts, width, label='Average RTT')
        ax.bar(x + width/2, p95_rtts, width, label='95th %ile RTT')

        ax.set_ylabel('RTT (ms)')
        ax.set_title('RTT Comparison ({})'.format(scenario))
        ax.set_xticks(x)
        ax.set_xticklabels([p.upper() for p in PROTOCOLS])
        ax.legend()
        ax.grid(True)

        out_file = 'rtt_comparison_{}.png'.format(scenario)
        plt.savefig(out_file)
        print("Saved:", out_file)
        plt.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting gracefully.")
