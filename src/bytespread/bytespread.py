# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = bytespread.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import sys
import os
import numpy as np
from pathlib import Path
import math
from datetime import datetime

from bytespread import __version__

__author__ = "jonathanlurie"
__copyright__ = "jonathanlurie"
__license__ = "mit"

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version="bytespread {ver}".format(ver=__version__))
    parser.add_argument(
        "-d",
        dest="directory",
        required=True,
        help="The directly to analyse")

    parser.add_argument(
        "-w",
        dest="wildcard",
        default="*",
        required=False,
        help="Wildcard for file match within the directory (default: *)")

    parser.add_argument(
        "-c",
        dest="clusters",
        default=32,
        required=False,
        type=int,
        help="Number of clusters (default: 32)")

    parser.add_argument(
        "-b",
        dest="bricks",
        default=100,
        required=False,
        type=int,
        help="Number bricks to show for the longest column (default: 100)")

    parser.add_argument(
        "-r",
        dest="recursive",
        action='store_true',
        required=False,
        help="Recursive within the provided folder (default: false)")

    return parser.parse_args(args)


def byteToHumanReadable(nb_bytes):
    log2_bytes = math.log2(nb_bytes)
    # print(nb_bytes, " --> ", log2_bytes)

    if log2_bytes >= 0 and log2_bytes < 10:
        return "{}B".format(int(nb_bytes))
    elif log2_bytes >= 10 and log2_bytes < 20:
        readable_number = round((nb_bytes / math.pow(2, 10))*100)/100
        return "{}KB".format(readable_number)
    elif log2_bytes >= 20 and log2_bytes < 30:
        readable_number = round((nb_bytes / math.pow(2, 20))*100)/100
        return "{}MB".format(readable_number)
    elif log2_bytes >= 30 and log2_bytes < 40:
        readable_number = round((nb_bytes / math.pow(2, 30))*100)/100
        return "{}GB".format(readable_number)
    elif log2_bytes >= 40 and log2_bytes < 50:
        readable_number = round((nb_bytes / math.pow(2, 40))*100)/100
        return "{}TB".format(readable_number)
    elif log2_bytes >= 50:
        readable_number = round((nb_bytes / math.pow(2, 50))*100)/100
        return "{}PB".format(readable_number)
    else:
        return "UNKNOWN SIZE"


def main():
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(sys.argv[1:])
    dir = args.directory
    wild = args.wildcard
    rec = args.recursive
    nb_clusters = args.clusters
    bricks = args.bricks

    path_for_display = os.path.abspath(dir)

    all_paths = None
    if rec:
        all_paths = Path(dir).rglob(wild)
        path_for_display += " (recursive)"
    else:
        all_paths = Path(dir).glob(wild)
        path_for_display += " (non recursive)"

    f_sizes = []

    for path in all_paths:

        full_path = os.path.join(path.parent, path.name)
        byte_size = os.path.getsize(full_path)
        # print(full_path, byte_size)
        f_sizes.append(byte_size)

    f_sizes = np.array(f_sizes)
    # print(f_sizes)

    min_byte_length = np.amin(f_sizes)
    max_byte_length = np.amax(f_sizes)
    mean_byte_length = np.mean(f_sizes)
    std_byte_length = np.std(f_sizes)
    median_byte_length = np.median(f_sizes)

    histo, bin_edges = np.histogram(f_sizes, nb_clusters)
    histo = histo.astype("float32")
    histo_normalized = (np.copy(histo) / histo.max() * bricks).astype("uint32")

    print("[BYTESPREAD REPORT]")
    print()
    print("Date:                ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("Directory:           ", path_for_display)
    print("Filename match:      ", wild)
    print("Number of files:     ", f_sizes.shape[0])
    print("Smallest file:       ", byteToHumanReadable(min_byte_length))
    print("Largest file:        ", byteToHumanReadable(max_byte_length))
    print("Average size:        ", byteToHumanReadable(mean_byte_length))
    print("Standard deviation:  ", byteToHumanReadable(std_byte_length))
    print("Median size:         ", byteToHumanReadable(median_byte_length))
    print("Histogram intervals: ", byteToHumanReadable(bin_edges[1] - bin_edges[0]))
    print("Histogram:")
    print()

    for i in range(0, len(bin_edges)-1):
        lower_bound = byteToHumanReadable(bin_edges[i])
        upper_bound = byteToHumanReadable(bin_edges[i+1])
        print("|", "▓" * histo_normalized[i], "[{}-{}], {} files".format(lower_bound, upper_bound, math.ceil(histo[i])))


if __name__ == "__main__":
    main()
