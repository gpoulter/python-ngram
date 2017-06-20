#!/usr/bin/python

import os
import os.path
import subprocess
import sys
import tempfile
import textwrap
import unittest

class CsvjoinTests(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="csvjoin_test_")
        self.leftpath = os.path.join(self.tmpdir, 'left')
        self.rightpath = os.path.join(self.tmpdir, 'right')
        self.outpath = os.path.join(self.tmpdir, 'output')
        with open(self.leftpath, 'w') as left:
            left.write('''ID,NAME\n1,Joe\n2,Kin\n3,ZAS''')
        with open(self.rightpath, 'w') as right:
            right.write('''ID,NAME\nID,NAME\nA,Joe\nB,Jon\nC,Job\nD,Kim''')

    def tearDown(self):
        os.remove(self.leftpath)
        os.remove(self.rightpath)
        os.remove(self.outpath)
        os.rmdir(self.tmpdir) 

    def test_csvjoin(self):
        args = [
            sys.executable,
            'scripts/csvjoin.py', '--titles', '-j', 'outer', '--minscore=0.24',
            '--count=5', '--warp=1.0',
            self.leftpath, '1', self.rightpath, '1', self.outpath
        ]
        print(args)
        subprocess.call(args)
        with open(self.outpath, 'r') as out:
            result = '\n'.join(s.strip() for s in out.readlines())
            correct = textwrap.dedent("""\
                ID,NAME,Rank,Similarity,ID,NAME
                1,Joe,1,1.0,A,Joe
                1,Joe,2,0.25,B,Jon
                1,Joe,3,0.25,C,Job
                2,Kin,1,0.25,D,Kim
                3,ZAS""")
            self.assertEqual(result, correct)

if __name__ == "__main__":
    unittest.main()
