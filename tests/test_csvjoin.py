#!/usr/bin/python

import unittest
import subprocess
import tempfile
import textwrap

class CsvjoinTests(unittest.TestCase):

    def test_csvjoin(self):
        left = tempfile.NamedTemporaryFile()
        left.write('''ID,NAME\n1,Joe\n2,Kin\n3,ZAS''')
        left.flush()
        right = tempfile.NamedTemporaryFile()
        right.write('''ID,NAME\nID,NAME\nA,Joe\nB,Jon\nC,Job\nD,Kim''')
        right.flush()
        output = tempfile.NamedTemporaryFile()
        subprocess.call([
            'csvjoin.py', '--titles', '-j', 'outer', '--minscore=0.24',
            '--count=5', '--warp=1.0',
            left.name, '1', right.name, '1', output.name])
        result = '\n'.join(s.strip() for s in output.readlines())
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
