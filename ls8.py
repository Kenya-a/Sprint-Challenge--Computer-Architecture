#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
from argparse import ArgumentParser

parser = ArgumentParser(description='select a file in the ls8 folder to run')
parser.add_argument('filename', type=str, help='please select a filename')

args = parser.parse_args()

cpu = CPU()

cpu.load(args.filename)
cpu.run()