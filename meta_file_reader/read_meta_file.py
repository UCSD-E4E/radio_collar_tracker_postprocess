#!/usr/bin/env python
import fileinput

def read_meta_file(filename, tag):
    for line in fileinput.input(filename):
        if tag == line.strip().split(':')[0].strip():
            return line.strip().split(':')[1].strip()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Utility to read a parameter from a Radio Collar Tracker meta file.  If no such tag exists, returns 'None'.")
    parser.add_argument('-i', '--input', help = 'Meta file to read.  Uses stdin by default', metavar = 'metafile', dest = 'filename', default = '-')
    parser.add_argument('-t', '--tag', help = 'Tag to return.', metavar = 'tag', dest = 'tag', required = True)
    args = parser.parse_args()
    print(read_meta_file(args.filename, args.tag))
