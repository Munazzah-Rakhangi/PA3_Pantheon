# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt

data_file = 'log_data.csv'
scenarios = {
    'low_bw_high_rtt': 'Low BW, High RTT',
    'high_bw_low_rtt': 'High BW, Low RTT'
}

colors = {
    'bbr': 'blue',
    'cubic': 'orange',
    'vegas': 'green'
}

plt.figure()
with open(data_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        scheme = row['Scheme'].upper()
        scenario = row['Scenario']
        rtt = float(row['Delay (ms)'])
        tput = float(row['Throughput (Mbps)'])

        label = '{} ({})'.format(scheme, scenarios.get(scenario, scenario))
        plt.scatter(rtt, tput, s=100, label=label, color=colors[row['Scheme']])

plt.xlabel('RTT (ms) [Lower is Better]')
plt.ylabel('Throughput (Mbps) [Higher is  Better]')
plt.title('RTT vs Throughput Summary')
plt.grid(True)
plt.legend()
plt.gca().invert_xaxis()  # RTT closer to origin inverted
plt.savefig('summary_rtt_vs_throughput.png')
print("Saved: summary_rtt_vs_throughput.png")
