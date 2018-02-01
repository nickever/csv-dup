#!/usr/bin/env python3

import sys
import datetime

# Which column number do you want to find duplicates in?
column = 2

# Creating empty lists of duplicates and non-duplicates
entries = []
duplicate_entries = []

# Starting row count. If header row then '-1', else '0'
row_count = -1

# File path of data set (input). Output file path will be created automatically if duplicates are found
input_filepath = "mockcsv.csv"
output_filepath = "mockcsv_duplicates.csv"


def find_duplicates():
    """
    Iterates through the rows of the csv to find duplicates by comparing to previous rows.
    Only compares one column within each row; choose which column using column variable above
    """
    global row_count
    with open(input_filepath, 'r') as f:
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

        if len(duplicate_entries) > 0:  # Do we have any duplicates?
            totals_print()
            print("duplicates found: please see {}".format(output_filepath))
            output_duplicates()
        else:
            totals_print()
            print("No Duplicates")



def output_duplicates():
    """
    Prints any rows that occur twice or more in the csv to the terminal (i.e prints original and duplicates)
    as well as saving them to a new csv file as specified in output_filepath above.
    """
    if len(duplicate_entries) > 0:
        with open(output_filepath, 'w') as out_file:
            with open(input_filepath, 'r') as f:
                for row_str in f:
                    row = row_str.strip().split(',')
                    if row[column] in duplicate_entries:
                        out_file.write(row_str)
    else:
        print("no duplicates found")


def screen_refresh():
    lines_printed = 2
    while lines_printed > 0:  # Clear previous lines of printed times
        sys.stdout.write("\033[F")  # up one line
        sys.stdout.write("\033[K")  # clear line
        lines_printed -= 1


def totals_print():
    print("Rows Checked: {}\nDuplicate Entries: {}".format(row_count, len(duplicate_entries)))


try:
    start = datetime.datetime.now()
    find_duplicates()
    dur = str(datetime.datetime.now()-start).split(":")
    print("Completed In: {}hr {}m {}s".format(dur[0], dur[1], dur[2].split(".")[0]))
except IndexError:
    totals_print()
    sys.exit("INDEX ERROR: check row {}".format(row_count))
except KeyboardInterrupt:
    totals_print()
    sys.exit("Keyboard Interrupt. Exiting...")
