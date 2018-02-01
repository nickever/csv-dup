#!/usr/bin/env python3

"""
Command Line Interface program to find and remove / export duplicates from a csv file
"""

import sys
import pathlib
import argparse
import datetime

__author__ = "Nick Everett"
__version__ = "1.0.0"
__license__ = "GNU GPLv3"

# Creating empty lists of duplicates and non-duplicates
entries = []
duplicate_entries = []

# Global variable to count as we iterate through rows in csv
row_count = 0


def find_duplicates(input_file, output_file, column):
    """
    Iterates through the rows of the csv to find duplicates by comparing to previous rows.
    Only compares one column within each row. As specified in args -c --column.
    """
    global row_count
    with open(input_file, 'r') as f:
        for row_str in f:
            row = row_str.strip().split(',')
            if row[column] not in entries:
                row_count += 1
                entries.append(row[column])
            else:
                row_count += 1
                duplicate_entries.append(row[column])
            totals_print()
            screen_refresh()
    f.close()
    totals_print()
    output_duplicates(input_file, output_file, column)


def output_duplicates(input_file, output_file, column):
    """
    Prints any rows that occur twice or more in the csv to the terminal (i.e prints original and duplicates)
    or saves them to a new csv file if specified in args -o --outfile.
    """
    global row_count
    row_count = 0   # reset row count global var
    if len(duplicate_entries) > 0:  # Do we have any duplicates?
        with open(input_file, 'r') as f:
            if output_file is None:
                print("{: ^6}| Data".format("Row"))
                for row_str in f:
                    row = row_str.strip().split(',')
                    row_count += 1
                    if row[column] in duplicate_entries:
                        print("{: ^6}| {}".format(row_count, row_str.strip()))
            else:
                with open(output_file, 'a+') as out_file:
                    for row_str in f:
                        row = row_str.strip().split(',')
                        if row[column] in duplicate_entries:
                            out_file.write(row_str)
                print("Duplicates found: please see '{}'".format(output_file))
                out_file.close()
        f.close()
    else:
        print("No Duplicates")


def screen_refresh():
    lines_printed = 2
    while lines_printed > 0:  # Clear previous lines of printed times
        sys.stdout.write("\033[F")  # up one line
        sys.stdout.write("\033[K")  # clear line
        lines_printed -= 1


def totals_print():
    print("Rows Checked: {}\nDuplicate Entries: {}".format(row_count, len(duplicate_entries)))


def parse_args():       # Command line arguments
    description = (
        'Command Line Interface program to find and remove / export duplicates from a csv file '
        '- https://github.com/nickever/csv-dup')
    parser = argparse.ArgumentParser(description=description, usage='%(prog)s [-h] [-o] [-v] [--version] input_file -c')

    parser.add_argument("input_file", type=str,
                        help="input file path (required)")
    parser.add_argument("-c", "--column", type=int, required=True, default=0, metavar='',
                        help="column to search for duplicates, as integer (required)")
    parser.add_argument("-o", "--output_file", action="store", default=None,
                        help="output file path", metavar='')
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="verbosity (-v, -vv, etc)")
    parser.add_argument(
        "--version",
        action="version",
        version="{} (version {})".format("%(prog)s", __version__))
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    try:
        if args.output_file is not None and pathlib.Path(args.output_file).exists():
            sys.exit("'{}' already exists, please specify a unique filename".format(args.output_file))
        else:
            start = datetime.datetime.now()
            find_duplicates(args.input_file, args.output_file, args.column)
            dur = str(datetime.datetime.now() - start).split(":")
            print("Completed In: {}hr {}m {}s".format(dur[0], dur[1], dur[2].split(".")[0]))
    except IndexError:
        totals_print()
        if row_count > 0:
            sys.exit("INDEX ERROR: check row {}".format(row_count + 1))
        else:
            sys.exit("INDEX ERROR: check column arg vs number of columns")
    except KeyboardInterrupt:
        totals_print()
        sys.exit("Keyboard Interrupt. Exiting...")


if __name__ == "__main__":      # executed when run from the command line
    main()
