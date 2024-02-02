#!/usr/bin/env python3

# File: Lib/tests/test_limit_line_length.py

"""
-rw-r--r-- 1 alex alex       1662 Jan 20 19:43 expected_res1arg.txt
-rw-r--r-- 1 alex alex          0 Jan 22 13:35 __init__.py
-rw-r--r-- 1 alex alex       1663 Jan 16 14:02 long_lines.txt
drwxr-xr-x 2 alex autologin  4096 Jan 31 13:22 __pycache__
-rwxr-xr-x 1 alex alex       1961 Jan 31 13:24 test_limit_line_length.py
"""
import os
import sys
import shutil
import unittest
from subprocess import run
import limit_line_length


textfile = "tests/long_lines.txt"
copy = "tests/ll.txt"
expected_res1arg = "tests/expected_res1arg.txt"
res1arg = "tests/new_ll.txt"

class TestLimitLineLength(unittest.TestCase):

    def content(self, file_name):
        try:
            with open(file_name, 'r') as stream:
                return stream.read()
        except FileNotFoundError as err:
            print("OS error:", err)
            print(f"file {file_name} not found")
            raise

    def setUP(self):
        shutil.copyfile(textfile, copy)
    
    def test_no_argF(self):
        """ 
        "testing the function vs no argument"
        """
        with self.assertRaises(TypeError):
            limit_line_length.limit_line_length()
    
    def test_no_argM(self):
        """
        "testing the module vs no argument"
        """
        output = run(('./limit_line_length.py'),
                        capture_output=True)
        self.assertTrue(output.stdout.decode(
                encoding='utf-8',
                errors='strict').startswith(
                    'Must provide at least one parameter!'))

    def test_1arg(self):
        """ "testing with only the file name as an arg" """
        output = run(('./limit_line_length.py', copy),
                        capture_output=True)
        self.assertEqual(self.content(expected_res1arg),
                        self.content(res1arg))

    def test_2arg_as_decimal(self):
        self.assertEqual(1, 1)

    def test_2arg_as_name(self):
        self.assertEqual(1, 1)

    def test_3arg(self):
        self.assertEqual(1, 1)

    def tearDown(self):
        if os.path.exists(copy):
            os.remove(copy)
        if os.path.exists(res1arg):
            os.remove(res1arg)
#       if os.path.exists():
#           os.remove()

if __name__ == "__main__":
    unittest.main()
