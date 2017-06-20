#!/usr/bin/python
"""
Left similarity join between two CSV files.

For each row in the first file, take the specified join column and find
similar rows in the second file based on ngram similarity to a specified
column in the second file. For each resulting pair of rows, output a row
consisting of the fields from the first file, a column with the similarity
value, and then the fields from the second file.
"""
from __future__ import print_function

import csv, os, re
from ngram import NGram

def lowstrip(term):
    """Convert to lowercase and strip spaces"""
    term = re.sub('\s+', ' ', term)
    term = term.lower()
    return term

def main(left_path, left_column, right_path, right_column,
         outfile, titles, join, minscore, count, warp):
    """Perform the similarity join"""
    right_file = csv.reader(open(right_path, 'r'))
    if titles:
        right_header = next(right_file)
    index = NGram((tuple(r) for r in right_file),
                  threshold=minscore,
                  warp=warp, key=lambda x: lowstrip(x[right_column]))
    left_file = csv.reader(open(left_path, 'r'))
    out = csv.writer(open(outfile, 'w'), lineterminator='\n')
    if titles:
        left_header = next(left_file)
        out.writerow(left_header + ["Rank", "Similarity"] + right_header)
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

def console_main():
    """Process command-line arguments."""
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--titles', action='store_true',
                        help='input files have column titles')
    parser.add_argument(
        '-j', '--join', choices=['inner', 'outer'],
        help=('The kind of left join to perform.  Outer join outputs left-hand '
              'rows which have no right hand match, while inner join discards '
              'such rows. Default: %(default)s'))
    parser.add_argument('-m', '--minscore', type=float,
                        help='Minimum match score: %(default)s')
    parser.add_argument('-c', '--count', type=int,
                help='Max number of rows to match (0 for all): %(default)s')
    parser.add_argument('-w', '--warp', type=float,
            help='N-gram warp, higher helps short strings: %(default)s')
    parser.add_argument('left', nargs=1, help='First CSV file')
    parser.add_argument('leftcolumn', nargs=1, type=int, help='Column in first CSV file')
    parser.add_argument('right', nargs=1, help='Second CSV file')
    parser.add_argument('rightcolumn', nargs=1, type=int, help='Column in second CSV file')
    parser.add_argument('outfile', nargs=1, help='Output CSV file')
    parser.set_defaults(
        titles=False, join='outer', minscore=0.24, count=0, warp=1.0)
    args = parser.parse_args()
    for path in [args.left[0], args.right[0]]:
        if not os.path.isfile(path):
            parser.error('File "%s" does not exist.' % path)
    if not (0 <= args.minscore <= 1.0):
        parser.error("Minimum score must be between 0 and 1")
    if not args.count >= 0:
        parser.error("Maximum number of matches per row must be non-negative.")
    if args.count == 0:
        args.count = None # to return all results
    main(args.left[0], args.leftcolumn[0], args.right[0], args.rightcolumn[0],
         args.outfile[0], args.titles, args.join, args.minscore, args.count,
         args.warp)


if __name__ == '__main__':
    console_main()
