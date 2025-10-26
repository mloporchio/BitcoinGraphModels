"""
    This script reads a TSV file, computes basic statistics for each column,
    and writes the results to a new TSV or XLSX file.
    fastexcel and XlsxWriter
    Author: Matteo Loporchio
"""

import polars as pl
import numpy as np
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if not (output_file.endswith(".tsv") or output_file.endswith(".xlsx")):
        print("Error: output file must be a .TSV or .XLSX file.")
        sys.exit(1)
    print(f"Reading data from {input_file}...")
    df = pl.read_csv(input_file, separator="\t", null_values=["nan", "-nan"])
    data = df.describe()
    if output_file.endswith(".tsv"):
        data.write_csv(output_file, separator="\t", null_value="nan")
    else:
        data.write_excel(output_file)
    print(f"Statistics written to {output_file}.")
