#!/usr/bin/python3.4
import sys
import random
from itertools import product


def file_to_list(filename):
    with open(filename) as inputFile:
        return [l.rstrip("\n") for l in inputFile][1:]


def generate_pairs(file1, file2):
    recursive = file_to_list(sys.argv[1])
    authoritative = file_to_list(sys.argv[2])

    test_pairs = list(product(recursive, authoritative)) * int(sys.argv[3])
    random.shuffle(test_pairs)

    for r, a in test_pairs:
        print("{},{}".format(r, a))


if __name__ == "__main__":
    generate_pairs(sys.argv[1], sys.argv[2])
