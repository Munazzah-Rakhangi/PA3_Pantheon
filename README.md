 Programming Assignment 3 - PANTHEON and MAHI MAHI
------------------------------------------------------------------
This repository contains a customized and fully configured version of Pantheon, 
a benchmarking framework for evaluating congestion control (CC) algorithms such 
as BBR, Cubic, and Vegas. The framework uses Mahimahi to emulate realistic 
network conditions and captures performance metrics including throughput, 
latency, and packet loss.

Setup Environment
-----------------
- OS: Ubuntu 22.04.5 LTS (in UTM on macOS, if virtualized)
- Python: 2.7
- Dependencies: matplotlib, PyYAML, numpy, Mahimahi, iperf3

Project Folder Structure
------------------------
- `src/`: Pantheon source code
- `tools/`: Support scripts
- `output/test_results/`: Stores logs and graphs for each CC scheme under test
- `output/data_analysis/`: Contains scripts for plotting and CSV extraction
- `traces/`: Network trace files (e.g., 1mbps.trace, 50mbps.trace)

Update Your System
------------------
sudo apt update && sudo apt upgrade -y

Install Core Dependencies
-------------------------
sudo apt install -y git python2 curl g++ cmake \
    pkg-config iproute2 iputils-ping \
    libssl-dev libpcap-dev python-is-python2 \
    python-pip python-setuptools python-wheel \
    libboost-all-dev autoconf automake \
    libprotobuf-dev protobuf-compiler \
    libtool linux-tools-common linux-tools-generic \
    linux-tools-$(uname -r) iperf3

Install Python 2 Manually
-------------------------
sudo apt install -y python2  
sudo ln -sf /usr/bin/python2 /usr/bin/python

Install pip for Python 2
------------------------
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py  
sudo python get-pip.py  

Check pip:
pip --version

Install setuptools and wheel
----------------------------
sudo pip install setuptools wheel

Re-run Full Install (Skip duplicates)
-------------------------------------
sudo apt install -y git curl g++ cmake \
    pkg-config iproute2 iputils-ping \
    libssl-dev libpcap-dev \
    python-pip \
    libboost-all-dev autoconf automake \
    libprotobuf-dev protobuf-compiler \
    libtool linux-tools-common linux-tools-generic \
    linux-tools-$(uname -r) iperf3

Clone Pantheon & Initialize Submodules
--------------------------------------
git clone https://github.com/StanfordSNR/pantheon.git  
cd pantheon  
git submodule update --init --recursive

Install Pantheon Dependencies
-----------------------------
./tools/install_deps.sh

Clone the Mahimahi Repo
-----------------------
cd ~  
git clone https://github.com/ravinet/mahimahi.git  
cd mahimahi  

Test installation:
which mm-link  

Install Apache and required packages:
sudo apt install apache2  
sudo apt install libxcb1-dev  
sudo apt install libxcb-present-dev  
sudo apt update  
sudo apt install libpangocairo-1.0-dev  
sudo apt install libpango1.0-dev libcairo2-dev  

Remove the broken PPA:
sudo add-apt-repository --remove ppa:keithw/mahimahi  
sudo apt update

Install missing dependencies:
sudo apt install libpango1.0-dev libcairo2-dev libglib2.0-dev

Build Mahimahi:
./configure  
make -j$(nproc)  
sudo make install

Enable IP Forwarding
--------------------
sudo sysctl -w net.ipv4.ip_forward=1

Test mm-delay:
mm-delay 100 bash -c 'echo "This ran in a 100ms delayed shell"'

Install YAML module
-------------------
sudo apt-get install python-yaml  
pip2 install 'PyYAML==5.3.1'

Install iperf and confirm BBR:
------------------------------
sudo apt-get install iperf3  
sudo apt-get install iperf  
iperf --version

Enable CC algorithms:
sudo sysctl -w net.ipv4.tcp_available_congestion_control="bbr cubic vegas"  
sysctl net.ipv4.tcp_available_congestion_control  
sysctl net.ipv4.tcp_congestion_control

Run Minimal Test (Part A)
-------------------------
Terminal 1:
python2 src/experiments/tunnel_manager.py

Terminal 2:
PYTHONPATH=src python2 src/experiments/test.py local --schemes bbr --data-dir output/test_results/bbr --runtime 60  
PYTHONPATH=src python2 src/experiments/test.py local --schemes cubic --data-dir output/test_results/cubic --runtime 60  
PYTHONPATH=src python2 src/experiments/test.py local --schemes vegas --data-dir output/test_results/vegas --runtime 60  

Permission Fix (If needed):
sudo sysctl -w net.ipv4.tcp_allowed_congestion_control="vegas cubic reno"  
sudo modprobe tcp_vegas  
sysctl net.ipv4.tcp_available_congestion_control

Analyze Each Scheme
-------------------
sudo apt-get install python2 python2-dev  
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py  
sudo python2 get-pip.py  
sudo pip2 install numpy  
sudo apt-get install build-essential gfortran libopenblas-dev liblapack-dev  
sudo pip2 install numpy  
sudo pip2 install matplotlib  
sudo apt install texlive-latex-extra

Run Analysis:
PYTHONPATH=src python2 src/analysis/analyze.py --data-dir output/test_results/bbr  
PYTHONPATH=src python2 src/analysis/analyze.py --data-dir output/test_results/cubic  
PYTHONPATH=src python2 src/analysis/analyze.py --data-dir output/test_results/vegas

Part B: Network Profiles
------------------------

Create Traces:
mkdir -p traces  
python2 -c "import sys; [sys.stdout.write('1500\n') for _ in range(4167)]" > traces/50mbps.trace  
python2 -c "import sys; [sys.stdout.write('1500\n') for _ in range(83)]" > traces/1mbps.trace  

Low-Latency, High-Bandwidth (10ms Delay, 50 Mbps):
--------------------------------------------------
BBR:
python2 src/experiments/test.py local --schemes "bbr" \
--uplink-trace traces/50mbps.trace \
--downlink-trace traces/50mbps.trace \
--prepend-mm-cmds "mm-delay 10" \
--data-dir output/test_results/bbr/high_bw_low_rtt  

CUBIC:
python2 src/experiments/test.py local --schemes "cubic" \
--uplink-trace traces/50mbps.trace \
--downlink-trace traces/50mbps.trace \
--prepend-mm-cmds "mm-delay 10" \
--data-dir output/test_results/cubic/high_bw_low_rtt  

VEGAS:
python2 src/experiments/test.py local --schemes "vegas" \
--uplink-trace traces/50mbps.trace \
--downlink-trace traces/50mbps.trace \
--prepend-mm-cmds "mm-delay 10" \
--data-dir output/test_results/vegas/high_bw_low_rtt  

High-Latency, Low-Bandwidth (100ms Delay, 1 Mbps):
--------------------------------------------------
BBR:
python2 src/experiments/test.py local --schemes "bbr" \
--uplink-trace traces/1mbps.trace \
--downlink-trace traces/1mbps.trace \
--prepend-mm-cmds "mm-delay 100" \
--data-dir output/test_results/bbr/low_bw_high_rtt  

CUBIC:
python2 src/experiments/test.py local --schemes "cubic" \
--uplink-trace traces/1mbps.trace \
--downlink-trace traces/1mbps.trace \
--prepend-mm-cmds "mm-delay 100" \
--data-dir output/test_results/cubic/low_bw_high_rtt  

VEGAS:
python2 src/experiments/test.py local --schemes "vegas" \
--uplink-trace traces/1mbps.trace \
--downlink-trace traces/1mbps.trace \
--prepend-mm-cmds "mm-delay 100" \
--data-dir output/test_results/vegas/low_bw_high_rtt  

Run Duration Verification
-------------------------
All tests run for at least 60 seconds by default (see src/wrappers/ files)

Part C: Metric Collection and Analysis
======================================

Extract Metrics to CSV
-----------------------
cd output/data_analysis  
python2 generate_csv.py

Output:
log_data.csv will be created in the same folder

Generate Throughput Plots
--------------------------
python2 plot_throughput_timeseries.py

Output:
* throughput_timeseries_low_bw_high_rtt.png  
* throughput_timeseries_high_bw_low_rtt.png

Generate Loss Plots
-------------------
python2 plot_loss_timeseries.py

Output:
* loss_timeseries_low_bw_high_rtt.png  
* loss_timeseries_high_bw_low_rtt.png

Generate RTT Comparison Plots
-----------------------------
python2 plot_rtt_comparison.py

Output:
* rtt_comparison_low_bw_high_rtt.png  
* rtt_comparison_high_bw_low_rtt.png

Generate Summary Plot (RTT vs Throughput)
-----------------------------------------
python2 plot_summary_rtt_vs_throughput.py

Output:
* summary_rtt_vs_throughput.png

