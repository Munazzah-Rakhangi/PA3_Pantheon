#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

import arg_parser
import context
from helpers.subprocess_wrappers import check_call


def main():
    args = arg_parser.parse_analyze()

    analysis_dir = path.join(context.src_dir, 'analysis')
    plot = path.join(analysis_dir, 'plot.py')
    report = path.join(analysis_dir, 'report.py')  # ← uncommented this

    # Build plot command
    plot_cmd = ['python', plot]
    if args.data_dir:
        plot_cmd += ['--data-dir', args.data_dir]
    if args.schemes:
        plot_cmd += ['--schemes', args.schemes]
    if args.include_acklink:
        plot_cmd += ['--include-acklink']

    # Run plot script
    check_call(plot_cmd)

    # Build report command
    report_cmd = ['python', report]  # ← uncommented
    if args.data_dir:
        report_cmd += ['--data-dir', args.data_dir]
    if args.schemes:
        report_cmd += ['--schemes', args.schemes]
    if args.include_acklink:
        report_cmd += ['--include-acklink']

    # Run report script (generates PDF)
    check_call(report_cmd)  # ← uncommented


if __name__ == '__main__':
    main()

