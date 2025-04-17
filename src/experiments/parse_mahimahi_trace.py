#!/usr/bin/env python2
import argparse
import os

def write_trace(path, capacity_mbps, delay_ms):
    # Convert Mbps to bytes per ms
    bytes_per_ms = (capacity_mbps * 1000000) / 8 / 1000
    with open(path, 'w') as f:
        for t in range(60000):  # 60 seconds trace (60000 ms)
            f.write('%d\n' % bytes_per_ms)

    print("Trace written to:", path)
    print("Capacity: %d Mbps, Delay: %d ms" % (capacity_mbps, delay_ms))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Mahimahi trace file.")
    parser.add_argument('--uplink-capacity', type=int, required=True)
    parser.add_argument('--uplink-delay', type=int, required=True)
    parser.add_argument('--uplink-trace-path', type=str, required=True)
    parser.add_argument('--downlink-capacity', type=int, required=True)
    parser.add_argument('--downlink-delay', type=int, required=True)
    parser.add_argument('--downlink-trace-path', type=str, required=True)

    args = parser.parse_args()

    write_trace(args.uplink_trace_path, args.uplink_capacity, args.uplink_delay)
    write_trace(args.downlink_trace_path, args.downlink_capacity, args.downlink_delay)
