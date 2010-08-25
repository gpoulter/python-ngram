#!/usr/bin/python
"""
:mod:`simjoin` -- Join CSV files using NGram similarity of a field
==================================================================

Performs a left similarity join between two CSV files. For each row in the
first file, take the specified join column and find similar rows in the 
second file based on ngram similarity to a specified column in the second file.

For each resulting pair of rows, output a row consisting of the
fields from the first file, a column with the similarity value, and then the
fields from the second file.

Usage::

  python %prog [options] <file1> <column1> <file2> <column2> <outfile>

.. cmdoption  <file1>, <file2>

   The files to join

Specify CSV file then the column in the file to use for joining. <outfile>
is where to write the CSV results.  

For example::

  python %prog -c 5 -m 0.24 -t -j outer left.csv 1 right.csv 1 out.csv

left.csv::
 ID,NAME
 1,Joe
 2,Kin
 3,ZAS

right.csv::
 ID,NAME
 A,Joe
 B,Jon
 C,Job
 D,Kim

out.csv::
 ID,NAME,Rank,Similarity,ID,NAME
 1,Joe,1,1.0,A,Joe
 1,Joe,2,0.25,B,Jon
 1,Joe,3,0.25,C,Job
 2,Kin,1,0.25,D,Kim
 3,ZAS

"""

import csv, os, re, sys
from ngram import NGram

def lowstrip(term):
    """Convert to lowercase and strip spaces"""
    term = re.sub('\s+', ' ', term)
    term = term.lower()
    return term

def main(left_path, left_column, right_path, right_column, outfile, titles, join, minscore, count, warp):
    """Perform the similarity join"""
    right_file = csv.reader(open(right_path,'r'))
    if titles:
        right_header = right_file.next()
    index = NGram((tuple(r) for r in right_file), 
                  threshold=minscore, 
                  warp=warp, key=lambda x: lowstrip(x[right_column]))
    left_file = csv.reader(open(left_path,'r'))
    out = csv.writer(open(outfile,'w'))
    if titles:
        left_header = left_file.next()
        out.writerow(left_header + ["Rank","Similarity"] + right_header)
    for row in left_file:
        if not row: continue # skip blank lines
        row = tuple(row)
        results = index.search(lowstrip(row[left_column]), threshold=minscore)
        if results:
            if count > 0:
                results = results[:count]
            for rank, result in enumerate(results, 1):
                out.writerow(row + (rank, result[1]) + result[0])
        elif join == "outer":
            out.writerow(row)

def parse_arguments(args=sys.argv[1:]):
    """Process command-line arguments."""
    from optparse import OptionParser
    parser = OptionParser()
    parser.set_usage(__doc__.strip())
    parser.add_option("-t", "--titles", action="store_true", 
                      help="The input files contain a heading row with column titles")
    parser.add_option("-j", "--join", action="store", type="choice", choices=["inner", "outer"],
                      help=("The kind of left join to perform.  Outer join outputs left-hand "
                            "rows which have no right hand match, while inner join discards "
                            "such rows. Default is 'outer'."))
    parser.add_option("-m", "--minscore", action="store", type="float",
                      help="Minimum score for outputting a match (default 0.24)")
    parser.add_option("-c", "--count", action="store", type="int",
                      help="Maximum number of matching right-hand columns to output (0 for all).")
    parser.add_option("-w", "--warp", action="store", type="float",
                      help="Set the warp for N-Gram similarity (default 1.0).  Increase to help short strings.")
    parser.set_defaults(titles=False, join="outer", minscore=0.24, count=0, warp=1.0)
    kw, args = parser.parse_args(args)
    # Extract and check positional arguments
    try:
        csv1, csv1_column, csv2, csv2_column, outfile = args
    except:
        parser.error("Invalid number of arguments.")
    for path in [csv1,csv2]:
        if not os.path.isfile(path):
            parser.error('File "%s" does not exist.' % path)
    try:
        csv1_column = int(csv1_column)
        csv2_column = int(csv2_column)
    except ValueError:
        parser.error('Columns must be integer')
    if not (0 <= kw.minscore <= 1.0):
        parser.error("Minimum score must be between 0 and 1")
    if not kw.count >= 0:
        parser.error("Maximum number of matches per row must be non-negative.")
    if kw.count == 0:
        kw.count = None # to return all results
    return (csv1, csv1_column, csv2, csv2_column, outfile), kw

if __name__ == '__main__':
    args, kwargs = parse_arguments()
    main(*args, **kwargs.__dict__)
