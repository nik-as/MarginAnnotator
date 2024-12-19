import sys
import os
import argparse
import csv
import pandas as pd

parser = argparse.ArgumentParser(description="Argparser")

parser.add_argument("-infile", help="File to read")
parser.add_argument("-outfile", help="File to write")
parser.add_argument("-in_delim", help="Delimiter of infile")
parser.add_argument("-out_delim", help="Delimiter of outfile")

args = parser.parse_args()

def cell_exists_and_not_empty(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[row]) and grid[row][col] != ""

# Read the TSV file into a 2D array
with open(str(args.infile), 'r') as file:
    reader = csv.reader(file, delimiter=args.in_delim.encode().decode('unicode_escape'))
    data = [row for row in reader]

try:
    bottom_right_has_data = cell_exists_and_not_empty(data, -1, len(data[0]))
    if bottom_right_has_data:
        raise Exception("Unknown table format: Bottom right cell is not empty.")
except Exception as e:
    print(f"Caught exception: {e}")

value_col_title = data[0][0] if data[0][0] != "" else "value"

row_titles = [cell for cell in data[-1] if cell != ""]

column_titles = []
column_headers = []
for i, row in enumerate(data):
    column_title_index = len(data[0])-1
    if not cell_exists_and_not_empty(data, i, column_title_index):
        #all column annotations read
        break
    column_titles.append(row[column_title_index])
    column_headers.append(row[len(row_titles):column_title_index])

row_headers = [row[:len(row_titles)] for row in data[len(column_titles):len(data)-1]]

stripped_data = [row[len(row_titles):] for row in data[len(column_titles):len(data)-1]]

proc_data = []
for row_index, data_row in enumerate(stripped_data):
    for col_index, _ in enumerate(column_headers[0]):
        datapoint = {}
        datapoint[value_col_title] = data_row[col_index]
        for i, field in enumerate(row_titles):
            datapoint[field] = row_headers[row_index][i]
        for i, field in enumerate(column_titles):
            datapoint[field] = column_headers[i][col_index]
        proc_data.append(datapoint)

sep = '\t'
if args.out_delim:
    sep = args.out_delim
pd.DataFrame(proc_data).to_csv(str(args.outfile), index=False, sep=sep.encode().decode('unicode_escape'))